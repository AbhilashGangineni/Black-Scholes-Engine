"""
Black-Scholes Engine — Greeks Visualization
Author: Abhilash Gangineni
GitHub: github.com/AbhilashGangineni/Black-Scholes-Engine

Addresses feedback from Jonathan Schachter PhD:
- T treated as a parameter (not fixed at 1 year)
- Greeks analyzed near expiry across ATM, ITM, OTM
- Volatility surface and time decay plots
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from black_scholes import black_scholes_price, calculate_greeks

# ── Style ────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'monospace',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'figure.facecolor': 'white',
})

S = 100.0   # Stock price
K = 100.0   # Strike price
r = 0.05    # Risk-free rate
sigma = 0.20  # Volatility

# ── FIGURE 1: Greeks vs Time (Jonathan's main point) ─────────
print("Generating Figure 1: Greeks vs Time to Expiry...")

T_range = np.linspace(0.01, 2.0, 300)  # 3 days to 2 years

# Three moneyness scenarios
scenarios = {
    'OTM  (S=90, K=100)': {'S': 90,  'color': 'black',  'ls': '--'},
    'ATM  (S=100, K=100)': {'S': 100, 'color': 'black',  'ls': '-'},
    'ITM  (S=110, K=100)': {'S': 110, 'color': 'black',  'ls': ':'},
}

fig1, axes = plt.subplots(2, 3, figsize=(15, 9))
fig1.suptitle(
    'Black-Scholes Greeks vs Time to Expiry\n'
    'Across ATM / ITM / OTM  |  sigma=20%  |  r=5%',
    fontsize=14, fontweight='bold', y=1.02
)

greek_names = ['delta', 'gamma', 'theta', 'vega', 'rho']
greek_labels = ['Delta', 'Gamma', 'Theta (per day)', 'Vega', 'Rho']
ax_flat = axes.flatten()

for idx, (greek, label) in enumerate(zip(greek_names, greek_labels)):
    ax = ax_flat[idx]
    for name, params in scenarios.items():
        values = []
        for T in T_range:
            g = calculate_greeks(params['S'], K, T, r, sigma, 'call')
            values.append(g[greek])
        ax.plot(T_range, values,
                color=params['color'],
                linestyle=params['ls'],
                linewidth=1.8,
                label=name)
    ax.set_title(label, fontweight='bold', fontsize=11)
    ax.set_xlabel('Time to Expiry (years)')
    ax.set_ylabel(label)
    if idx == 0:
        ax.legend(fontsize=8, loc='upper left')
    ax.axvline(x=0.25, color='gray', alpha=0.4, linewidth=0.8, linestyle='-.')
    ax.axvline(x=1.0,  color='gray', alpha=0.4, linewidth=0.8, linestyle='-.')

# Use last panel for near-expiry delta closeup (Jonathan's key point)
ax = ax_flat[5]
T_near = np.linspace(0.001, 0.15, 500)  # 0 to ~55 days
for name, params in scenarios.items():
    deltas = [calculate_greeks(params['S'], K, T, r, sigma, 'call')['delta']
              for T in T_near]
    ax.plot(T_near * 365, deltas,
            color=params['color'],
            linestyle=params['ls'],
            linewidth=2.0,
            label=name)
ax.set_title('Delta Near Expiry (days)', fontweight='bold', fontsize=11)
ax.set_xlabel('Days to Expiry')
ax.set_ylabel('Delta')
ax.legend(fontsize=8)
ax.set_xlim(0, 55)
ax.axhline(y=0.5, color='gray', alpha=0.4, linewidth=0.8)

plt.tight_layout()
plt.savefig('greeks_vs_time.png', dpi=150, bbox_inches='tight')
print("Saved: greeks_vs_time.png")
plt.close()

# ── FIGURE 2: Delta Heatmap (Moneyness x Time) ───────────────
print("Generating Figure 2: Delta Heatmap...")

S_range = np.linspace(70, 130, 60)
T_range2 = np.linspace(0.01, 1.0, 60)
S_grid, T_grid = np.meshgrid(S_range, T_range2)

delta_grid = np.vectorize(
    lambda s, t: calculate_greeks(s, K, t, r, sigma, 'call')['delta']
)(S_grid, T_grid)

fig2, ax = plt.subplots(figsize=(10, 6))
im = ax.contourf(S_grid, T_grid, delta_grid, levels=20, cmap='Greys')
plt.colorbar(im, ax=ax, label='Delta')
ax.contour(S_grid, T_grid, delta_grid,
           levels=[0.25, 0.5, 0.75],
           colors='black', linewidths=1.2)
ax.axvline(x=K, color='black', linewidth=1.5,
           linestyle='--', label=f'Strike K={K}')
ax.set_xlabel('Stock Price (S)', fontsize=12)
ax.set_ylabel('Time to Expiry (years)', fontsize=12)
ax.set_title(
    'Delta Heatmap — Moneyness vs Time to Expiry\n'
    'Contour lines at Delta = 0.25, 0.50, 0.75',
    fontsize=13, fontweight='bold'
)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('delta_heatmap.png', dpi=150, bbox_inches='tight')
print("Saved: delta_heatmap.png")
plt.close()

# ── FIGURE 3: Option Price vs Volatility ─────────────────────
print("Generating Figure 3: Volatility Sensitivity...")

sigma_range = np.linspace(0.05, 0.80, 200)
T_vals = [0.25, 0.5, 1.0, 2.0]

fig3, ax = plt.subplots(figsize=(10, 6))
linestyles = ['-', '--', '-.', ':']
for T_val, ls in zip(T_vals, linestyles):
    prices = [black_scholes_price(S, K, T_val, r, s, 'call')
              for s in sigma_range]
    label = f'T = {int(T_val*12)} months'
    ax.plot(sigma_range * 100, prices,
            color='black', linestyle=ls,
            linewidth=2.0, label=label)

ax.axvline(x=20, color='gray', alpha=0.5, linewidth=1,
           linestyle='-.', label='sigma=20% (base case)')
ax.set_xlabel('Volatility sigma (%)', fontsize=12)
ax.set_ylabel('Call Option Price ($)', fontsize=12)
ax.set_title(
    'Option Price vs Volatility — Across Different Time Horizons\n'
    'S=$100, K=$100, r=5%',
    fontsize=13, fontweight='bold'
)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('volatility_sensitivity.png', dpi=150, bbox_inches='tight')
print("Saved: volatility_sensitivity.png")
plt.close()

print("\n" + "="*55)
print("   VISUALIZATION COMPLETE")
print("   3 charts generated:")
print("   1. greeks_vs_time.png")
print("   2. delta_heatmap.png")
print("   3. volatility_sensitivity.png")
print("="*55)
