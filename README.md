# Option Pricing and 3D Volatility Visualizer (In Progress) 
**By:** Oskar Andersen 


## Content ##

**1. Overview** 

**2. European Options: Call and Put**

**3. Exotic Options**

**4. Asian and Barrier Options**

**5. Volatility Surface Visualizor 3D** 


## 1. Overview ## 

This is a very first project implemented in Python by me with focus on option pricing, as I am interested in derivative and asset pricing. I wanted to challenge myself and implement something interesting within my field of study which is quantitative finance and asset pricing. 

This project explores option pricing with core objective to move beyond classical closed-form pricing methods and investigate more realistic models that better reflect the financial market and behavior. I began my implementing the famous Black-Scholes model for European pricing, using its analytical solution. The model is computationally efficient, but relies on perfect market conditions, consequently misaligning with how the real financial market behaves. Most notable incosistant assumptions are the constant volatility or log-normal asset dynamics, which may casue empirical problems like the volatility smile. 

To adress these limitation to Black-Scholes model I extended the project to using stochastic volatility modelling for Exotic options, that do not have a analytical solutions, as they are rather more unique than European options in terms of payoffs and pricing. For this section I wanted to focus on Heston model, allowing volatility to evolve as a stochastic process and enabling a better fit. 

As a final model for option pricing would be Asian and Barrier options with central idea on Monte Carlo simulations, before implementing a 3D volatility surface visualizer for analysis of implied volatility varies across strike prices and maturities. 


## 2. European Options: Call and Put ##

Under the Black-Scholes model a stock price $S_T$ follows the Geometric Brownian Motion (GBM) - a countinous time stochastic process with a drift and random component. A stock $S_t$ follows a GBM process given under the risk-netrual measure by:  

$$dS_t = r S_t dt + \sigma S_t d W_t$$ 

where: 

$r$ = risk free rate 

$r S_t$ = drift 

$\sigma S_t$ = volatility/random component

$W_t$ = standard Brownian Motion 



The future possible prices of a stock that follows the GBM model can be modelled by the GBM stochastic differential process:  

$$
S_{t+\Delta t} = S_t \cdot \exp\Big((r - q - \frac{1}{2}\sigma^2)\Delta t + \sigma \sqrt{\Delta t} Z_t \Big)
$$

The formula above is used to simulate possible stochastic paths of stock prices under the risk neutral measure to ensure that discounted prices follow a martingale approach. 

Changing the parameters will generate all the possible paths of the stock starting from an initial stock price at time t=0. The right-hand side of the graph shows the empirical distribution of simulated terminal stock prices $S_T$. 

Note:

(1) Keeping 252 time steps so that it is more aligned with trading days. 
 
(2) Having a larger number of paths simulated will more closly align with the theoritical expected stock price as well as put and call prices (typically > 50,000 simulations is good enough)

(3) Option maturity is measured in $T$ years. If an option matures in 120 days from now then write code 120/365, which let's Python calculate the option maturing in 120 days with 256 time steps. 


**Model Parameters**

- $S_0$ — Initial Stock Price at Time $t=0$  

- $K$ = Strike Price

- $r$ — Risk Free Rate 

- $q$ = Dividend 

- $\sigma$ — Volatility (standard deviation of returns)  

- $N_{\text{Time}}$ — Number of time steps  

- $N_{\text{Paths}}$ — Number of simulated paths  

- $T$ — Option's Maturity 
