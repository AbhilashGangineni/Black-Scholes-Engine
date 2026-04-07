# Black-Scholes Options Pricing Engine

A production-quality Python quantitative finance library implementing the Black-Scholes model from first principles — covering closed-form pricing, all five Greeks, implied volatility extraction via Brent's method, Monte Carlo simulation, and advanced Greeks visualization across time and moneyness.

Part of my **Quant Finance Project Series** — building toward a full quantitative research portfolio.

---

## Project Structure

```
Black-Scholes-Engine/
├── black_scholes.py            # Core engine — BS pricing, all 5 Greeks, IV, Monte Carlo
├── visualization.py            # Greeks visualization across stock price range
├── visualization_greeks.py     # Advanced — Greeks vs time, moneyness heatmap, vol surface
├── requirements.txt            # Dependencies
├── README.md
└── examples/
    └── basic_usage.py          # 7 worked examples with real output
```

---

## What This Engine Computes

### 1. Option Pricing (Closed-Form Black-Scholes)

For a European call option:

```
C = S * N(d1) - K * e^(-rT) * N(d2)

d1 = [ln(S/K) + (r + sigma^2/2) * T] / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)
```

Where:
- `S` = Current stock price
- `K` = Strike price
- `T` = Time to expiration (years)
- `r` = Risk-free interest rate
- `sigma` = Volatility
- `N()` = Cumulative standard normal distribution

### 2. All 5 Greeks (Analytical)

| Greek | Measures | Value (ATM, T=1yr, sigma=20%) |
|-------|----------|-------------------------------|
| Delta | Price sensitivity to stock price | 0.6368 |
| Gamma | Rate of change of Delta | 0.0188 |
| Theta | Time decay per day | -0.0176 |
| Vega  | Sensitivity to volatility | 0.3752 |
| Rho   | Sensitivity to interest rate | 0.5323 |

### 3. Implied Volatility Extraction

Works **backwards** from a market price to extract the implied volatility using **Brent's root-finding method** — numerical optimization that converges to the exact solution.

### 4. Monte Carlo Simulation

Simulates **10,000 stochastic price paths** using Geometric Brownian Motion and averages the discounted payoffs to produce an independent price estimate.

---

## Sample Output

```
QUANT PROJECT 1 — BLACK-SCHOLES ENGINE
Abhilash Gangineni | MS Finance @ UNT
====================================================
   BLACK-SCHOLES PRICING SUMMARY
====================================================
   Stock Price  (S):    $100.00
   Strike Price (K):    $100.00
   Time to Expiry (T):  1.00 years
   Risk-Free Rate (r):  5.0%
   Volatility (sigma):  20.0%
----------------------------------------------------
   Call Price:          $10.4506
   Put Price:           $5.5735
----------------------------------------------------
   GREEKS (Call)
   Delta                0.636831
   Gamma                0.018762
   Theta               -0.017573
   Vega                 0.375240
   Rho                  0.532325
----------------------------------------------------
   GREEKS (Put)
   Delta               -0.363169
   Gamma                0.018762
   Theta               -0.004542
   Vega                 0.375240
   Rho                 -0.418905
====================================================
--- IMPLIED VOLATILITY ---
Market Call Price:   $10.4506
Extracted IV:        20.00%  (exact match)

--- MONTE CARLO SIMULATION (10,000 paths) ---
MC Call Price:       $10.2211
BS Call Price:       $10.4506
Difference:          $0.2295
95% CI:              ($9.94, $10.51)
```

---

## Usage Examples

### Basic Pricing

```python
from black_scholes import BlackScholes

bs = BlackScholes(S=100, K=100, T=1.0, r=0.05, sigma=0.20)

print(bs.call_price())   # 10.4506
print(bs.put_price())    # 5.5735
print(bs.all_greeks('call'))
```

### Implied Volatility

```python
from black_scholes import implied_volatility

iv = implied_volatility(market_price=10.4506, S=100, K=100, T=1.0, r=0.05, option_type='call')
print(f"IV: {iv*100:.2f}%")   # 20.00%
```

### Monte Carlo

```python
from black_scholes import monte_carlo_price

price = monte_carlo_price(S=100, K=100, T=1.0, r=0.05, sigma=0.20, option_type='call', n_simulations=10000)
print(f"MC Price: ${price:.4f}")   # ~$10.22
```

### Run All Examples

```python
python examples/basic_usage.py
```

---

## Visualizations

### Basic Greeks (visualization.py)
<img width="2010" height="1441" alt="greeks_visualization" src="https://github.com/user-attachments/assets/5eaf0d24-6db3-4397-b6c4-43a0c395ed9e" />

```bash
python visualization.py
```

Plots all 5 Greeks across a range of stock prices.

### Advanced Greeks — Time and Moneyness (visualization_greeks.py)

```bash
python visualization_greeks.py
```

Generates 3 charts addressing near-expiry Greek behavior across ATM, ITM, and OTM options:

**Chart 1 — Greeks vs Time to Expiry**
All 5 Greeks plotted from 3 days to 2 years, across three moneyness scenarios:
- OTM (S=90, K=100)
- ATM (S=100, K=100)
- ITM (S=110, K=100)

Includes a near-expiry Delta closeup showing convergence behavior as T → 0.
<img width="2234" height="1382" alt="greeks_vs_time" src="https://github.com/user-attachments/assets/5eda5b63-3c8c-4096-94a5-2363f87812cb" />

**Chart 2 — Delta Heatmap**
Contour map of Delta across stock price (S=70 to 130) and time to expiry (0 to 1 year). Contour lines at Delta = 0.25, 0.50, 0.75.
<img width="1406" height="879" alt="delta_heatmap" src="https://github.com/user-attachments/assets/3715fd97-1df7-4b99-af4d-040ba157581f" />

**Chart 3 — Volatility Sensitivity**
Option price vs volatility (5% to 80%) across four time horizons: 3 months, 6 months, 1 year, 2 years.
<img width="1482" height="878" alt="volatility_sensitivity" src="https://github.com/user-attachments/assets/943f4d2e-a2d8-4986-be58-a6a2e6f85ce1" />

> Visualization updated based on feedback from Jonathan Schachter PhD (Wall Street quant, model governance) — treating T as a live parameter and analyzing Greeks across moneyness near expiry.

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the pricing engine
python black_scholes.py

# Run examples
python examples/basic_usage.py

# Generate basic visualization
python visualization.py

# Generate advanced Greeks visualization
python visualization_greeks.py
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| NumPy | Vectorized calculations |
| SciPy | Brent's method for IV, normal distributions |
| Matplotlib | All visualizations |

---

## Key Validation Checks

- **Put-Call Parity:** `C - P = S - K * e^(-rT)` → verified ($4.88 = $4.88)
- **Implied Volatility:** Extracted IV matches input sigma exactly (20.00%)
- **Monte Carlo convergence:** MC price ($10.22) within 2.2% of analytical ($10.45) at 10,000 paths

---

## Project Series

| # | Project | Status |
|---|---------|--------|
| 1 | Black-Scholes Options Pricing Engine | ✅ Complete |
| 2 | Risk Parity Portfolio Optimizer | 🔄 In Progress |
| 3 | Fama-French Factor Model | 📅 Week 3 |
| 4 | Pairs Trading / Statistical Arbitrage | 📅 Week 4 |
| 5 | Live Market Risk Dashboard (Streamlit) | 📅 Week 5-6 |

---

## Author

**Abhilash Gangineni**
MS Finance, University of North Texas (GPA: 3.50) | B.Tech Computer Science, VIT

- GitHub: [github.com/AbhilashGangineni](https://github.com/AbhilashGangineni)
- LinkedIn: [linkedin.com/in/abhilash-gangineni](https://linkedin.com/in/abhilash-gangineni)
- Project: [Black-Scholes-Engine](https://github.com/AbhilashGangineni/Black-Scholes-Engine)
