# ==========================================================
# Packages Importation
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.gridspec import GridSpec
from matplotlib.cm import ScalarMappable
from scipy.stats import gaussian_kde
import math

# ==========================================================
# Model's Parameters 
# ==========================================================

S0 = 100
K = 140
r = 0.05
q = 0
sigma = 0.40

Number_Time_Steps = 256
Number_Paths = 5000

T = 250/365
dt = T / Number_Time_Steps

rng = np.random.default_rng(5000) 

# ==========================================================
# Stock Dynamics under The Geometric Brownian Motion
# ==========================================================

paths = np.zeros((Number_Paths, Number_Time_Steps + 1))
paths[:, 0] = S0
for i in range(1, Number_Time_Steps + 1):
    Z = rng.standard_normal(Number_Paths)
    paths[:, i] = paths[:, i-1] * np.exp((r - q - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

Final_Prices = paths[:, -1]
norm = Normalize(vmin=min(Final_Prices), vmax=max(Final_Prices))
cmap = plt.get_cmap("magma")  
colors = cmap(norm(Final_Prices))

fig = plt.figure(figsize=(12, 7), dpi=150)
gs = GridSpec(1, 2, width_ratios=[4, 1], wspace=0.05)

ax0 = fig.add_subplot(gs[0])
for i in range(Number_Paths):
    ax0.plot(paths[i], color=colors[i], lw=1.2, alpha=0.6)
ax0.set_xlabel("Time Step")
ax0.set_ylabel("Stock Price")
ax0.set_title("Risk-Neutral Simulation of Expected Stock Prices $E[S_t]$ given GBM Dynamics")
ax0.grid(True, linestyle='--', alpha=0.4)  

ax1 = fig.add_subplot(gs[1], sharey=ax0)
sorted_idx = np.argsort(Final_Prices)
sorted_prices = Final_Prices[sorted_idx]
sorted_colors = colors[sorted_idx]

bins = np.linspace(min(Final_Prices), max(Final_Prices), 20)
for i in range(len(bins)-1):
    mask = (sorted_prices >= bins[i]) & (sorted_prices < bins[i+1])
    count = np.sum(mask)
    if count > 0:
        color = np.mean(sorted_colors[mask], axis=0)
        ax1.barh((bins[i]+bins[i+1])/2, count, height=bins[i+1]-bins[i], color=color, edgecolor='k', alpha=0.8)

kde = gaussian_kde(Final_Prices)
y_vals = np.linspace(min(Final_Prices), max(Final_Prices), 300)
density = kde(y_vals) * Number_Paths * (bins[1]-bins[0])  
ax1.plot(density, y_vals, color='black', lw=2) 

ax1.set_xlabel("Frequency")
ax1.yaxis.tick_right()
ax1.yaxis.set_label_position("right")
ax1.grid(True, linestyle='--', alpha=0.4)  

sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=[ax0, ax1], orientation='vertical', fraction=0.03, pad=0.02)
cbar.set_label("")

# ==========================================================
# Black-Scholes Model for European Options with Greeks 
# ==========================================================

from scipy.stats import norm as scipy_norm
_norm_cdf = scipy_norm.cdf
_norm_pdf = scipy_norm.pdf

def _d1_d2(S0, K, r, q, sigma, T):
    sqrtT = math.sqrt(T)
    d1 = (math.log(S0 / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT
    return d1, d2

def bs_call_price(S0, K, r, q, sigma, T):
    d1, d2 = _d1_d2(S0, K, r, q, sigma, T)
    return S0 * math.exp(-q*T) * _norm_cdf(d1) - K * math.exp(-r*T) * _norm_cdf(d2)

def bs_put_price(S0, K, r, q, sigma, T):
    d1, d2 = _d1_d2(S0, K, r, q, sigma, T)
    return K * math.exp(-r*T) * _norm_cdf(-d2) - S0 * math.exp(-q*T) * _norm_cdf(-d1)

def bs_delta(S0, K, r, q, sigma, T, option='call'):
    d1, _ = _d1_d2(S0, K, r, q, sigma, T)
    if option == 'call':
        return math.exp(-q*T) * _norm_cdf(d1)
    else:
        return math.exp(-q*T) * (_norm_cdf(d1) - 1)

def bs_gamma(S0, K, r, q, sigma, T):
    d1, _ = _d1_d2(S0, K, r, q, sigma, T)
    return math.exp(-q*T) * _norm_pdf(d1) / (S0 * sigma * math.sqrt(T))

def bs_vega(S0, K, r, q, sigma, T):
    d1, _ = _d1_d2(S0, K, r, q, sigma, T)
    return S0 * math.exp(-q*T) * _norm_pdf(d1) * math.sqrt(T)

def bs_theta(S0, K, r, q, sigma, T, option='call'):
    d1, d2 = _d1_d2(S0, K, r, q, sigma, T)
    term1 = -(S0 * _norm_pdf(d1) * sigma * math.exp(-q*T)) / (2 * math.sqrt(T))

    if option == 'call':
        return (term1
                - r * K * math.exp(-r*T) * _norm_cdf(d2)
                + q * S0 * math.exp(-q*T) * _norm_cdf(d1))
    else:
        return (term1
                + r * K * math.exp(-r*T) * _norm_cdf(-d2)
                - q * S0 * math.exp(-q*T) * _norm_cdf(-d1))
    

# ==========================================================
# Monte Carlo Simulation for European Option Prices 
# ==========================================================

payoff_call = np.maximum(Final_Prices - K, 0.0)
payoff_put = np.maximum(K - Final_Prices, 0.0)

mc_call_price = math.exp(-r*T) * payoff_call.mean()
mc_put_price = math.exp(-r*T) * payoff_put.mean()

se_call = math.exp(-r*T) * payoff_call.std(ddof=1) / math.sqrt(Number_Paths)
se_put  = math.exp(-r*T) * payoff_put.std(ddof=1) / math.sqrt(Number_Paths)

# ==========================================================
# Results 
# ==========================================================

print("Monte Carlo Final Price:", np.mean(Final_Prices))
print("Theoretical Risk-Neutral Mean", S0 * np.exp((r - q) * T))
print()
print("Black-Scholes Call Price:", bs_call_price(S0, K, r, q, sigma, T))
print("Monte Carlo Call Price:", mc_call_price, "SE:", se_call)
print()
print("Black-Scholes Put Price:", bs_put_price(S0, K, r, q, sigma, T))
print("Monte Carlo Put Price:", mc_put_price, "SE:", se_put)
print()
print("Delta (call):", bs_delta(S0, K, r, q, sigma, T, 'call'))
print("Gamma:", bs_gamma(S0, K, r, q, sigma, T))
print("Vega:", bs_vega(S0, K, r, q, sigma, T))
print("Theta (call, per year):", bs_theta(S0, K, r, q, sigma, T, 'call'))
print("Theta (call, per day):", bs_theta(S0, K, r, q, sigma, T, 'call') / 365)
plt.show()