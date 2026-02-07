import numpy as np
from montepython.likelihood_class import Likelihood_prior

class w0wa_prior(Likelihood_prior):
    def loglkl(self, cosmo, data):
        w0 = data.mcmc_parameters['w0_fld']['current']
        wa = data.mcmc_parameters['wa_fld']['current']
        # hard cut: require w0 + wa < 0
        if (w0 + wa) >= self.cutoff:
            return -1e30  # effectively -inf for MCMC
        return 0.0
