import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
from matplotlib.gridspec import GridSpec
from scipy.interpolate import interp1d
from scipy.optimize import brentq
from matplotlib.ticker import LogLocator, NullFormatter
from scipy.ndimage import gaussian_filter
import datetime

class DESI_like_data:
    def __init__(self, mean_file, cov_file):
        self.mean_file = mean_file
        self.cov_file = cov_file
        self.z = np.array([], 'float64')
        self.data_array = np.array([], 'float64')
        self.quantity = []
        # read redshifts and data points
        with open(self.mean_file, 'r') as filein:
            for i, line in enumerate(filein):
                if line.strip() and line.find('#') == -1:
                    this_line = line.split()
                    self.z = np.append(self.z, float(this_line[0]))
                    self.data_array = np.append(self.data_array, float(this_line[1]))
                    self.quantity.append(str(this_line[2]))
        # read covariance matrix
        self.cov_data = np.loadtxt(self.cov_file)
        # number of bins
        self.num_bins = np.shape(self.z)[0]
        # number of data points
        self.num_points = np.shape(self.cov_data)[0]
    def make_fake_DESI_data(self, cosmo, mean_noise=False, seed=None, return_theory=False):
        # make fake data by adding Gaussian noise to the theory array
        # the noise is drawn from a multivariate normal distribution with mean 0 and covariance given by the covariance matrix
        theory = np.zeros(self.num_bins)
        rs = cosmo.rs_drag()
        for i in range(self.num_bins):
            DM_at_z = cosmo.angular_distance(self.z[i]) * (1. + self.z[i])
            H_at_z = cosmo.Hubble(self.z[i])
            theo_DM_over_rs = DM_at_z / rs
            theo_DH_over_rs = 1. / H_at_z / rs
            theo_DV_over_rs = (self.z[i] * DM_at_z**2 / H_at_z)**(1./3.) / rs
            # calculate theory predictions
            if self.quantity[i] == 'DV_over_rs':
                theory[i] = theo_DV_over_rs
            elif self.quantity[i] == 'DM_over_rs':
                theory[i] = theo_DM_over_rs
            elif self.quantity[i] == 'DH_over_rs':
               theory[i] = theo_DH_over_rs
        rng = np.random.default_rng(seed)
        noise = rng.multivariate_normal(
            mean=np.zeros(self.num_bins, dtype=np.float64),
            cov=self.cov_data
        )
        if mean_noise:
            mock = theory + noise
        else:
            mock = theory.copy()
        fake_cov = self.cov_data
        if return_theory:
            return {'dat':mock, 'cov':fake_cov, 'th':theory}
        else:
            return {'dat':mock, 'cov':fake_cov}
    def make_fake_likelihood(self, cosmo, model,mean_noise=False,seed=False):
        # generate the mock data
        result = self.make_fake_DESI_data(cosmo, mean_noise=mean_noise,seed=seed)
        mock_data = result['dat']
        mock_cov = result['cov']

        # create unique name based on model and timestamp
        now = datetime.datetime.now()
        tag = model + "_" + now.strftime("%Y%m%d%H%M%S")
        lk_name = "mock_bao_desi_dr2_" + tag

        lk_dir = "../../montepython_fDE/montepython/likelihoods/" + lk_name
        dat_dir = "../../montepython_fDE/data/" + lk_name

        if not os.path.exists(lk_dir):
            os.makedirs(lk_dir)
        if not os.path.exists(dat_dir):
            os.makedirs(dat_dir)

        # --- write mean file ---
        mean_filename = lk_name + "_mean.txt"
        mean_path = os.path.join(dat_dir, mean_filename)
        with open(mean_path, 'w') as f:
            f.write("# mock DESI-like BAO data\n")
            f.write("# model: {}\n".format(model))
            f.write("# Cosmological parameters: ")
            for key, val in cosmo.pars.items():
                f.write("#   {} = {}, ".format(key, val))
            f.write("\n# [z] [value at z] [quantity]\n")
            for i in range(self.num_bins):
                f.write("{:.8f} {:.12f} {}\n".format(
                    self.z[i], mock_data[i], self.quantity[i]))

        # --- write covariance file ---
        cov_filename = lk_name + "_cov.txt"
        cov_path = os.path.join(dat_dir, cov_filename)
        np.savetxt(cov_path, mock_cov, fmt='%.8e')

        # --- write __init__.py ---
        init_path = os.path.join(lk_dir, "__init__.py")
        init_content = '''import os
import numpy as np
import warnings
import montepython.io_mp as io_mp
from montepython.likelihood_class import Likelihood
import scipy.constants as conts

#  adapted from bao_boss_dr12 likelihood
class {class_name}(Likelihood):

    # initialization routine
    def __init__(self, path, data, command_line):

        Likelihood.__init__(self, path, data, command_line)
        # Note: need to check for conflicting experiments manually

        # define arrays for values of z and data points
        self.z = np.array([], 'float64')
        self.data_array = np.array([], 'float64')
        self.quantity = []

        # read redshifts and data points
        with open(os.path.join(self.data_directory, self.data_file), 'r') as filein:
            for i, line in enumerate(filein):
                if line.strip() and line.find('#') == -1:
                    this_line = line.split()
                    self.z = np.append(self.z, float(this_line[0]))
                    self.data_array = np.append(self.data_array, float(this_line[1]))
                    self.quantity.append(str(this_line[2]))

        # read covariance matrix
        self.cov_data = np.loadtxt(os.path.join(self.data_directory, self.cov_file))

        # number of bins
        self.num_bins = np.shape(self.z)[0]

        # number of data points
        self.num_points = np.shape(self.cov_data)[0]

        # end of initialization

    # compute likelihood

    def loglkl(self, cosmo, data):

        # for each point, compute comoving angular diameter distance D_M = (1 + z) * D_A,
        # Hubble distance D_H = 1 / H(z),
        # sound horizon at baryon drag rs and
        # angle-averaged distance D_V = (z * D_M^2 * D_H)^(1/3)
        
        diff = np.zeros(self.num_bins)
        for i in range(self.num_bins):

            DM_at_z = cosmo.angular_distance(self.z[i]) * (1. + self.z[i])
            H_at_z = cosmo.Hubble(self.z[i])
            rs = cosmo.rs_drag()

            theo_DM_over_rs = DM_at_z / rs
            theo_DH_over_rs = 1. / H_at_z / rs
            theo_DV_over_rs = (self.z[i] * DM_at_z**2 / H_at_z)**(1./3.) / rs

            # calculate difference between the sampled point and observations
            if self.quantity[i] == 'DV_over_rs':
                diff[i] = theo_DV_over_rs - self.data_array[i]
            elif self.quantity[i] == 'DM_over_rs':
                diff[i] = theo_DM_over_rs - self.data_array[i]
            elif self.quantity[i] == 'DH_over_rs':
                diff[i] = theo_DH_over_rs - self.data_array[i]
        
        # compute chi squared
        inv_cov_data = np.linalg.inv(self.cov_data)
        chi2 = np.dot(np.dot(diff,inv_cov_data),diff)

        # return ln(L)
        loglkl = - 0.5 * chi2

        return loglkl
'''.format(class_name=lk_name)

        with open(init_path, 'w') as f:
            f.write(init_content)

        # --- write .data file ---
        data_file_path = os.path.join(lk_dir, lk_name + ".data")
        with open(data_file_path, 'w') as f:
            f.write("# mock DESI-like BAO data\n")
            f.write("# model: {}\n".format(model))
            f.write("{}.data_directory      = data.path['data']\n".format(lk_name))
            f.write("{}.data_file           = '{}/{}'\n".format(
                lk_name, lk_name, mean_filename))
            f.write("{}.cov_file            = '{}/{}'\n".format(
                lk_name, lk_name, cov_filename))

        print("Created likelihood: {}".format(lk_name))
        print("  Likelihood dir: {}".format(lk_dir))
        print("  Data dir:       {}".format(dat_dir))

        return lk_name


