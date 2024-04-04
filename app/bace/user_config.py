# Example configuration file
import scipy.stats
import numpy as np

author       = 'Jiayue Zhang' # Your name here
size_thetas  = 2500                      # Size of sample drawn from prior distribuion over preference parameters.
answers      = [0, 1]                    # All possible answers that can be observed.
max_opt_time = 5                         # Stop Bayesian Optimization process after max_opt_time and return best design.


# Configuration Dictionary for Bayesian Optimization
# See https://github.com/ARM-software/mango#6-optional-configurations for details
# Possible to add constraints and early stopping rules here.
conf_dict = dict(
    domain_size    = 5000,
    initial_random = 1,
    num_iteration  = 20
)

# Preference parameters (theta_params)
# Dictionary where each preference parameter has a prior distribution specified by a scipy.stats distribution
# All entries must have a .rvs() and .log_pdf() method
theta_params = dict(
    beta    = scipy.stats.norm(loc=1, scale=0.5),
    gamma    = scipy.stats.beta(20,0.5),
    mu       = scipy.stats.norm(loc=0, scale=100)
)

# Design parameters (design_params)
# Dictionary where each parameter specifies what designs can be chosen for a characteristic
# See https://github.com/ARM-software/mango#DomainSpace for details on specifying designs
design_params = dict(
    price_a   = scipy.stats.uniform(300, 2000),
    price_b   = scipy.stats.uniform(300, 2000),
    repay_a   = scipy.stats.uniform(10, 100),
    repay_b   = scipy.stats.uniform(10, 100),
    type_a    = ['Now', 'Tomorrow'],
    type_b    = ['Now', 'Tomorrow']
)

# Specify likelihood function
# Returns Prob(answer | theta, design) for each answer in answers
def likelihood_pdf(answer, thetas,
                   # All keys in design_params here
                   price_a, price_b,
                   repay_a, repay_b,
                   type_a, type_b):

    eps = 1e-10


    U_a = (-price_a - thetas['beta']*thetas['delta']/(1-thetas['delta']) * (repay_a - thetas['mu'])) * (1+thetas['delta']*(type_a == 'Tomorrow')) + (price_a*(1-thetas['beta'])*thetas['delta']*(type_a == 'Tomorrow'))
    U_b = (-price_b - thetas['beta']*thetas['delta']/(1-thetas['delta']) * (repay_b - thetas['mu'])) * (1+thetas['delta']*(type_b == 'Tomorrow')) + (price_b*(1-thetas['beta'])*thetas['delta']*(type_b == 'Tomorrow'))
    base_utility_diff = U_b - U_a

    # Choose higher utility option with probability p. Choose randomly otherwise.
    likelihood = 1 / (1 + np.exp(-1  * base_utility_diff))

    likelihood[likelihood < eps] = eps
    likelihood[likelihood > (1 - eps)] = 1 - eps

    if str(answer) == '1':
        return likelihood
    elif str(answer) == '0':
        return 1 - likelihood
    else:
        print("Warning: `answer` input to likelihood_pdf is not an element in `answers`.")
        print(f"Answer received: {str(answer)}.")
        return 1/2
