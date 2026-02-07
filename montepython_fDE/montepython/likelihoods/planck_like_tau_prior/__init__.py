from montepython.likelihood_class import Likelihood_prior
    
class planck_like_tau_prior(Likelihood_prior):

    # initialisation of the class is done within the parent Likelihood_prior. For
    # this case, it does not differ, actually, from the __init__ method in
    # Likelihood class.
    def loglkl(self, cosmo, data):
        tau_reio = data.mcmc_parameters['tau_reio']['current']*data.mcmc_parameters['tau_reio']['scale']
        loglkl = -0.5 * (tau_reio - self.mean_tau_reio) ** 2 / (self.sigma_tau_reio ** 2)
        return loglkl
