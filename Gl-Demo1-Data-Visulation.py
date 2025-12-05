# ============================================================================
# CELL 1: Import Libraries (100% Pre-installed in Azure ML)
# ============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

print("✅ Libraries loaded successfully!")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Set matplotlib style
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


# ============================================================================
# CELL 2: Generate Azure Blob Data
# ============================================================================
print("🔷 GENERATING AZURE BLOB STORAGE DATA\n")

np.random.seed(42)

# Simulate 300 blobs across 3 containers
data = {
    'blob_name': [f'backup-{i}.zip' for i in range(100)] + 
                 [f'log-{i}.txt' for i in range(150)] +
                 [f'media-{i}.mp4' for i in range(50)],
    'size_mb': np.random.randint(1, 5000, 300),
    'last_accessed_days': np.random.randint(1, 365, 300),
    'access_tier': np.random.choice(['Hot', 'Cool', 'Archive'], 300),
    'container': ['backups']*100 + ['logs']*150 + ['media']*50
}

df = pd.DataFrame(data)

print(f"✅ Generated {len(df)} blobs")
print(f"📦 Containers: {df['container'].nunique()}")
print(f"🔄 Tiers: {df['access_tier'].unique().tolist()}\n")

# Show sample
print("Sample Data:")
df.head(10)


# ============================================================================
# CELL 3: Calculate Costs
# ============================================================================
print("💰 CALCULATING COSTS\n")

# Azure pricing per GB/month
tier_costs = {'Hot': 0.018, 'Cool': 0.01, 'Archive': 0.00099}

# Calculate monthly cost
df['monthly_cost'] = df.apply(
    lambda row: (row['size_mb']/1024) * tier_costs[row['access_tier']], 
    axis=1
)
df['size_gb'] = df['size_mb'] / 1024

print(f"💵 Total Monthly Cost: ${df['monthly_cost'].sum():.2f}")
print(f"📊 Total Storage: {df['size_gb'].sum():.2f} GB")
print(f"📈 Average blob size: {df['size_gb'].mean():.2f} GB\n")

# Cost by tier
print("💰 Cost by Access Tier:")
tier_cost_summary = df.groupby('access_tier')['monthly_cost'].sum().sort_values(ascending=False)
for tier, cost in tier_cost_summary.items():
    pct = (cost / df['monthly_cost'].sum()) * 100
    print(f"  {tier:8s}: ${cost:7.2f} ({pct:5.1f}%)")


# ============================================================================
# CELL 4: Storage Analysis
# ============================================================================
print("\n📊 STORAGE ANALYSIS")
print("=" * 70)

# By container
print("\n📦 Storage by Container:")
container_summary = df.groupby('container').agg({
    'size_gb': ['sum', 'mean', 'count'],
    'monthly_cost': 'sum'
}).round(2)
container_summary.columns = ['Total_GB', 'Avg_GB', 'Blob_Count', 'Monthly_Cost']
container_summary = container_summary.sort_values('Monthly_Cost', ascending=False)
display(container_summary)

# By tier
print("\n🔄 Storage by Access Tier:")
tier_summary = df.groupby('access_tier').agg({
    'blob_name': 'count',
    'size_gb': 'sum',
    'monthly_cost': 'sum'
}).round(2)
tier_summary.columns = ['Blob_Count', 'Size_GB', 'Monthly_Cost']
tier_summary = tier_summary.sort_values('Monthly_Cost', ascending=False)
display(tier_summary)

# Access pattern statistics
print("\n📈 Access Pattern Statistics:")
print(f"  Average days since access: {df['last_accessed_days'].mean():.1f}")
print(f"  Median days since access: {df['last_accessed_days'].median():.1f}")
print(f"  Blobs not accessed in 90+ days: {len(df[df['last_accessed_days'] > 90])}")
print(f"  Blobs not accessed in 180+ days: {len(df[df['last_accessed_days'] > 180])}")


# ============================================================================
# CELL 5: Find Optimization Opportunities
# ============================================================================
print("\n💡 OPTIMIZATION OPPORTUNITIES")
print("=" * 70)

# Hot tier blobs not accessed in 90+ days
hot_unused = df[(df['access_tier'] == 'Hot') & (df['last_accessed_days'] > 90)]

if len(hot_unused) > 0:
    current_cost = hot_unused['monthly_cost'].sum()
    savings = current_cost * 0.44  # 44% savings moving to Cool
    
    print("\n✅ RECOMMENDATION 1: Move Hot → Cool")
    print(f"   Criteria: Not accessed in 90+ days")
    print(f"   Blobs to move: {len(hot_unused)}")
    print(f"   Total size: {hot_unused['size_gb'].sum():.2f} GB")
    print(f"   Current cost: ${current_cost:.2f}/month")
    print(f"   New cost (Cool): ${current_cost * 0.56:.2f}/month")
    print(f"   💰 Potential savings: ${savings:.2f}/month (${savings*12:.2f}/year)")
    
    print("\n   Top 5 Candidates by Cost:")
    top_hot = hot_unused.nlargest(5, 'monthly_cost')[
        ['blob_name', 'size_gb', 'last_accessed_days', 'monthly_cost']
    ].copy()
    top_hot['potential_saving'] = top_hot['monthly_cost'] * 0.44
    display(top_hot)
else:
    print("\n✅ Hot tier is optimized - no blobs unused for 90+ days")

# Cool tier blobs not accessed in 180+ days
cool_unused = df[(df['access_tier'] == 'Cool') & (df['last_accessed_days'] > 180)]

if len(cool_unused) > 0:
    current_cost_cool = cool_unused['monthly_cost'].sum()
    savings_archive = current_cost_cool * 0.90  # 90% savings moving to Archive
    
    print("\n✅ RECOMMENDATION 2: Move Cool → Archive")
    print(f"   Criteria: Not accessed in 180+ days")
    print(f"   Blobs to move: {len(cool_unused)}")
    print(f"   Total size: {cool_unused['size_gb'].sum():.2f} GB")
    print(f"   💰 Potential savings: ${savings_archive:.2f}/month (${savings_archive*12:.2f}/year)")
else:
    print("\n✅ Cool tier is optimized - no blobs unused for 180+ days")

# Total savings
total_monthly_savings = (savings if len(hot_unused) > 0 else 0) + \
                        (savings_archive if len(cool_unused) > 0 else 0)
print(f"\n🎯 TOTAL POTENTIAL SAVINGS: ${total_monthly_savings:.2f}/month (${total_monthly_savings*12:.2f}/year)")
print(f"   ROI: {(total_monthly_savings/df['monthly_cost'].sum()*100):.1f}% cost reduction")


# ============================================================================
# CELL 6: Create Visual Dashboard
# ============================================================================
print("\n📊 CREATING VISUAL DASHBOARD")
print("=" * 70)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Azure Blob Storage Analysis Dashboard', fontsize=18, fontweight='bold', y=0.995)

# Plot 1: Storage by Container (Bar Chart)
container_storage = df.groupby('container')['size_gb'].sum().sort_values(ascending=False)
bars = axes[0, 0].bar(container_storage.index, container_storage.values, 
                       color='#0078D4', edgecolor='black', linewidth=1.5)
axes[0, 0].set_title('Storage by Container (GB)', fontweight='bold', fontsize=12)
axes[0, 0].set_ylabel('Size (GB)', fontsize=10)
axes[0, 0].grid(axis='y', alpha=0.3)
# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 5,
                     f'{height:.0f}', ha='center', va='bottom', fontweight='bold')

# Plot 2: Cost Distribution by Tier (Pie Chart)
tier_costs_plot = df.groupby('access_tier')['monthly_cost'].sum()
colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']
wedges, texts, autotexts = axes[0, 1].pie(tier_costs_plot.values, 
                                            labels=tier_costs_plot.index, 
                                            autopct='%1.1f%%',
                                            colors=colors,
                                            startangle=90,
                                            textprops={'fontweight': 'bold'})
axes[0, 1].set_title('Cost Distribution by Tier', fontweight='bold', fontsize=12)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(10)

# Plot 3: Blob Count by Tier (Bar Chart)
tier_counts = df['access_tier'].value_counts()
bars3 = axes[0, 2].bar(tier_counts.index, tier_counts.values,
                        color=['#FF6B6B', '#4ECDC4', '#95E1D3'],
                        edgecolor='black', linewidth=1.5)
axes[0, 2].set_title('Blob Count by Tier', fontweight='bold', fontsize=12)
axes[0, 2].set_ylabel('Number of Blobs', fontsize=10)
axes[0, 2].grid(axis='y', alpha=0.3)
for bar in bars3:
    height = bar.get_height()
    axes[0, 2].text(bar.get_x() + bar.get_width()/2., height + 2,
                     f'{int(height)}', ha='center', va='bottom', fontweight='bold')

# Plot 4: Access Pattern Histogram
axes[1, 0].hist(df['last_accessed_days'], bins=30, color='#107C10', 
                edgecolor='black', alpha=0.7)
axes[1, 0].axvline(x=90, color='red', linestyle='--', linewidth=2, label='90 days (Hot→Cool)')
axes[1, 0].axvline(x=180, color='orange', linestyle='--', linewidth=2, label='180 days (Cool→Archive)')
axes[1, 0].set_title('Blob Access Patterns', fontweight='bold', fontsize=12)
axes[1, 0].set_xlabel('Days Since Last Access', fontsize=10)
axes[1, 0].set_ylabel('Number of Blobs', fontsize=10)
axes[1, 0].legend(fontsize=9)
axes[1, 0].grid(alpha=0.3)

# Plot 5: Size vs Cost Scatter
scatter = axes[1, 1].scatter(df['size_gb'], df['monthly_cost'], 
                              c=df['last_accessed_days'], cmap='RdYlGn_r',
                              alpha=0.6, s=60, edgecolors='black', linewidth=0.5)
axes[1, 1].set_title('Size vs Cost (color = days since access)', fontweight='bold', fontsize=12)
axes[1, 1].set_xlabel('Size (GB)', fontsize=10)
axes[1, 1].set_ylabel('Monthly Cost ($)', fontsize=10)
axes[1, 1].grid(alpha=0.3)
cbar = plt.colorbar(scatter, ax=axes[1, 1])
cbar.set_label('Days Since Access', fontsize=9)

# Plot 6: Cost by Container (Horizontal Bar)
container_costs = df.groupby('container')['monthly_cost'].sum().sort_values()
bars6 = axes[1, 2].barh(container_costs.index, container_costs.values,
                         color='#50E6FF', edgecolor='black', linewidth=1.5)
axes[1, 2].set_title('Monthly Cost by Container', fontweight='bold', fontsize=12)
axes[1, 2].set_xlabel('Cost ($)', fontsize=10)
axes[1, 2].grid(axis='x', alpha=0.3)
for i, bar in enumerate(bars6):
    width = bar.get_width()
    axes[1, 2].text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                     f'${width:.2f}', va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('azure_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ Dashboard created and saved as 'azure_dashboard.png'")


# ============================================================================
# CELL 7: Export Recommendations to CSV
# ============================================================================
print("\n📤 EXPORTING RECOMMENDATIONS")
print("=" * 70)

if len(hot_unused) > 0:
    # Create detailed recommendations
    recommendations = hot_unused[['blob_name', 'container', 'size_gb', 
                                   'last_accessed_days', 'access_tier', 
                                   'monthly_cost']].copy()
    
    recommendations['recommended_tier'] = 'Cool'
    recommendations['new_monthly_cost'] = recommendations['monthly_cost'] * 0.56
    recommendations['potential_savings'] = recommendations['monthly_cost'] * 0.44
    
    # Sort by savings potential
    recommendations = recommendations.sort_values('potential_savings', ascending=False)
    
    # Export to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'azure_optimization_recommendations_{timestamp}.csv'
    recommendations.to_csv(filename, index=False)
    
    print(f"\n✅ Exported {len(recommendations)} recommendations to: {filename}")
    print(f"\n📋 Top 10 Optimization Opportunities:")
    display(recommendations.head(10))
    
    # Summary stats
    print(f"\n📊 Recommendations Summary:")
    print(f"   Total blobs to optimize: {len(recommendations)}")
    print(f"   Total storage to move: {recommendations['size_gb'].sum():.2f} GB")
    print(f"   Current monthly cost: ${recommendations['monthly_cost'].sum():.2f}")
    print(f"   New monthly cost: ${recommendations['new_monthly_cost'].sum():.2f}")
    print(f"   💰 Total savings: ${recommendations['potential_savings'].sum():.2f}/month")
    print(f"   💰 Annual savings: ${recommendations['potential_savings'].sum() * 12:.2f}")
else:
    print("\n✅ No optimization recommendations needed!")
    print("   Your storage is already optimally tiered.")


# ============================================================================
# CELL 8: Final Summary Report
# ============================================================================
print("\n" + "=" * 70)
print("🎉 AZURE BLOB STORAGE ANALYSIS - FINAL REPORT")
print("=" * 70)

total_savings = recommendations['potential_savings'].sum() if len(hot_unused) > 0 else 0

# Create formatted summary
summary = f"""
📊 STORAGE OVERVIEW:
   • Total Blobs: {len(df):,}
   • Total Storage: {df['size_gb'].sum():.2f} GB
   • Number of Containers: {df['container'].nunique()}
   • Average Blob Size: {df['size_gb'].mean():.2f} GB

💰 COST ANALYSIS:
   • Current Monthly Cost: ${df['monthly_cost'].sum():.2f}
   • Current Annual Cost: ${df['monthly_cost'].sum() * 12:.2f}
   • Most Expensive Container: {container_costs.idxmax()} (${container_costs.max():.2f}/month)

🔄 TIER DISTRIBUTION:
   • Hot Tier: {len(df[df['access_tier']=='Hot'])} blobs ({len(df[df['access_tier']=='Hot'])/len(df)*100:.1f}%)
   • Cool Tier: {len(df[df['access_tier']=='Cool'])} blobs ({len(df[df['access_tier']=='Cool'])/len(df)*100:.1f}%)
   • Archive Tier: {len(df[df['access_tier']=='Archive'])} blobs ({len(df[df['access_tier']=='Archive'])/len(df)*100:.1f}%)

📈 ACCESS PATTERNS:
   • Average days since access: {df['last_accessed_days'].mean():.1f}
   • Blobs unused 90+ days: {len(df[df['last_accessed_days'] > 90])}
   • Blobs unused 180+ days: {len(df[df['last_accessed_days'] > 180])}

💡 OPTIMIZATION RESULTS:
   • Blobs to optimize: {len(hot_unused) + len(cool_unused)}
   • Potential monthly savings: ${total_savings:.2f}
   • Potential annual savings: ${total_savings * 12:.2f}
   • Cost reduction: {(total_savings/df['monthly_cost'].sum()*100):.1f}%

📁 GENERATED FILES:
   1. azure_dashboard.png - Visual analytics dashboard
   2. {filename if len(hot_unused) > 0 else 'N/A'} - Optimization recommendations

✅ NEXT STEPS:
   1. Review the recommendations CSV file
   2. Implement tier changes using Azure Portal or CLI
   3. Schedule monthly reviews to maintain optimization
   4. Consider Azure Lifecycle Management policies for automation
"""

print(summary)
print("=" * 70)

# Create quick stats table
summary_data = pd.DataFrame({
    'Metric': [
        'Total Blobs',
        'Total Storage (GB)',
        'Current Monthly Cost',
        'Optimization Opportunities',
        'Potential Monthly Savings',
        'Annual Savings',
        'ROI (%)'
    ],
    'Value': [
        f"{len(df):,}",
        f"{df['size_gb'].sum():.2f}",
        f"${df['monthly_cost'].sum():.2f}",
        f"{len(hot_unused) + len(cool_unused)} blobs",
        f"${total_savings:.2f}",
        f"${total_savings * 12:.2f}",
        f"{(total_savings/df['monthly_cost'].sum()*100):.1f}%"
    ]
})

print("\n📊 Quick Reference Table:")
display(summary_data.style.set_properties(**{'text-align': 'left', 'font-weight': 'bold'}).hide(axis='index'))

print("\n" + "=" * 70)
print("🎓 CONGRATULATIONS!")
print("You've successfully completed Python data analysis with Azure!")
print("=" * 70)
print("\nKey Skills Demonstrated:")
print("  ✅ Data manipulation with Pandas")
print("  ✅ Numerical computations with NumPy")
print("  ✅ Data visualization with Matplotlib")
print("  ✅ Cost optimization analysis")
print("  ✅ Business intelligence reporting")
print("\nYou're now ready to analyze real Azure Storage data!")
print("=" * 70)