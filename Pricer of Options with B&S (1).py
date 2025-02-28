"Pricer of Options thanks to the Black-Scholes Formula with their Greeks"

import yfinance as yf
from scipy.stats import norm
import numpy as np 

apple_ticker = yf.Ticker("AAPL")
df = apple_ticker.history(period="1y") 
print(df.head())

class actif:
    
    ''' We develop a class of actif and several methods in order to have the price of a call and a put
        d1 and d2 are variables that are used in the Black-Scholes Formulas
        Then, we calculate the greeks of the options according to the derivatives for B&S
        To calcultate the volatily, we used the logaritmic return 
    '''
        
    def __init__(self,price,strike,time,risk_free):
        self.price=price
        self.strike=strike
        self.time=time 
        self.risk_free=risk_free
    
    def info(self):
        print(self.price,self.strike,self.time)
        
    def volatility(self):
        log_returns = np.log(df['High'] / df['High'].shift(1))
        vol = np.std(log_returns)  
        vol_annualized = vol * np.sqrt(252) 
        return vol_annualized
    
    def d1(self):
        vol = self.volatility()
        return (np.log(self.price / self.strike) + (self.risk_free + 0.5 * vol**2) * self.time) / (vol * np.sqrt(self.time))

    def d2(self):
        return self.d1() - self.volatility() * np.sqrt(self.time)
    
    def call(self):
        d1_value = self.d1()
        d2_value = self.d2()
        C = (self.price * norm.cdf(d1_value) - 
             self.strike * np.exp(-self.risk_free * self.time) * norm.cdf(d2_value))
        return C
    
    def put(self):
        d1_value = self.d1()
        d2_value = self.d2()
        P = (self.strike * np.exp(-self.risk_free * self.time) * norm.cdf(-d2_value) - 
             self.price * norm.cdf(-d1_value))
        return P
        
    def delta(self, option_type='call'):
        d1_value = self.d1()
        if option_type == 'call':
            return norm.cdf(d1_value)
        elif option_type == 'put':
            return norm.cdf(d1_value) - 1

    def gamma(self):
        vol = self.volatility()
        d1_value = self.d1()
        return norm.pdf(d1_value) / (self.price * vol * np.sqrt(self.time))

    def vega(self):
        d1_value = self.d1()
        return self.price * norm.pdf(d1_value) * np.sqrt(self.time)

    def theta(self, option_type='call'):
        vol = self.volatility()
        d1_value = self.d1()
        d2_value = self.d2()
        term1 = -(self.price * norm.pdf(d1_value) * vol) / (2 * np.sqrt(self.time))
        if option_type == 'call':
            term2 = self.risk_free * self.strike * np.exp(-self.risk_free * self.time) * norm.cdf(d2_value)
            return term1 - term2
        elif option_type == 'put':
            term2 = self.risk_free * self.strike * np.exp(-self.risk_free * self.time) * norm.cdf(-d2_value)
            return term1 + term2

    def rho(self, option_type='call'):
        d2_value = self.d2()
        if option_type == 'call':
            return self.strike * self.time * np.exp(-self.risk_free * self.time) * norm.cdf(d2_value)
        elif option_type == 'put':
            return -self.strike * self.time * np.exp(-self.risk_free * self.time) * norm.cdf(-d2_value)*


apple = actif(df['High'].iloc[1], df['High'].mean(), 1, 0.01)

# Printing option prices
print("Call Price:", apple.call())
print("Put Price:", apple.put())

# Printing Greeks
print("Delta (Call):", apple.delta(option_type='call'))
print("Delta (Put):", apple.delta(option_type='put'))
print("Gamma:", apple.gamma())
print("Vega:", apple.vega())
print("Theta (Call):", apple.theta(option_type='call'))
print("Theta (Put):", apple.theta(option_type='put'))
print("Rho (Call):", apple.rho(option_type='call'))
print("Rho (Put):", apple.rho(option_type='put'))

        
