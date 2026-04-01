"""
visualization.py
Black-Scholes Greeks & Price Visualization
Abhilash Gangineni | MS Finance @ UNT
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from black_scholes import BlackScholesEngine

# ─────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────
K     = 100    # Strike price
T     = 1.0    # Time to expiry (years)
r     = 0.05   # Risk-free rate
sigma = 0.20   # Volatility

S_range = np.linspace(60, 140, 300)

# ─────────────────────────────────────────────
# Compute values across stock price range
# ─────────────────────────────────────────────
call_prices, put_prices = [], []
deltas_call, deltas_put = [], []
gammas = []
thetas_call, thetas_put = [], []
vegas  = []
rhos_call, rhos_put = [], []

for S in S_range:
    bs = BlackScholesEngine(S=S, K=K, T=T, r=r, sigma=sigma)
    call_prices.append(bs.call_price())
    put_prices.append(bs.put_price())
    g = bs.greeks()
    deltas_call.append(g['call']['delta'])
    deltas_put.append(g['put']['delta'])
    gammas.append(g['call']['gamma'])
    thetas_call.append(g['call']['theta'])
    thetas_put.append(g['put']['theta'])
    vegas.append(g['call']['vega'])
    rhos_call.append(g['call']['rho'])
    rhos_put.append(g['put']['rho'])

# ─────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10))
fig.suptitle(
    f'Black-Scholes Pricing & Greeks  |  K={K}, T={T}yr, r={r*100:.0f}%, σ={sigma*100:.0f}%',
    fontsize=14, fontweight='bold', y=1.01
)

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

CALL_COLOR    = '#1a4fa0'
PUT_COLOR     = '#c0392b'
NEUTRAL_COLOR = '#0d7a6e'

def style_ax(ax, title):
    ax.set_title(title, fontweight='bold', fontsize=11)
    ax.axvline(x=K, color='gray', linewidth=1, linestyle=':', alpha=0.6, label=f'ATM K={K}')
    ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.25)
    ax.set_xlabel('Stock Price (S)', fontsize=9)
    ax.grid(True, alpha=0.18)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(fontsize=8)

# 1. Option Prices
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(S_range, call_prices, color=CALL_COLOR,    linewidth=2, label='Call Price')
ax1.plot(S_range, put_prices,  color=PUT_COLOR,     linewidth=2, linestyle='--', label='Put Price')
ax1.set_ylabel('Option Price ($)')
style_ax(ax1, 'Option Price')

# 2. Delta
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(S_range, deltas_call, color=CALL_COLOR, linewidth=2, label='Call Delta')
ax2.plot(S_range, deltas_put,  color=PUT_COLOR,  linewidth=2, linestyle='--', label='Put Delta')
ax2.set_ylabel('Delta')
style_ax(ax2, 'Delta')

# 3. Gamma
ax3 = fig.add_subplot(gs[0, 2])
ax3.plot(S_range, gammas, color=NEUTRAL_COLOR, linewidth=2, label='Gamma')
ax3.set_ylabel('Gamma')
style_ax(ax3, 'Gamma')

# 4. Theta
ax4 = fig.add_subplot(gs[1, 0])
ax4.plot(S_range, thetas_call, color=CALL_COLOR, linewidth=2, label='Call Theta')
ax4.plot(S_range, thetas_put,  color=PUT_COLOR,  linewidth=2, linestyle='--', label='Put Theta')
ax4.set_ylabel('Theta')
style_ax(ax4, 'Theta (Time Decay)')

# 5. Vega
ax5 = fig.add_subplot(gs[1, 1])
ax5.plot(S_range, vegas, color=NEUTRAL_COLOR, linewidth=2, label='Vega')
ax5.set_ylabel('Vega')
style_ax(ax5, 'Vega (Volatility Sensitivity)')

# 6. Rho
ax6 = fig.add_subplot(gs[1, 2])
ax6.plot(S_range, rhos_call, color=CALL_COLOR, linewidth=2, label='Call Rho')
ax6.plot(S_range, rhos_put,  color=PUT_COLOR,  linewidth=2, linestyle='--', label='Put Rho')
ax6.set_ylabel('Rho')
style_ax(ax6, 'Rho (Rate Sensitivity)')

plt.savefig('greeks_visualization.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: greeks_visualization.png")
