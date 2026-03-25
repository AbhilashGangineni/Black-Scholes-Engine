# Black-Scholes Options Pricing Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-1.24+-green.svg)
![SciPy](https://img.shields.io/badge/SciPy-1.10+-orange.svg)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow.svg)

A Python-based options pricing engine implementing the Black-Scholes model with full Greeks calculation, implied volatility extraction, and Monte Carlo simulation for European options pricing.

---

## Project Overview

This project builds a complete options pricing system from first principles covering the Black-Scholes closed-form solution, all five Greeks (Delta, Gamma, Theta, Vega, Rho), implied volatility extraction, and Monte Carlo simulation as an alternative pricing method.

**Part of my Quant Finance Project Series** - building toward a full quantitative research portfolio.

---

## Objectives

- Implement Black-Scholes formula for European call and put options
- Calculate all Greeks analytically: Delta, Gamma, Theta, Vega, Rho
- Extract implied volatility from market prices using numerical optimization
- Simulate option prices via Monte Carlo (10,000+ paths)
- Visualize volatility surface and Greeks sensitivity across strike and maturity

---

## Project Structure

```
Black-Scholes-Engine/
|
|-- black_scholes.py        # Core BS formula + Greeks
|-- implied_vol.py          # Implied volatility extraction
|-- monte_carlo.py          # Monte Carlo pricing simulation
|-- visualization.py        # Vol surface + Greeks plots
|-- requirements.txt
|-- README.md
```

---

## Black-Scholes Formula

For a European call option:

```
C = S * N(d1) - K * e^(-rT) * N(d2)

d1 = [ln(S/K) + (r + sigma^2/2) * T] / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)
```

Where:
- S = Current stock price
- K = Strike price
- T = Time to expiration (years)
- r = Risk-free interest rate
- sigma = Implied volatility
- N() = Cumulative standard normal distribution

---

## The Greeks

| Greek | Measures | 
|-------|----------|
| Delta | Price sensitivity to stock price |
| Gamma | Rate of change of delta |
| Theta | Time decay per day |
| Vega  | Sensitivity to volatility |
| Rho   | Sensitivity to interest rate |

---

## Tech Stack

- Python 3.10+
- NumPy - vectorized calculations
- SciPy - optimization and statistical distributions
- Matplotlib / Plotly - visualization
- Pandas - data handling

---

## Status

Currently in progress. Code and visualizations being added daily.

---

## Author

**Abhilash Gangineni**
MS Finance, University of North Texas (GPA: 3.50)
- LinkedIn: linkedin.com/in/abhilash-gangineni
  
---

*Part of a 5-project quantitative finance series.*
