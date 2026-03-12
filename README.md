# Option Pricing and 3D Volatility Visualizer (In Progress) 

## 1. Overview ## 

This project explores option pricing with core objective to move beyond classical closed-form pricing methods and investigate more realistic models that better reflect the financial market and behavior. I began my implementing the famous Black-Scholes model for European pricing, using its analytical solution. The model is computationally efficient, but relies on perfect market conditions, consequently misaligning with how the real financial market behaves. Most notable incosistant assumptions are the constant volatility or log-normal asset dynamics, which may casue empirical problems like the volatility smile. 

To adress these limitation to Black-Scholes model I extended the project to using Least Square Monte Carlo simulation for  American options, where the Black-Scholes would not work. Further, stochastic volatility modelling for Exotic options - including asian and barrier options - that do not have a analytical solutions, as they are rather more unique than European options in terms of payoffs and pricing. For this section I wanted to focus on Heston model, allowing volatility to evolve as a stochastic process and enabling a better fit. 

## 2. European Options: Call and Put ##

**Black-Scholes Model**

The Black-Scholes model (BS) is a mathematical framework for pricing European call and put options under the risk-netrual pricing measure. It assumes the underlying stock follows the Geometric Brownian Motion (GBM) dynamics with constant volatility and frictionless market condition.

Assumption of the BS model includes: 
- no arbitrage condition
- constant risk free rate
- constant volatility
- log-normal asset price dynamics

Black–Scholes PDE for the option value $V(S,t)$:

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - r V = 0$$

Closed form solution of the BS model is given by: 

$$d_1 = \frac{\ln\left(\frac{S_0}{K}\right) + (r - q + \frac{1}{2}\sigma^2)T}{\sigma \sqrt{T}}$$ , $$d_2 = d_1 - \sigma \sqrt{T}$$

Let $\( N(\cdot) \)$ denote the cumulative distribution function (CDF) of the standard normal distribution.

European Call: 
$C = S_0 e^{-qT} N(d_1) - K e^{-rT} N(d_2)$

European Put: 
$P = K e^{-rT} N(-d_2) - S_0 e^{-qT} N(-d_1)$

Put-Call Parity: 
$C - P = S_0 e^{-qT} - K e^{-rT}$


Under the BS model a stock price $S_T$ follows the GBM dynamics - a countinous time stochastic process with a drift and random component. A stock $S_t$ follows a GBM process given under the risk-netrual measure by:  


$$dS_t = (r - q) S_t dt + \sigma S_t d W_t$$ 


where: 

$r$ = Risk Free Rate 

$q$ = Dividend Yield 

$\sigma$ = Bolatility 

$(r - q) S_t$ = Drift 

$W_t$ = Standard Brownian Motion 



The future possible prices of a stock that follows the GBM model can be modelled by the GBM stochastic differential process:  

$$S_{t+\Delta t} = S_t \cdot \exp\Big((r - q - \frac{1}{2}\sigma^2)\Delta t + \sigma \sqrt{\Delta t} Z_t \Big)$$


**Notes on the model**

(1) Keeping $N$ = 252 (time steps) so that it is more aligned with trading days or any $N$ for $N$ > 30 is standard. 

(2) Having a larger number Monte Carlo simulations will more closly align with the theoritical expected stock price as well as put and call prices - typically $M$ > 50,000 simulations. 

(3) For the model to be more closely aligned with real financial option trade for the parameter $T$, instert the maturity of the option in datetime.date(). The code will then proceed to compute the option maturity in years and use for it further pricing computation. 


## 3. American Options: Put and Call  ## 

**American Options** 

American options are financial derivatives where the holder of the contract may exercise the option at any time up to and  on the option's maturity. This early-exercise flexbility distinguishes American option from European options. 

Under the standard financial assumption that the underlying asset (stock) follows the GBM dynamics under the risk-netrual measure given by: 

$$dS_t = (r - q) S_t dt + \sigma S_t d W_t$$  

where: 

$r$ = Risk Free Rate 

$q$ = Dividend Yield 

$\sigma$ = Volatility 

$(r - q) S_t$ = Drift 

$W_t$ = Standard Brownian Motion

The financial valuation essentially becomes an optimal stopping problem where at each potential exercise date the investor would compare the immediate exercise payoff to the expected value of continuing to hold the option and exercise it at another optimal point in time. 

**An important expection is of an American call on non-dividend stock**, which is never optimal to exercise it early, hence the standard BS model applies. 


**Least Square Monte Carlo (LSMC) Approach**

The approach used for pricing American options is the Least Square Monte Carlo (LSMC), where Monte Carlo simulation is combined with Least Square regression. The core idea of this approach is for Monte Carlo to generate paths for the stock $S_t$ following the GBM dynamics. Following by the backward induction starting at maturity date, where for each discrete exercise date the simulation computes paths that are in the money and computes the countinous value of the option. If immediate exercise payoff is greater, the simulation will mark that path as exercised at that date. Finally, after accounting for all possible early exercises, the option price is computed as the average payoff across pricpaths. 


**Notes on the model** 

(1) It is important to put inside the parameter "option_type" which type it is (call/put) 

(2) The model generates the *estimated* price of the American option contract, along with two graphs: GBM stock simulations and exercise boundary visualisation of the contract. 


## 4. Asian Options ##

**Bermudian Asian Options** 

Asian options - often referred to as average options - are a part of exotic options types. The payoff given to the holder of the contract is based on the average price of the underlying asset for the whole duration of the contract. There are two types of Asian options: American and Bermudian options. American types allow for early exercise and Bermudian exercise only at the maturity of the contract. 

The payoff then is given by: 

$$
\pi(\bar{S}) = \max[\bar{S}-K,0]
$$ 

, where $\bar{S}$ represente the the average stock price over the duration of the contract. 


The average price of the option is calculated in two different ways: the arthimetic average and geometric average. The arthimetic average takes the sum of all the stock prices divided by the number of observations of the stock path. The geometric average is calculated by the integral of the sum of all stock observation prices.  

The artihmetic average: 

$$
\bar{S} = \frac{1}{n}\sum_{i=1}^{n} S_{t_i}
$$

The geometric average is given by: 

$$
G = \left(\prod_{i=1}^{n} S_{t_i}\right)^{\frac{1}{n}}
$$


**Asian Options Prices**









