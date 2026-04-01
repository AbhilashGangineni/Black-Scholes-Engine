"""
examples/basic_usage.py
Basic usage examples for the Black-Scholes Engine
Abhilash Gangineni | MS Finance @ UNT
"""

from black_scholes import BlackScholesEngine

# ─────────────────────────────────────────────
# Example 1: ATM Option Pricing
# ─────────────────────────────────────────────
print("=" * 52)
print("  EXAMPLE 1: At-The-Money (ATM) Option")
print("=" * 52)

bs_atm = BlackScholesEngine(S=100, K=100, T=1.0, r=0.05, sigma=0.20)
print(f"  Stock Price  : $100.00")
print(f"  Strike Price : $100.00  (ATM)")
print(f"  Expiry       : 1 year")
print(f"  Risk-Free    : 5.0%")
print(f"  Volatility   : 20.0%")
print()
print(f"  Call Price   : ${bs_atm.call_price():.4f}")
print(f"  Put Price    : ${bs_atm.put_price():.4f}")

greeks_atm = bs_atm.greeks()
print()
print("  Greeks (Call):")
for k, v in greeks_atm['call'].items():
    print(f"    {k.capitalize():<8}: {v:.6f}")


# ─────────────────────────────────────────────
# Example 2: OTM Option (Out-of-the-Money)
# ─────────────────────────────────────────────
print()
print("=" * 52)
print("  EXAMPLE 2: Out-of-The-Money (OTM) Call")
print("=" * 52)

bs_otm = BlackScholesEngine(S=90, K=110, T=0.5, r=0.05, sigma=0.25)
print(f"  Stock Price  : $90.00")
print(f"  Strike Price : $110.00  (OTM)")
print(f"  Expiry       : 0.5 years")
print(f"  Risk-Free    : 5.0%")
print(f"  Volatility   : 25.0%")
print()
print(f"  Call Price   : ${bs_otm.call_price():.4f}")
print(f"  Put Price    : ${bs_otm.put_price():.4f}")


# ─────────────────────────────────────────────
# Example 3: ITM Option (In-the-Money)
# ─────────────────────────────────────────────
print()
print("=" * 52)
print("  EXAMPLE 3: In-The-Money (ITM) Call")
print("=" * 52)

bs_itm = BlackScholesEngine(S=120, K=100, T=0.25, r=0.05, sigma=0.15)
print(f"  Stock Price  : $120.00")
print(f"  Strike Price : $100.00  (ITM)")
print(f"  Expiry       : 0.25 years")
print(f"  Risk-Free    : 5.0%")
print(f"  Volatility   : 15.0%")
print()
print(f"  Call Price   : ${bs_itm.call_price():.4f}")
print(f"  Put Price    : ${bs_itm.put_price():.4f}")


# ─────────────────────────────────────────────
# Example 4: Put-Call Parity Check
# ─────────────────────────────────────────────
print()
print("=" * 52)
print("  EXAMPLE 4: Put-Call Parity Verification")
print("=" * 52)

import math
S, K, T, r = 100, 100, 1.0, 0.05
bs_pcp = BlackScholesEngine(S=S, K=K, T=T, r=r, sigma=0.20)
call = bs_pcp.call_price()
put  = bs_pcp.put_price()
parity_lhs = call - put
parity_rhs = S - K * math.exp(-r * T)
print(f"  Call - Put         : {parity_lhs:.4f}")
print(f"  S - K*e^(-rT)      : {parity_rhs:.4f}")
print(f"  Parity Holds       : {abs(parity_lhs - parity_rhs) < 0.0001}")

print()
print("=" * 52)
print("  All examples completed successfully.")
print("=" * 52)
