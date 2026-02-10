from montepython.likelihood_class import Likelihood
from numpy import matrix, dot, exp, log


class Qcmb(Likelihood):

    def loglkl(self, cosmo, data):
        _100theta_s, ob, om = (
            data.mcmc_parameters[p]['current']*data.mcmc_parameters[p]['scale']
            for p in ['theta_s_100', 'omega_b', 'omega_m'])
        diffvec = matrix([x-mu for x, mu in zip([_100theta_s, ob, om], self.centre)])
        minusHessian = matrix(self.covmat).I
        lkl = exp(-0.5 * (dot(diffvec, dot(minusHessian, diffvec.T))))
        return log(lkl)
