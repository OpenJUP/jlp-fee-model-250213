import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ace_tools as tools

# -----------------------------
# 1. Define parameters
# -----------------------------
# Pool size for SOL in $
SOL_POOL_SIZE = 857_554_811

# Target utilization in decimal form
TARGET_UTIL = 0.80

# OLD SOL parameters (as decimals)
old_SOL_params = {
    "min": 0.10,       # 10%
    "target": 0.60,    # 60%
    "max": 2.30,       # 230%
    "lower_slope": 0.625,  # 62.5%
    "upper_slope": 8.50    # 850%
}

# GAUNTLET SOL parameters (as decimals)
gauntlet = {
    "min": 0.03,       # 3%
    "target": 0.20,    # 20%
    "max": 0.75,       # 75%
    "lower_slope": 0.2125, # 21.25%
    "upper_slope": 2.75    # 275%
}

# CHAOS RECOMMENDATIONS SOL parameters (as decimals)
chaos_recommendations = {
    "min": 0.03,       # 3%
    "target": 0.50,    # 50%
    "max": 1.50,       # 150%
    "lower_slope": 0.5875, # 58.75%
    "upper_slope": 5.00    # 500%
}

# -----------------------------
# 2. Dual-slope model function
# -----------------------------
def dual_slope_borrowing_rate(u, param):
    """
    Given utilization u (0 <= u <= 1) and a parameter dict with:
      param["min"], param["target"], param["max"],
      param["lower_slope"], param["upper_slope"],
    returns the borrowing rate in decimal form (e.g. 0.10 = 10% APR).
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
# 3. Generate fees data
# -----------------------------
util_range = np.linspace(0, 1.0, 101)  # 0%, 1%, 2%, ..., 100%
old_fees = []
gauntlet_fees = []
chaos_fees = []

for u in util_range:
    # Borrowed amount in $
    borrowed_amount = SOL_POOL_SIZE * u
    
    # Get annual borrowing rate
    old_rate = dual_slope_borrowing_rate(u, old_SOL_params)  # decimal
    gauntlet_rate = dual_slope_borrowing_rate(u, gauntlet)  # decimal
    chaos_rate = dual_slope_borrowing_rate(u, chaos_recommendations)  # decimal
    
    # Annual fees in $
    old_fee = borrowed_amount * old_rate
    gauntlet_fee = borrowed_amount * gauntlet_rate
    chaos_fee = borrowed_amount * chaos_rate
    
    old_fees.append(old_fee)
    gauntlet_fees.append(gauntlet_fee)
    chaos_fees.append(chaos_fee)

# -----------------------------
# 4. Plot the results with Y-axis in millions of dollars
# -----------------------------
plt.figure(figsize=(9, 6))

plt.plot(util_range*100, np.array(old_fees) / 1e6, 'r--', label="SOL old model")
plt.plot(util_range*100, np.array(gauntlet_fees) / 1e6, 'b-',  label="SOL gauntlet model")
plt.plot(util_range*100, np.array(chaos_fees) / 1e6, 'g-',  label="SOL chaos recommendations")

plt.title("Yearly Fee Revenue for SOL (Old vs. Gauntlet vs. Chaos) vs. Utilization")
plt.xlabel("Utilization (%)")
plt.ylabel("Yearly Fees (Million $)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -----------------------------
# 5. Print sample points
# -----------------------------
sample_utilizations = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
print("Sample utilization points:")
print("Util  | Old Fees ($)      | Gauntlet Fees ($)      | Chaos Fees ($)")
print("--------------------------------------------------------------")

sample_results = []
for su in sample_utilizations:
    # Borrowed amount
    borrowed_amount = SOL_POOL_SIZE * su
    
    old_rate = dual_slope_borrowing_rate(su, old_SOL_params)
    gauntlet_rate = dual_slope_borrowing_rate(su, gauntlet)
    chaos_rate = dual_slope_borrowing_rate(su, chaos_recommendations)
    
    old_fee = borrowed_amount * old_rate
    gauntlet_fee = borrowed_amount * gauntlet_rate
    chaos_fee = borrowed_amount * chaos_rate
    
    sample_results.append([f"{su:.0%}", f"{old_fee:,.2f}", f"{gauntlet_fee:,.2f}", f"{chaos_fee:,.2f}"])

df = pd.DataFrame(sample_results, columns=["Utilization", "Old Fees ($)", "Gauntlet Fees ($)", "Chaos Fees ($)"])
tools.display_dataframe_to_user(name="Sample Utilization Fees", dataframe=df)
