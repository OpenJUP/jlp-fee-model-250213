import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Define parameters
# -----------------------------
# target utilization in decimal form
TARGET_UTIL = 0.80

# OLD parameters (as decimals)
old_params = {
    "SOL":  {"min": 0.10, "target": 0.60, "max": 2.30, "lower_slope": 0.625, "upper_slope": 8.50},
    "ETH":  {"min": 0.10, "target": 0.23, "max": 0.90, "lower_slope": 0.1625, "upper_slope": 3.35},
    "BTC":  {"min": 0.10, "target": 0.20, "max": 0.80, "lower_slope": 0.1250, "upper_slope": 3.00},
    "USDC": {"min": 0.10, "target": 0.10, "max": 0.25, "lower_slope": 0.00,   "upper_slope": 0.75},
    "USDT": {"min": 0.10, "target": 0.10, "max": 0.10, "lower_slope": 0.00,   "upper_slope": 0.00}
}

# NEW parameters (as decimals)
new_params = {
    "SOL":  {"min": 0.03, "target": 0.20, "max": 0.75, "lower_slope": 0.2125, "upper_slope": 2.75},
    "ETH":  {"min": 0.03, "target": 0.11, "max": 0.40, "lower_slope": 0.10,   "upper_slope": 1.45},
    "BTC":  {"min": 0.03, "target": 0.11, "max": 0.50, "lower_slope": 0.10,   "upper_slope": 1.95},
    "USDC": {"min": 0.03, "target": 0.10, "max": 0.30, "lower_slope": 0.0875, "upper_slope": 1.00},
    "USDT": {"min": 0.03, "target": 0.10, "max": 0.10, "lower_slope": 0.0875, "upper_slope": 0.00}
}

# -----------------------------
# 2. Dual-slope model function
# -----------------------------
def dual_slope_borrowing_rate(u, param):
    """
    Given utilization u (0 <= u <= 1) and a parameter dict with:
      param["min"], param["target"], param["max"],
      param["lower_slope"], param["upper_slope"],
    returns the borrowing rate in decimal form.
    """
    min_rate     = param["min"]
    target_rate  = param["target"]
    lower_slope  = param["lower_slope"]
    upper_slope  = param["upper_slope"]

    if u <= TARGET_UTIL:
        # from 0 to 80% utilization
        return min_rate + lower_slope * u
    else:
        # from 80% to 100% utilization
        return target_rate + upper_slope * (u - TARGET_UTIL)

# -----------------------------
# 3. Generate curves
# -----------------------------
util_range = np.linspace(0, 1.0, 200)  # 0% to 100% in 200 steps

# Prepare the figure
plt.figure(figsize=(10, 6))

# We'll plot the old curves in dashed lines, new curves in solid lines
for asset in old_params:
    old_rates = [dual_slope_borrowing_rate(u, old_params[asset]) for u in util_range]
    new_rates = [dual_slope_borrowing_rate(u, new_params[asset]) for u in util_range]
    
    # Convert from decimal to percentage
    old_rates_pct = [r * 100 for r in old_rates]
    new_rates_pct = [r * 100 for r in new_rates]
    
    plt.plot(util_range * 100, old_rates_pct, linestyle='--', label=f"{asset} old")
    plt.plot(util_range * 100, new_rates_pct, linestyle='-',  label=f"{asset} new")

# Add a horizontal line at the target utilization (80%) if you like
plt.axvline(x=80, color='gray', linestyle=':', alpha=0.5)

# -----------------------------
# 4. Customize and show plot
# -----------------------------
plt.title("Dual Slope Borrowing Rate Models (Old vs New)")
plt.xlabel("Utilization (%)")
plt.ylabel("Borrowing Rate (APR, %)")
plt.ylim(0, 250)   # adjust y-limit as needed
plt.legend(loc='upper left', ncol=2)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()