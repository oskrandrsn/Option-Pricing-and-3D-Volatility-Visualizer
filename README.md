# Option-Pricing
## 1. European Options: Call and Put ##

Under the Black-Scholes model a stock price $S_T$ follows the Geometric Brownian Motion (GBM) - a countinous time stochastic process with a drift and random component. A stock $S_t$ follows a GBM process given under the risk-netrual measure by:  $$dS_t = r S_t dt + \sigma S_t d W_t$$ 

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
