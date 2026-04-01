"""
tests/test_black_scholes.py
Unit Tests for Black-Scholes Engine
Abhilash Gangineni | MS Finance @ UNT
"""

import unittest
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from black_scholes import BlackScholesEngine


class TestBlackScholesPricing(unittest.TestCase):

    def setUp(self):
        """Standard ATM option used across most tests."""
        self.bs = BlackScholesEngine(S=100, K=100, T=1.0, r=0.05, sigma=0.20)

    # ─────────────────────────────────────────────
    # 1. Call & Put Prices — Basic Sanity
    # ─────────────────────────────────────────────
    def test_call_price_positive(self):
        """Call price must always be positive."""
        self.assertGreater(self.bs.call_price(), 0)

    def test_put_price_positive(self):
        """Put price must always be positive."""
        self.assertGreater(self.bs.put_price(), 0)

    def test_call_price_known_value(self):
        """ATM call price should be ~10.4506 for standard inputs."""
        self.assertAlmostEqual(self.bs.call_price(), 10.4506, places=3)

    def test_put_price_known_value(self):
        """ATM put price should be ~5.5735 for standard inputs."""
        self.assertAlmostEqual(self.bs.put_price(), 5.5735, places=3)

    # ─────────────────────────────────────────────
    # 2. Put-Call Parity
    # ─────────────────────────────────────────────
    def test_put_call_parity(self):
        """
        Put-Call Parity: C - P = S - K * e^(-rT)
        Must hold within 4 decimal places.
        """
        S, K, T, r = 100, 100, 1.0, 0.05
        lhs = self.bs.call_price() - self.bs.put_price()
        rhs = S - K * math.exp(-r * T)
        self.assertAlmostEqual(lhs, rhs, places=4)

    def test_put_call_parity_otm(self):
        """Put-Call Parity holds for OTM options too."""
        S, K, T, r, sigma = 90, 110, 0.5, 0.05, 0.25
        bs = BlackScholesEngine(S=S, K=K, T=T, r=r, sigma=sigma)
        lhs = bs.call_price() - bs.put_price()
        rhs = S - K * math.exp(-r * T)
        self.assertAlmostEqual(lhs, rhs, places=4)

    # ─────────────────────────────────────────────
    # 3. Greeks — Range Checks
    # ─────────────────────────────────────────────
    def test_call_delta_range(self):
        """Call Delta must be between 0 and 1."""
        delta = self.bs.greeks()['call']['delta']
        self.assertGreater(delta, 0)
        self.assertLess(delta, 1)

    def test_put_delta_range(self):
        """Put Delta must be between -1 and 0."""
        delta = self.bs.greeks()['put']['delta']
        self.assertLess(delta, 0)
        self.assertGreater(delta, -1)

    def test_gamma_positive(self):
        """Gamma must always be positive."""
        gamma = self.bs.greeks()['call']['gamma']
        self.assertGreater(gamma, 0)

    def test_vega_positive(self):
        """Vega must always be positive."""
        vega = self.bs.greeks()['call']['vega']
        self.assertGreater(vega, 0)

    def test_call_theta_negative(self):
        """Call Theta must be negative (time decay)."""
        theta = self.bs.greeks()['call']['theta']
        self.assertLess(theta, 0)

    def test_call_rho_positive(self):
        """Call Rho must be positive (calls benefit from rate increases)."""
        rho = self.bs.greeks()['call']['rho']
        self.assertGreater(rho, 0)

    def test_put_rho_negative(self):
        """Put Rho must be negative (puts hurt from rate increases)."""
        rho = self.bs.greeks()['put']['rho']
        self.assertLess(rho, 0)

    # ─────────────────────────────────────────────
    # 4. Boundary Conditions
    # ─────────────────────────────────────────────
    def test_deep_itm_call_delta_near_one(self):
        """Deep ITM call Delta should approach 1."""
        bs = BlackScholesEngine(S=200, K=100, T=1.0, r=0.05, sigma=0.20)
        delta = bs.greeks()['call']['delta']
        self.assertGreater(delta, 0.95)

    def test_deep_otm_call_delta_near_zero(self):
        """Deep OTM call Delta should approach 0."""
        bs = BlackScholesEngine(S=50, K=100, T=1.0, r=0.05, sigma=0.20)
        delta = bs.greeks()['call']['delta']
        self.assertLess(delta, 0.05)

    def test_high_volatility_increases_option_price(self):
        """Higher volatility should produce a higher call price."""
        bs_low  = BlackScholesEngine(S=100, K=100, T=1.0, r=0.05, sigma=0.10)
        bs_high = BlackScholesEngine(S=100, K=100, T=1.0, r=0.05, sigma=0.40)
        self.assertGreater(bs_high.call_price(), bs_low.call_price())

    def test_longer_expiry_increases_option_price(self):
        """Longer time to expiry should produce a higher call price."""
        bs_short = BlackScholesEngine(S=100, K=100, T=0.25, r=0.05, sigma=0.20)
        bs_long  = BlackScholesEngine(S=100, K=100, T=2.00, r=0.05, sigma=0.20)
        self.assertGreater(bs_long.call_price(), bs_short.call_price())


if __name__ == '__main__':
    unittest.main(verbosity=2)
