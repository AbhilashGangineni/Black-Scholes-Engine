"""
Black-Scholes Options Pricing Engine
=====================================
Author: Abhilash Gangineni
GitHub: github.com/AbhilashGangineni
LinkedIn: linkedin.com/in/abhilash-gangineni

Implements:
- Black-Scholes formula for European call and put options
- All 5 Greeks: Delta, Gamma, Theta, Vega, Rho
- Implied Volatility extraction using Brent's method
- Monte Carlo simulation with 10,000 paths
"""

import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
import warnings
warnings.filterwarnings('ignore')


class BlackScholes:
    """
    Black-Scholes options pricing engine.

    Parameters
    ----------
    S     : float -- Current stock price
    K     : float -- Strike price
    T     : float -- Time to expiration in years
    r     : float -- Risk-free interest rate (annual)
    sigma : float -- Volatility (annual)
    """

    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        self.S     = S
        self.K     = K
        self.T     = T
        self.r     = r
        self.sigma = sigma
        self.d1, self.d2 = self._compute_d1_d2()

    def _compute_d1_d2(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) \
             / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return d1, d2

    # ── Option Prices ──────────────────────────────────────

    def call_price(self) -> float:
        """European call option price using Black-Scholes formula."""
        return (self.S * norm.cdf(self.d1)
                - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2))

    def put_price(self) -> float:
        """European put option price using Black-Scholes formula."""
        return (self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
                - self.S * norm.cdf(-self.d1))

    # ── Greeks ─────────────────────────────────────────────

    def delta(self, option_type: str = 'call') -> float:
        """
        Delta: sensitivity of option price to stock price.
        Call delta is between 0 and 1.
        Put delta is between -1 and 0.
        """
        if option_type == 'call':
            return norm.cdf(self.d1)
        return norm.cdf(self.d1) - 1

    def gamma(self) -> float:
        """
        Gamma: rate of change of delta with respect to stock price.
        Same for calls and puts.
        High gamma means delta changes rapidly near expiry.
        """
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))

    def theta(self, option_type: str = 'call') -> float:
        """
        Theta: time decay of option value per day.
        Almost always negative -- options lose value as time passes.
        """
        common = (-(self.S * norm.pdf(self.d1) * self.sigma)
                  / (2 * np.sqrt(self.T)))
        if option_type == 'call':
            return (common - self.r * self.K
                    * np.exp(-self.r * self.T) * norm.cdf(self.d2)) / 365
        return (common + self.r * self.K
                * np.exp(-self.r * self.T) * norm.cdf(-self.d2)) / 365

    def vega(self) -> float:
        """
        Vega: sensitivity to a 1% change in volatility.
        Same for calls and puts.
        """
        return self.S * norm.pdf(self.d1) * np.sqrt(self.T) * 0.01

    def rho(self, option_type: str = 'call') -> float:
        """
        Rho: sensitivity to a 1% change in interest rate.
        """
        if option_type == 'call':
            return (self.K * self.T * np.exp(-self.r * self.T)
                    * norm.cdf(self.d2)) * 0.01
        return -(self.K * self.T * np.exp(-self.r * self.T)
                 * norm.cdf(-self.d2)) * 0.01

    def all_greeks(self, option_type: str = 'call') -> dict:
        """Return all 5 Greeks as a dictionary."""
        return {
            'Delta': self.delta(option_type),
            'Gamma': self.gamma(),
            'Theta': self.theta(option_type),
            'Vega':  self.vega(),
            'Rho':   self.rho(option_type),
        }

    def summary(self):
        """Print a complete pricing and Greeks summary."""
        print("=" * 52)
        print("   BLACK-SCHOLES PRICING SUMMARY")
        print("=" * 52)
        print(f"   Stock Price  (S):    ${self.S:.2f}")
        print(f"   Strike Price (K):    ${self.K:.2f}")
        print(f"   Time to Expiry (T):  {self.T:.2f} years")
        print(f"   Risk-Free Rate (r):  {self.r*100:.1f}%")
        print(f"   Volatility (sigma):  {self.sigma*100:.1f}%")
        print("-" * 52)
        print(f"   Call Price:          ${self.call_price():.4f}")
        print(f"   Put Price:           ${self.put_price():.4f}")
        print("-" * 52)
        print("   GREEKS (Call)")
        for name, val in self.all_greeks('call').items():
            print(f"   {name:<10}           {val:.6f}")
        print("-" * 52)
        print("   GREEKS (Put)")
        for name, val in self.all_greeks('put').items():
            print(f"   {name:<10}           {val:.6f}")
        print("=" * 52)


# ── Implied Volatility ─────────────────────────────────────

def implied_volatility(market_price: float, S: float, K: float,
                       T: float, r: float,
                       option_type: str = 'call') -> float:
    """
    Extract implied volatility from a market option price
    using Brent's root-finding method.

    Returns implied volatility as a decimal (e.g. 0.25 = 25%)
    Returns np.nan if no solution found.
    """
    def objective(sigma):
        bs = BlackScholes(S, K, T, r, sigma)
        if option_type == 'call':
            return bs.call_price() - market_price
        return bs.put_price() - market_price

    try:
        return brentq(objective, 1e-6, 10.0, xtol=1e-6)
    except ValueError:
        return np.nan


# ── Monte Carlo Simulation ─────────────────────────────────

def monte_carlo_price(S: float, K: float, T: float, r: float,
                      sigma: float, option_type: str = 'call',
                      n_simulations: int = 10_000,
                      n_steps: int = 252,
                      seed: int = 42) -> dict:
    """
    Price European options using Monte Carlo simulation.
    Simulates stock price paths using Geometric Brownian Motion:

        dS = r*S*dt + sigma*S*dW

    Parameters
    ----------
    n_simulations : number of price paths to simulate
    n_steps       : number of time steps per path (252 = daily)
    seed          : random seed for reproducibility

    Returns dict with price, std error, and 95% confidence interval.
    """
    np.random.seed(seed)
    dt = T / n_steps

    # Simulate log returns using GBM
    Z = np.random.standard_normal((n_simulations, n_steps))
    log_returns = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    price_paths = S * np.exp(np.cumsum(log_returns, axis=1))

    # Final stock prices at expiry
    S_T = price_paths[:, -1]

    # Calculate payoffs
    if option_type == 'call':
        payoffs = np.maximum(S_T - K, 0)
    else:
        payoffs = np.maximum(K - S_T, 0)

    # Discount payoffs back to present value
    discounted = np.exp(-r * T) * payoffs
    price      = np.mean(discounted)
    std_err    = np.std(discounted) / np.sqrt(n_simulations)
    ci_95      = (price - 1.96 * std_err, price + 1.96 * std_err)

    return {
        'price':         price,
        'std_error':     std_err,
        'ci_95':         ci_95,
        'paths':         price_paths,
        'final_prices':  S_T
    }


# ── Main Demo ──────────────────────────────────────────────

if __name__ == "__main__":

    # Parameters
    S     = 100.0   # Current stock price
    K     = 100.0   # Strike price (at-the-money)
    T     = 1.0     # 1 year to expiry
    r     = 0.05    # 5% risk-free rate
    sigma = 0.20    # 20% volatility

    print("\nQUANT PROJECT 1 — BLACK-SCHOLES ENGINE")
    print("Abhilash Gangineni | MS Finance @ UNT\n")

    # 1. Black-Scholes pricing
    bs = BlackScholes(S, K, T, r, sigma)
    bs.summary()

    # 2. Implied volatility extraction
    print("\n--- IMPLIED VOLATILITY ---")
    call_price = bs.call_price()
    iv = implied_volatility(call_price, S, K, T, r, 'call')
    print(f"Market Call Price:   ${call_price:.4f}")
    print(f"Extracted IV:        {iv*100:.2f}%  (matches sigma = {sigma*100:.0f}%)")

    # 3. Monte Carlo simulation
    print("\n--- MONTE CARLO SIMULATION (10,000 paths) ---")
    mc = monte_carlo_price(S, K, T, r, sigma, 'call', n_simulations=10_000)
    print(f"MC Call Price:       ${mc['price']:.4f}")
    print(f"BS Call Price:       ${bs.call_price():.4f}")
    print(f"Difference:          ${abs(mc['price'] - bs.call_price()):.4f}")
    print(f"95% CI:              (${mc['ci_95'][0]:.4f}, ${mc['ci_95'][1]:.4f})")
