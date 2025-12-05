# Project 3: Azure Storage Cost Analyzer
# Problem: Analyze blob storage to identify cost optimization opportunities
# Solution: Use Pandas to filter, analyze, and recommend tier changes

# Import Pandas library for data manipulation
import pandas as pd
import numpy as np

print("=" * 80)
print("AZURE BLOB STORAGE - COST OPTIMIZATION ANALYSIS")
print("=" * 80)

# --- Pandas Series ---
# Series: One-dimensional labeled array (single column of data)

# Create Series for storage account names
storage_accounts = pd.Series([
    'proddata01', 'devlogs02', 'backups03', 'archives04', 
    'tempfiles05', 'webapp06', 'analytics07', 'media08'
])

print("\n--- Storage Account Names (Pandas Series) ---")
print(storage_accounts)
print(f"Type: {type(storage_accounts)}")
print(f"Total Accounts: {len(storage_accounts)}")


# --- Pandas DataFrame ---
# DataFrame: Two-dimensional labeled table (like Excel spreadsheet)

# Create DataFrame with storage usage data
storage_data = pd.DataFrame({
    'account_name': [
        'proddata01', 'devlogs02', 'backups03', 'archives04',
        'tempfiles05', 'webapp06', 'analytics07', 'media08',
        'reports09', 'userfiles10'
    ],
    'size_gb': [1250, 45, 3200, 8500, 12, 890, 2100, 5600, 340, 1500],
    'monthly_cost': [125.50, 8.90, 280.00, 425.00, 2.40, 98.00, 189.00, 448.00, 42.50, 165.00],
    'current_tier': [
        'Hot', 'Hot', 'Hot', 'Hot', 'Hot', 'Hot', 'Cool', 'Hot', 'Hot', 'Cool'
    ],
    'last_access_days': [2, 5, 45, 180, 3, 1, 90, 10, 30, 120],
    'transaction_count': [15000, 2300, 100, 50, 8900, 45000, 200, 12000, 1500, 400]
})

print("\n--- Storage Accounts DataFrame ---")
# Display first few rows using .head()
print(storage_data.head())

# Display DataFrame info
print("\n--- DataFrame Information ---")
print(f"Shape (rows, columns): {storage_data.shape}")
print(f"Column Names: {list(storage_data.columns)}")
print(f"Data Types:\n{storage_data.dtypes}")


# --- Basic DataFrame Operations ---
print("\n" + "=" * 80)
print("BASIC STATISTICS")
print("=" * 80)

# Calculate total storage across all accounts
total_storage = storage_data['size_gb'].sum()
print(f"Total Storage Used: {total_storage:,.0f} GB")

# Calculate total monthly cost
total_cost = storage_data['monthly_cost'].sum()
print(f"Total Monthly Cost: ${total_cost:,.2f}")

# Calculate average cost per GB
avg_cost_per_gb = total_cost / total_storage
print(f"Average Cost per GB: ${avg_cost_per_gb:.4f}")

# Find maximum and minimum
max_cost_account = storage_data.loc[storage_data['monthly_cost'].idxmax()]
print(f"\nMost Expensive Account: {max_cost_account['account_name']} - ${max_cost_account['monthly_cost']}")

min_cost_account = storage_data.loc[storage_data['monthly_cost'].idxmin()]
print(f"Least Expensive Account: {min_cost_account['account_name']} - ${min_cost_account['monthly_cost']}")

# Statistical summary using .describe()
print("\n--- Storage Size Statistics ---")
print(storage_data['size_gb'].describe())


# --- Filtering DataFrames ---
print("\n" + "=" * 80)
print("🔍 FILTERED ANALYSIS")
print("=" * 80)

# Filter 1: Accounts in Hot tier (using boolean indexing)
hot_tier_accounts = storage_data[storage_data['current_tier'] == 'Hot']
print(f"\n--- Hot Tier Accounts ---")
print(hot_tier_accounts[['account_name', 'size_gb', 'monthly_cost']])
print(f"Total Hot Tier Cost: ${hot_tier_accounts['monthly_cost'].sum():,.2f}")

# Filter 2: Large storage accounts (> 1000 GB)
large_accounts = storage_data[storage_data['size_gb'] > 1000]
print(f"\n--- Large Storage Accounts (> 1000 GB) ---")
print(large_accounts[['account_name', 'size_gb', 'current_tier']])

# Filter 3: Rarely accessed accounts (> 30 days)
# These are candidates for Cool/Archive tier
rarely_accessed = storage_data[storage_data['last_access_days'] > 30]
print(f"\n--- Rarely Accessed Accounts (> 30 days) ---")
print(rarely_accessed[['account_name', 'last_access_days', 'current_tier', 'monthly_cost']])

# Filter 4: Multiple conditions using & (AND)
# Hot tier AND rarely accessed AND large size
optimization_candidates = storage_data[
    (storage_data['current_tier'] == 'Hot') & 
    (storage_data['last_access_days'] > 30) &
    (storage_data['size_gb'] > 500)
]
print(f"\n--- HIGH PRIORITY Optimization Candidates ---")
print(optimization_candidates[['account_name', 'size_gb', 'monthly_cost', 'last_access_days']])


# --- Adding Calculated Columns ---
print("\n" + "=" * 80)
print("💰 COST OPTIMIZATION OPPORTUNITIES")
print("=" * 80)

# Add new column: cost per GB for each account
storage_data['cost_per_gb'] = storage_data['monthly_cost'] / storage_data['size_gb']

# Add new column: recommended tier based on access patterns
def recommend_tier(row):
    """
    Recommend storage tier based on access patterns
    Hot: Accessed frequently (< 30 days)
    Cool: Accessed occasionally (30-90 days)
    Archive: Rarely accessed (> 90 days)
    """
    if row['last_access_days'] < 30:
        return 'Hot'
    elif row['last_access_days'] < 90:
        return 'Cool'
    else:
        return 'Archive'

# Apply function to each row
storage_data['recommended_tier'] = storage_data.apply(recommend_tier, axis=1)

# Calculate potential savings (Cool tier saves ~50%, Archive saves ~80%)
def calculate_savings(row):
    current = row['current_tier']
    recommended = row['recommended_tier']
    cost = row['monthly_cost']
    
    if current == 'Hot' and recommended == 'Cool':
        return cost * 0.50  # 50% savings
    elif current == 'Hot' and recommended == 'Archive':
        return cost * 0.80  # 80% savings
    elif current == 'Cool' and recommended == 'Archive':
        return cost * 0.60  # 60% savings
    else:
        return 0

storage_data['potential_savings'] = storage_data.apply(calculate_savings, axis=1)

# Display optimization recommendations
print("\n--- Tier Change Recommendations ---")
needs_optimization = storage_data[storage_data['current_tier'] != storage_data['recommended_tier']]
print(needs_optimization[['account_name', 'current_tier', 'recommended_tier', 
                          'monthly_cost', 'potential_savings', 'last_access_days']])

# Calculate total potential savings
total_savings = storage_data['potential_savings'].sum()
annual_savings = total_savings * 12

print(f"\n💡 SAVINGS SUMMARY:")
print(f"   Total Monthly Savings: ${total_savings:,.2f}")
print(f"   Annual Savings: ${annual_savings:,.2f}")
print(f"   Accounts to Optimize: {len(needs_optimization)}")


# --- Sorting DataFrames ---
print("\n" + "=" * 80)
print("📊 TOP OPTIMIZATION OPPORTUNITIES (Sorted by Savings)")
print("=" * 80)

# Sort by potential savings (descending)
top_opportunities = storage_data.sort_values('potential_savings', ascending=False).head(5)
print(top_opportunities[['account_name', 'size_gb', 'current_tier', 
                         'recommended_tier', 'potential_savings']])


# --- Tier Distribution Analysis ---
print("\n" + "=" * 80)
print("STORAGE TIER DISTRIBUTION")
print("=" * 80)

# Count accounts by tier using .value_counts()
current_distribution = storage_data['current_tier'].value_counts()
print("\n--- Current Tier Distribution ---")
print(current_distribution)

recommended_distribution = storage_data['recommended_tier'].value_counts()
print("\n--- Recommended Tier Distribution ---")
print(recommended_distribution)

# Group by tier and calculate totals
tier_analysis = storage_data.groupby('current_tier').agg({
    'size_gb': 'sum',
    'monthly_cost': 'sum',
    'account_name': 'count'
})
tier_analysis.columns = ['Total_GB', 'Total_Cost', 'Account_Count']

print("\n--- Cost by Current Tier ---")
print(tier_analysis)


# --- Final Summary Report ---
print("\n" + "=" * 80)
print("📋 EXECUTIVE SUMMARY")
print("=" * 80)

print(f"""
Storage Overview:
  • Total Accounts: {len(storage_data)}
  • Total Storage: {total_storage:,.0f} GB
  • Current Monthly Cost: ${total_cost:,.2f}
  
Optimization Potential:
  • Accounts Needing Optimization: {len(needs_optimization)}
  • Monthly Savings Available: ${total_savings:,.2f}
  • Annual Savings Available: ${annual_savings:,.2f}
  • ROI: {(total_savings / total_cost * 100):.1f}% monthly cost reduction

Top Recommendation:
  • Move {len(needs_optimization)} accounts to appropriate tiers
  • Focus on Hot tier accounts not accessed in 30+ days
  • Prioritize large storage accounts (> 1000 GB) for maximum impact
""")

print("=" * 80)
print("✓ Analysis Complete - Review recommendations and implement changes")
print("=" * 80)