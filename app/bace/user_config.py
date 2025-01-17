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
    vbar    = scipy.stats.norm(loc=5000, scale=1000),
    k       = scipy.stats.norm(loc=10000, scale=10000)
)

# Design parameters (design_params)
# Dictionary where each parameter specifies what designs can be chosen for a characteristic
# See https://github.com/ARM-software/mango#DomainSpace for details on specifying designs
design_params = dict(
    deposit_a   = scipy.stats.uniform(0, 2000),
    deposit_b   = scipy.stats.uniform(0, 2000),
    repay_a   = scipy.stats.uniform(10, 300),
    repay_b   = scipy.stats.uniform(10, 300)
)

# Specify likelihood function
# Returns Prob(answer | theta, design) for each answer in answers
def likelihood_pdf(answer, thetas,
                   # All keys in design_params here
                   deposit_a, deposit_b,
                   repay_a, repay_b):

    eps = 1e-10

    p_a = repay_a * 4 + 24*362
    p_b = repay_b * 4 + 24*362
                       

    # Version 1                   
    U_a = -deposit_a + 0.5/thetas['vbar']*( (thetas['vbar']-p_a)**2 + (thetas['k']/p_a*thetas['vbar'] - 0.5*(2*p_a-thetas['k']) * thetas['k'] / thetas['vbar'] )**2 )
    U_b = -deposit_b + 0.5/thetas['vbar']*( (thetas['vbar']-p_b)**2 + (thetas['k']/p_b*thetas['vbar'] - 0.5*(2*p_b-thetas['k']) * thetas['k'] / thetas['vbar'])**2 )
                       
    # Version 2
    #Ua1 = -deposit_a + 0.5/thetas['vbar']*( (thetas['vbar']-p_a)**2 + (thetas['k']/p_a*thetas['vbar'] - 0.5*(2*p_a-thetas['k']) * thetas['k'] / thetas['vbar'] )**2 )
    #Ua2 = -deposit_a + 0.5/thetas['vbar']*((thetas['vbar']-p_a)**2 + (thetas['vbar']-0.5*p_a^2/thetas['vbar'])**2 )
    #U_a = Ua1*(1+1/(1+np.exp(-20*(thetas['k']-p_a)))) + Ua2/(1+np.exp(-20*(thetas['k']-p_a)))
    
    #Ub1 = -deposit_b + 0.5/thetas['vbar']*( (thetas['vbar']-p_b)**2 + (thetas['k']/p_b*thetas['vbar'] - 0.5*(2*p_b-thetas['k']) * thetas['k'] / thetas['vbar'])**2 )
    #Ub2 = -deposit_b + 0.5/thetas['vbar']*((thetas['vbar']-p_b)**2 + (thetas['vbar']-0.5*p_b^2/thetas['vbar'])**2 )
    #U_b = Ub1*(1+1/(1+np.exp(-20*(thetas['k']-p_b)))) + Ub2/(1+np.exp(-20*(thetas['k']-p_b)))
                 
                       

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
