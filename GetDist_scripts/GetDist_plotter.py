from getdist import loadMCSamples, MCSamples
from getdist import plots
import os
from tqdm import trange
import numpy as np
import matplotlib.pyplot as plt

burnin = 0.05
smooth1D = 0.4
smooth2D = 0.6


file_name0='2026-02-10_50030_'
desi_cmb_fa_dir='/scratch/09218/gab97/chains/desi_dr2_Qcmb_fa_v1/'+file_name0
desi_cmb_w0wa_dir='/scratch/09218/gab97/chains/desi_dr2_Qcmb_w0wa_v1/'+file_name0
desi_cmb_lcdm_dir='/scratch/09218/gab97/chains/desi_dr2_Qcmb_lcdm_v1/'+file_name0


desi_cmb_fa_samples= loadMCSamples(desi_cmb_fa_dir,settings={'ignore_rows': burnin, 'smooth_scale_1D': smooth1D, 'smooth_scale_2D': smooth2D})
desi_cmb_w0wa_samples= loadMCSamples(desi_cmb_w0wa_dir,settings={'ignore_rows': burnin, 'smooth_scale_1D': smooth1D, 'smooth_scale_2D': smooth2D})
desi_cmb_lcdm_samples= loadMCSamples(desi_cmb_lcdm_dir,settings={'ignore_rows': burnin, 'smooth_scale_1D': smooth1D, 'smooth_scale_2D': smooth2D})

pars_w0wa = ["omega_b","omega_m","theta_s_100","w0_fld","wa_fld","H0"]

pairs_w0wa = [
  ("omega_m", "omega_b"),
  ("theta_s_100", "omega_b"),("theta_s_100", "omega_m"),
  ("w0_fld", "omega_b"),("w0_fld", "omega_m"),("w0_fld", "theta_s_100"),
  ("wa_fld", "omega_b"),("wa_fld", "omega_m"),("wa_fld", "theta_s_100"),("wa_fld", "w0_fld"),
  ("H0", "omega_b"),("H0", "omega_m"),("H0", "theta_s_100"),("H0", "w0_fld"),("H0", "wa_fld")]

pars_fa = ["omega_b","omega_m","theta_s_100","fa_fld","H0"]

pairs_fa = [
  ("omega_m", "omega_b"),
  ("theta_s_100", "omega_b"),("theta_s_100", "omega_m"),
  ("fa_fld", "omega_b"),("fa_fld", "omega_m"),("fa_fld", "theta_s_100"),
  ("H0", "omega_b"),("H0", "omega_m"),("H0", "theta_s_100"),("H0", "fa_fld")]

pars_lcdm = ["omega_b","omega_m","theta_s_100","H0"]

pairs_lcdm = [
  ("omega_m", "omega_b"),
  ("theta_s_100", "omega_b"),("theta_s_100", "omega_m"),
  ("H0", "omega_b"),("H0", "omega_m"),("H0", "theta_s_100")]

def save_posteriors(chain_sample,pars,pairs,name):
    save_dict= {}
    for param in trange(len(pars), desc="Computing 1D densities"):
        p=pars[param]
        density1D=chain_sample.get1DDensity(p)
        x_1D=density1D.x
        P_1D=density1D.P
        save_dict[f"{name}_{p}_1D_x"]=x_1D
        save_dict[f"{name}_{p}_1D_P"]=P_1D
    for i in trange(len(pairs), desc="Computing 2D densities"):
        p1, p2 = pairs[i]
        density2D = chain_sample.get2DDensity(p2, p1)
        # Extract data
        xvs = density2D.x            # 1D array of x values
        yvs = density2D.y            # 1D array of y values
        p_grid = density2D.P         # 2D array of density
        contour_levels = density2D.getContourLevels()  # e.g. [level_68, level_95]

        # Build a key prefix
        key_prefix = f"{name}_{p1}__{p2}"
        # Store in the dictionary
        save_dict[key_prefix + "_x"] = xvs
        save_dict[key_prefix + "_y"] = yvs
        save_dict[key_prefix + "_p_grid"] = p_grid
        save_dict[key_prefix + "_contour_levels"] = contour_levels
    # -------------------------------------------------
    # Save everything to an .npz file
    # -------------------------------------------------
    output_file = f"output/{name}.npz"
    np.savez(output_file, **save_dict)
    return None
save_posteriors(desi_cmb_w0wa_samples,pars_w0wa,pairs_w0wa,'desi_cmb_w0wa')
save_posteriors(desi_cmb_fa_samples,pars_fa,pairs_fa,'desi_cmb_fa')
save_posteriors(desi_cmb_w0wa_samples,pars_w0wa,pairs_w0wa,'desi_cmb_w0wa')
save_posteriors(desi_cmb_lcdm_samples,pars_lcdm,pairs_lcdm,'desi_cmb_lcdm')

