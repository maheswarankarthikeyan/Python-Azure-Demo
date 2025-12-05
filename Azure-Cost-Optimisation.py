# ============================================================================
# LAB 4: AZURE COST OPTIMIZATION DASHBOARD
# Topics: Data Visualization, Chart Types, Insights Generation
# ============================================================================

# ============================================================================
# CELL 1: Setup and Generate Cost Data
# ============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

print("=" * 70)
print("💰 AZURE COST OPTIMIZATION DASHBOARD LAB")
print("=" * 70)

# Generate 90 days of Azure cost data
np.random.seed(42)

num_days = 90
start_date = datetime.now() - timedelta(days=num_days)

# Resource categories
services = ['Virtual Machines', 'Storage', 'SQL Database', 'App Service', 
            'Networking', 'Key Vault', 'Function App', 'Container Registry']

# Generate daily costs for each service
cost_data = []

for day in range(num_days):
    current_date = start_date + timedelta(days=day)
    
    for service in services:
        # Base costs with some growth over time
        base_cost = {
            'Virtual Machines': 350,
            'Storage': 120,
            'SQL Database': 280,
            'App Service': 200,
            'Networking': 80,
            'Key Vault': 15,
            'Function App': 45,
            'Container Registry': 30
        }[service]
        
        # Add growth trend
        growth_factor = 1 + (day / num_days) * 0.15  # 15% growth over period
        
        # Add randomness
        daily_cost = base_cost * growth_factor * np.random.uniform(0.85, 1.15)
        
        # Add weekly pattern (weekends cheaper)
        if current_date.weekday() >= 5:  # Weekend
            daily_cost *= 0.7
        
        cost_data.append({
            'date': current_date.date(),
            'service': service,
            'cost': round(daily_cost, 2),
            'resource_group': np.random.choice(['rg-production', 'rg-development', 'rg-staging']),
            'region': np.random.choice(['East US', 'West Europe', 'Southeast Asia']),
            'environment': np.random.choice(['Production', 'Development', 'Staging'])
        })

df = pd.DataFrame(cost_data)

# Add month column
df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
df['week'] = pd.to_datetime(df['date']).dt.to_period('W')

print(f"✅ Generated {len(df)} cost records")
print(f"📅 Period: {df['date'].min()} to {df['date'].max()}")
print(f"🔧 Services: {df['service'].nunique()}")
print(f"💵 Total Cost: ${df['cost'].sum():,.2f}")

print("\n📋 Sample Data:")
df.head(10)


# ============================================================================
# CELL 2: Cost Analysis and Insights
# ============================================================================
print("\n" + "=" * 70)
print("📊 COST ANALYSIS")
print("=" * 70)

# Total cost by service
print("\n1️⃣ COST BY SERVICE:")
service_costs = df.groupby('service')['cost'].sum().sort_values(ascending=False)
for service, cost in service_costs.items():
    pct = (cost / service_costs.sum()) * 100
    print(f"  {service:20s}: ${cost:10,.2f} ({pct:5.1f}%)")

# Monthly trend
print("\n2️⃣ MONTHLY COST TREND:")
monthly_costs = df.groupby('month')['cost'].sum()
for month, cost in monthly_costs.items():
    print(f"  {month}: ${cost:,.2f}")

# Calculate month-over-month growth
if len(monthly_costs) > 1:
    mom_growth = ((monthly_costs.iloc[-1] - monthly_costs.iloc[0]) / monthly_costs.iloc[0] * 100)
    print(f"\n  📈 Growth: {mom_growth:+.1f}% over period")

# Cost by environment
print("\n3️⃣ COST BY ENVIRONMENT:")
env_costs = df.groupby('environment')['cost'].sum().sort_values(ascending=False)
for env, cost in env_costs.items():
    pct = (cost / env_costs.sum()) * 100
    print(f"  {env:15s}: ${cost:10,.2f} ({pct:5.1f}%)")


# ============================================================================
# CELL 3: Create Comprehensive Dashboard (Part 1)
# ============================================================================
print("\n" + "=" * 70)
print("📊 CREATING VISUALIZATION DASHBOARD - PART 1")
print("=" * 70)

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Chart 1: Daily Cost Trend (Line Chart)
ax1 = fig.add_subplot(gs[0, :])
daily_total = df.groupby('date')['cost'].sum()
ax1.plot(daily_total.index, daily_total.values, linewidth=2, color='#0078D4', marker='o', markersize=3)
ax1.fill_between(daily_total.index, daily_total.values, alpha=0.3, color='#0078D4')
ax1.set_title('Daily Azure Cost Trend', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('Date', fontsize=11)
ax1.set_ylabel('Daily Cost ($)', fontsize=11)
ax1.grid(alpha=0.3, linestyle='--')

# Add 7-day moving average
rolling_avg = daily_total.rolling(window=7).mean()
ax1.plot(daily_total.index, rolling_avg, linewidth=2, color='#FF6B6B', 
         linestyle='--', label='7-day Moving Avg')
ax1.legend(fontsize=10)

# Add annotations
max_day = daily_total.idxmax()
ax1.annotate(f'Peak: ${daily_total.max():.0f}', 
             xy=(max_day, daily_total.max()),
             xytext=(10, 20), textcoords='offset points',
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

# Chart 2: Cost by Service (Horizontal Bar)
ax2 = fig.add_subplot(gs[1, 0])
service_costs_sorted = service_costs.sort_values()
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(service_costs_sorted)))
bars = ax2.barh(service_costs_sorted.index, service_costs_sorted.values, color=colors, edgecolor='black')
ax2.set_title('Total Cost by Service', fontsize=12, fontweight='bold')
ax2.set_xlabel('Cost ($)', fontsize=10)
ax2.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, service_costs_sorted.values)):
    ax2.text(value + 500, i, f'${value:,.0f}', va='center', fontsize=9, fontweight='bold')

# Chart 3: Cost Distribution (Pie Chart)
ax3 = fig.add_subplot(gs[1, 1])
top_services = service_costs.nlargest(5)
other_cost = service_costs.sum() - top_services.sum()
pie_data = pd.concat([top_services, pd.Series({'Other': other_cost})])

colors_pie = ['#0078D4', '#50E6FF', '#FFB900', '#FF8C00', '#E81123', '#C7C7C7']
wedges, texts, autotexts = ax3.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%',
                                     colors=colors_pie, startangle=90, pctdistance=0.85)
ax3.set_title('Cost Distribution by Service', fontsize=12, fontweight='bold')

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(9)

# Chart 4: Weekly Spend Pattern
ax4 = fig.add_subplot(gs[1, 2])
weekly_costs = df.groupby('week')['cost'].sum()
ax4.bar(range(len(weekly_costs)), weekly_costs.values, color='#107C10', edgecolor='black', alpha=0.7)
ax4.set_title('Weekly Cost Progression', fontsize=12, fontweight='bold')
ax4.set_xlabel('Week', fontsize=10)
ax4.set_ylabel('Cost ($)', fontsize=10)
ax4.grid(axis='y', alpha=0.3)

# Add trend line
z = np.polyfit(range(len(weekly_costs)), weekly_costs.values, 1)
p = np.poly1d(z)
ax4.plot(range(len(weekly_costs)), p(range(len(weekly_costs))), 
         "r--", linewidth=2, label=f'Trend: ${z[0]:+.0f}/week')
ax4.legend(fontsize=9)

# Chart 5: Cost by Environment (Stacked Area)
ax5 = fig.add_subplot(gs[2, 0])
env_daily = df.pivot_table(values='cost', index='date', columns='environment', aggfunc='sum', fill_value=0)
ax5.stackplot(env_daily.index, env_daily['Production'], env_daily['Development'], env_daily['Staging'],
              labels=['Production', 'Development', 'Staging'],
              colors=['#E81123', '#FFB900', '#107C10'], alpha=0.8)
ax5.set_title('Daily Cost by Environment', fontsize=12, fontweight='bold')
ax5.set_xlabel('Date', fontsize=10)
ax5.set_ylabel('Cost ($)', fontsize=10)
ax5.legend(loc='upper left', fontsize=9)
ax5.grid(alpha=0.3)

# Chart 6: Top Services Comparison (Grouped Bar)
ax6 = fig.add_subplot(gs[2, 1])
top_3_services = service_costs.nlargest(3).index
env_service_costs = df[df['service'].isin(top_3_services)].groupby(['environment', 'service'])['cost'].sum().unstack()

x = np.arange(len(env_service_costs.index))
width = 0.25
colors_bar = ['#0078D4', '#50E6FF', '#FFB900']

for i, service in enumerate(env_service_costs.columns):
    ax6.bar(x + i*width, env_service_costs[service], width, label=service, color=colors_bar[i])

ax6.set_title('Top 3 Services: Cost by Environment', fontsize=12, fontweight='bold')
ax6.set_xlabel('Environment', fontsize=10)
ax6.set_ylabel('Cost ($)', fontsize=10)
ax6.set_xticks(x + width)
ax6.set_xticklabels(env_service_costs.index)
ax6.legend(fontsize=9)
ax6.grid(axis='y', alpha=0.3)

# Chart 7: Cost Heatmap by Service and Month
ax7 = fig.add_subplot(gs[2, 2])
service_month_costs = df.pivot_table(values='cost', index='service', columns='month', aggfunc='sum', fill_value=0)
im = ax7.imshow(service_month_costs.values, cmap='YlOrRd', aspect='auto')
ax7.set_title('Cost Heatmap: Service × Month', fontsize=12, fontweight='bold')
ax7.set_xticks(range(len(service_month_costs.columns)))
ax7.set_xticklabels([str(m) for m in service_month_costs.columns], rotation=45, ha='right', fontsize=8)
ax7.set_yticks(range(len(service_month_costs.index)))
ax7.set_yticklabels(service_month_costs.index, fontsize=9)

# Add colorbar
cbar = plt.colorbar(im, ax=ax7)
cbar.set_label('Cost ($)', rotation=270, labelpad=20, fontsize=10)

plt.suptitle('Azure Cost Optimization Dashboard', fontsize=18, fontweight='bold', y=0.995)
plt.savefig('azure_cost_dashboard_part1.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Dashboard Part 1 saved as 'azure_cost_dashboard_part1.png'")


# ============================================================================
# CELL 4: Advanced Visualizations (Part 2)
# ============================================================================
print("\n" + "=" * 70)
print("📊 CREATING ADVANCED VISUALIZATIONS - PART 2")
print("=" * 70)

fig2, axes = plt.subplots(2, 2, figsize=(16, 10))
fig2.suptitle('Azure Cost Analytics - Advanced Insights', fontsize=16, fontweight='bold')

# Chart 8: Scatter Plot - Cost vs Days
ax8 = axes[0, 0]
for service in services[:4]:  # Top 4 services
    service_data = df[df['service'] == service]
    daily_service = service_data.groupby('date')['cost'].sum()
    ax8.scatter(range(len(daily_service)), daily_service.values, 
               label=service, alpha=0.6, s=30)

ax8.set_title('Cost Trends: Top 4 Services', fontsize=12, fontweight='bold')
ax8.set_xlabel('Days', fontsize=10)
ax8.set_ylabel('Daily Cost ($)', fontsize=10)
ax8.legend(fontsize=9)
ax8.grid(alpha=0.3)

# Chart 9: Box Plot - Cost Distribution by Service
ax9 = axes[0, 1]
service_data_for_box = [df[df['service'] == s]['cost'].values for s in services]
bp = ax9.boxplot(service_data_for_box, labels=services, patch_artist=True)

for patch, color in zip(bp['boxes'], plt.cm.Set3(range(len(services)))):
    patch.set_facecolor(color)

ax9.set_title('Cost Distribution by Service', fontsize=12, fontweight='bold')
ax9.set_ylabel('Cost ($)', fontsize=10)
ax9.tick_params(axis='x', rotation=45)
ax9.grid(axis='y', alpha=0.3)

# Chart 10: Histogram - Daily Cost Distribution
ax10 = axes[1, 0]
daily_totals = df.groupby('date')['cost'].sum()
ax10.hist(daily_totals.values, bins=20, color='#0078D4', edgecolor='black', alpha=0.7)
ax10.axvline(daily_totals.mean(), color='red', linestyle='--', linewidth=2, 
            label=f'Mean: ${daily_totals.mean():.0f}')
ax10.axvline(daily_totals.median(), color='green', linestyle='--', linewidth=2,
            label=f'Median: ${daily_totals.median():.0f}')
ax10.set_title('Daily Cost Distribution', fontsize=12, fontweight='bold')
ax10.set_xlabel('Daily Cost ($)', fontsize=10)
ax10.set_ylabel('Frequency', fontsize=10)
ax10.legend(fontsize=9)
ax10.grid(axis='y', alpha=0.3)

# Chart 11: Region Comparison (Radar/Spider Chart alternative - Stacked Bar)
ax11 = axes[1, 1]
region_costs = df.groupby(['region', 'environment'])['cost'].sum().unstack(fill_value=0)
region_costs.plot(kind='bar', stacked=True, ax=ax11, 
                 color=['#E81123', '#FFB900', '#107C10'], edgecolor='black')
ax11.set_title('Cost by Region and Environment', fontsize=12, fontweight='bold')
ax11.set_xlabel('Region', fontsize=10)
ax11.set_ylabel('Total Cost ($)', fontsize=10)
ax11.tick_params(axis='x', rotation=45)
ax11.legend(title='Environment', fontsize=9)
ax11.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('azure_cost_dashboard_part2.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Dashboard Part 2 saved as 'azure_cost_dashboard_part2.png'")


# ============================================================================
# CELL 5: Cost Anomaly Detection
# ============================================================================
print("\n" + "=" * 70)
print("🔍 COST ANOMALY DETECTION")
print("=" * 70)

# Calculate daily totals and detect anomalies
daily_costs = df.groupby('date')['cost'].sum().reset_index()
daily_costs['cost_ma7'] = daily_costs['cost'].rolling(window=7).mean()
daily_costs['cost_std7'] = daily_costs['cost'].rolling(window=7).std()

# Define anomaly as >2 std deviations from moving average
daily_costs['is_anomaly'] = abs(daily_costs['cost'] - daily_costs['cost_ma7']) > (2 * daily_costs['cost_std7'])

anomalies = daily_costs[daily_costs['is_anomaly'] == True]

if len(anomalies) > 0:
    print(f"⚠️  {len(anomalies)} cost anomalies detected:\n")
    for _, row in anomalies.iterrows():
        deviation = ((row['cost'] - row['cost_ma7']) / row['cost_ma7'] * 100)
        print(f"  {row['date']}: ${row['cost']:.2f} ({deviation:+.1f}% from avg)")
    
    # Find services contributing to anomalies
    print("\n📊 Services contributing to anomalies:")
    for date in anomalies['date'].values:
        day_costs = df[df['date'] == date].groupby('service')['cost'].sum().sort_values(ascending=False)
        print(f"\n  {date}:")
        for service, cost in day_costs.head(3).items():
            print(f"    {service}: ${cost:.2f}")
else:
    print("✅ No significant cost anomalies detected")


# ============================================================================
# CELL 6: Cost Forecasting
# ============================================================================
print("\n" + "=" * 70)
print("📈 COST FORECASTING")
print("=" * 70)

# Simple linear regression for forecast
from numpy.polynomial import polynomial as P

daily_total_costs = df.groupby('date')['cost'].sum()
x = np.arange(len(daily_total_costs))
y = daily_total_costs.values

# Fit polynomial (degree 1 = linear)
coefs = P.polyfit(x, y, 1)
trend = P.polyval(x, coefs)

# Forecast next 30 days
forecast_days = 30
future_x = np.arange(len(daily_total_costs), len(daily_total_costs) + forecast_days)
forecast = P.polyval(future_x, coefs)

print(f"📊 Current daily average: ${daily_total_costs.mean():.2f}")
print(f"📈 Trend: ${coefs[1]:+.2f} per day")
print(f"\n🔮 30-Day Forecast:")
print(f"  Projected daily cost (Day 30): ${forecast[-1]:.2f}")
print(f"  Projected monthly total: ${forecast.sum():.2f}")
print(f"  Expected increase: ${(forecast.sum() - daily_total_costs.sum()):,.2f}")

# Visualize forecast
plt.figure(figsize=(14, 6))
plt.plot(daily_total_costs.index, daily_total_costs.values, 
         label='Historical', linewidth=2, color='#0078D4')
plt.plot(daily_total_costs.index, trend, 
         label='Trend', linewidth=2, linestyle='--', color='#FF6B6B')

# Plot forecast
forecast_dates = [daily_total_costs.index[-1] + timedelta(days=i+1) for i in range(forecast_days)]
plt.plot(forecast_dates, forecast, 
         label='Forecast', linewidth=2, linestyle='--', color='#107C10')
plt.fill_between(forecast_dates, forecast, alpha=0.3, color='#107C10')

plt.title('Azure Cost Forecast (30 Days)', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=11)
plt.ylabel('Daily Cost ($)', fontsize=11)
plt.legend(fontsize=10)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('cost_forecast.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ Forecast chart saved as 'cost_forecast.png'")


# ============================================================================
# CELL 7: Generate Optimization Recommendations
# ============================================================================
print("\n" + "=" * 70)
print("💡 COST OPTIMIZATION RECOMMENDATIONS")
print("=" * 70)

recommendations = []

# 1. Check for high-cost services
for service, cost in service_costs.items():
    pct_of_total = (cost / service_costs.sum()) * 100
    if pct_of_total > 20:
        recommendations.append({
            'Priority': 'HIGH',
            'Category': 'Resource Optimization',
            'Service': service,
            'Issue': f'{pct_of_total:.1f}% of total cost',
            'Potential_Savings': f'${cost * 0.15:.2f}',
            'Action': 'Review resource sizing, implement auto-scaling, consider reserved instances'
        })

# 2. Weekend usage (potential savings)
weekend_costs = df[pd.to_datetime(df['date']).dt.dayofweek >= 5].groupby('service')['cost'].sum()
weekday_costs = df[pd.to_datetime(df['date']).dt.dayofweek < 5].groupby('service')['cost'].sum()

for service in services:
    if service in weekend_costs.index and service in weekday_costs.index:
        weekend_avg = weekend_costs[service] / 26  # ~26 weekend days
        weekday_avg = weekday_costs[service] / 64  # ~64 weekday days
        
        if weekend_avg > weekday_avg * 0.5:  # Weekend usage > 50% of weekday
            potential_savings = weekend_costs[service] * 0.6
            recommendations.append({
                'Priority': 'MEDIUM',
                'Category': 'Schedule Optimization',
                'Service': service,
                'Issue': 'High weekend usage detected',
                'Potential_Savings': f'${potential_savings:.2f}',
                'Action': 'Implement auto-shutdown policies for non-production resources on weekends'
            })

# 3. Development environment costs
dev_costs = df[df['environment'] == 'Development'].groupby('service')['cost'].sum()
for service, cost in dev_costs.items():
    if cost > service_costs[service] * 0.3:  # Dev costs > 30% of total service cost
        potential_savings = cost * 0.5
        recommendations.append({
            'Priority': 'MEDIUM',
            'Category': 'Environment Optimization',
            'Service': service,
            'Issue': f'Dev environment: ${cost:.2f} ({cost/service_costs[service]*100:.1f}% of {service})',
            'Potential_Savings': f'${potential_savings:.2f}',
            'Action': 'Use smaller SKUs for dev, implement auto-shutdown during off-hours'
        })

# 4. Growing costs
if len(monthly_costs) >= 2:
    first_month_cost = monthly_costs.iloc[0]
    last_month_cost = monthly_costs.iloc[-1]
    growth_rate = ((last_month_cost - first_month_cost) / first_month_cost * 100)
    
    if growth_rate > 10:
        recommendations.append({
            'Priority': 'HIGH',
            'Category': 'Cost Governance',
            'Service': 'All Services',
            'Issue': f'Cost growth: {growth_rate:+.1f}% over period',
            'Potential_Savings': f'${last_month_cost * 0.1:.2f}',
            'Action': 'Implement Azure Budgets, enable cost alerts, review resource tagging'
        })

# Display recommendations
if recommendations:
    df_recommendations = pd.DataFrame(recommendations)
    df_recommendations = df_recommendations.sort_values('Priority', ascending=True)
    
    print(f"\n🎯 {len(recommendations)} Optimization Opportunities Found:\n")
    display(df_recommendations)
    
    # Calculate total potential savings
    total_savings = sum([float(r['Potential_Savings'].replace('$', '').replace(',', '')) 
                        for r in recommendations])
    
    print(f"\n💰 TOTAL POTENTIAL SAVINGS: ${total_savings:,.2f}/month (${total_savings*12:,.2f}/year)")
    print(f"📊 ROI: {(total_savings/monthly_costs.mean()*100):.1f}% monthly cost reduction")
    
    # Export to CSV
    df_recommendations.to_csv('cost_optimization_recommendations.csv', index=False)
    print("\n✅ Recommendations saved to 'cost_optimization_recommendations.csv'")
else:
    print("\n✅ Cost management is optimal - no major recommendations")


# ============================================================================
# CELL 8: Executive Summary Report
# ============================================================================
print("\n" + "=" * 70)
print("📋 EXECUTIVE SUMMARY REPORT")
print("=" * 70)

total_cost = df['cost'].sum()
avg_daily_cost = df.groupby('date')['cost'].sum().mean()
peak_daily_cost = df.groupby('date')['cost'].sum().max()

report = f"""
╔═══════════════════════════════════════════════════════════════════╗
║           AZURE COST OPTIMIZATION EXECUTIVE SUMMARY              ║
╚═══════════════════════════════════════════════════════════════════╝

📅 REPORTING PERIOD: {df['date'].min()} to {df['date'].max()} ({num_days} days)

💰 COST OVERVIEW:
   • Total Spend: ${total_cost:,.2f}
   • Average Daily Cost: ${avg_daily_cost:,.2f}
   • Peak Daily Cost: ${peak_daily_cost:,.2f}
   • Projected Monthly: ${avg_daily_cost * 30:,.2f}

📊 TOP 3 COST DRIVERS:
"""

for i, (service, cost) in enumerate(service_costs.head(3).items(), 1):
    pct = (cost / total_cost) * 100
    report += f"   {i}. {service}: ${cost:,.2f} ({pct:.1f}%)\n"

report += f"""
🏢 ENVIRONMENT BREAKDOWN:
"""

for env, cost in env_costs.items():
    pct = (cost / total_cost) * 100
    report += f"   • {env}: ${cost:,.2f} ({pct:.1f}%)\n"

report += f"""
📈 TRENDS:
   • Month-over-Month Growth: {mom_growth:+.1f}%
   • Cost Anomalies Detected: {len(anomalies)}
   • 30-Day Forecast: ${forecast.sum():,.2f}

💡 OPTIMIZATION OPPORTUNITIES:
   • Recommendations: {len(recommendations)}
   • Potential Monthly Savings: ${total_savings:,.2f}
   • Potential Annual Savings: ${total_savings * 12:,.2f}
   • ROI: {(total_savings/monthly_costs.mean()*100):.1f}% cost reduction

🎯 PRIORITY ACTIONS:
"""

high_priority = [r for r in recommendations if r['Priority'] == 'HIGH']
for i, rec in enumerate(high_priority[:3], 1):
    report += f"   {i}. {rec['Category']}: {rec['Action']}\n"

report += f"""
📁 GENERATED REPORTS:
   • azure_cost_dashboard_part1.png - Comprehensive dashboard
   • azure_cost_dashboard_part2.png - Advanced analytics
   • cost_forecast.png - 30-day cost projection
   • cost_optimization_recommendations.csv - Detailed recommendations

═══════════════════════════════════════════════════════════════════
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
═══════════════════════════════════════════════════════════════════
"""

print(report)

# Save report to file
with open('executive_cost_summary.txt', 'w') as f:
    f.write(report)

print("✅ Executive summary saved to 'executive_cost_summary.txt'")

print("\n" + "=" * 70)
print("🎓 LAB 4 COMPLETE!")
print("=" * 70)
print("\nSkills Demonstrated:")
print("  ✅ Multiple chart types (line, bar, pie, scatter, box, heatmap)")
print("  ✅ Advanced visualization techniques")
print("  ✅ Statistical analysis and forecasting")
print("  ✅ Anomaly detection")
print("  ✅ Data-driven insights generation")
print("  ✅ Executive reporting")
print("=" * 70)