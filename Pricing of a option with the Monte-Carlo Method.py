import numpy as np
import matplotlib.pyplot as plt

"""we are pricing a options thanks to the Monte-Carlo Method that consist in simulated
overtime the varitions of the price of the underlying asset
"""

def monte_carlo_option_pricing_and_simulation(S0, K, T, r, sigma, num_simulations=1000, option_type="call", num_trajectories=10000, time_steps=100):
    """
    
    
    S0 : Spot price
    K : Strike
    T : Maturity  (in years)
    r : risk-free rate
    sigma : Volatility
    num_simulations : Number of simulation
    option_type : "call" ou "put"
    num_trajectories : number of trajectories
    time_steps  number of time steps
    """

    # we generate random numbers that follow a normal random variable
    Z = np.random.standard_normal(num_simulations)
    
    # we calculate the price at matury and so the payoff of the option
    S_T = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
    else:
        payoffs = np.maximum(K - S_T, 0)
    
    #we calculate the price of the options 
    option_price = np.exp(-r * T) * np.mean(payoffs)

    #we now plot each trajectories
    dt = T / time_steps
    trajectories = np.zeros((time_steps + 1, num_trajectories))
    trajectories[0] = S0

    for t in range(1, time_steps + 1):
        Z = np.random.standard_normal(num_trajectories)
        trajectories[t] = trajectories[t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
 
    time = np.linspace(0, T, time_steps + 1)
    plt.figure(figsize=(10, 6))
    for i in range(num_trajectories):
        plt.plot(time, trajectories[:, i], lw=1.5)
    plt.grid()
    plt.show()


    return option_price

print("premium of the option =",monte_carlo_option_pricing_and_simulation(100, 110,1, 0.05, 0.02  , num_simulations=1000, option_type="call", num_trajectories=10000, time_steps=100))
