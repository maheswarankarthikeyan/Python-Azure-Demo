# Project 1: Azure VM Cost Optimizer
# Problem: Identify underutilized VMs to reduce monthly Azure costs
# Solution: Analyze CPU usage and recommend VM actions (downsize/stop)

# --- Variables and Basic Data Types ---
# string: VM name identifier
vm_name = "prod-web-vm-01"

# int: number of days monitored
monitoring_days = 30

# float: average CPU utilization percentage
avg_cpu_usage = 12.5

# float: monthly cost in USD
monthly_cost = 245.00

# boolean: check if VM is in production environment
is_production = True

# list: CPU usage samples over time (percentages)
cpu_samples = [8.2, 15.3, 10.1, 12.8, 9.4, 14.2, 11.5, 13.1]

# dictionary: VM configuration details
vm_config = {
    "name": "prod-web-vm-01",
    "size": "Standard_D4s_v3",
    "region": "East US",
    "monthly_cost": 245.00,
    "cpu_cores": 4
}

# tuple: cost thresholds (low, medium, high) - immutable
cost_thresholds = (100.0, 250.0, 500.0)


# --- Functions ---
def calculate_potential_savings(current_cost, reduction_percentage):
    """
    Calculate potential monthly savings
    Parameters: 
        current_cost (float): Current monthly VM cost
        reduction_percentage (float): Percentage to reduce (0-1)
    Returns: 
        savings (float): Monthly savings amount
    """
    # arithmetic operators: multiplication and subtraction
    savings = current_cost * reduction_percentage
    return savings


def recommend_action(cpu_avg, is_prod):
    """
    Recommend action based on CPU usage and environment
    Parameters:
        cpu_avg (float): Average CPU percentage
        is_prod (bool): Whether VM is in production
    Returns:
        recommendation (string): Action to take
    """
    # Control Flow: if/elif/else with comparison operators
    
    # comparison operator: less than (<)
    if cpu_avg < 10:
        # logical operator: 'not' to check non-production
        if not is_prod:
            return "STOP - Extremely underutilized"
        else:
            return "DOWNSIZE - Consider smaller VM size"
    
    # comparison operators: >= and <
    elif cpu_avg >= 10 and cpu_avg < 20:
        return "REVIEW - Low utilization, monitor closely"
    
    # comparison operator: >= and <
    elif cpu_avg >= 20 and cpu_avg < 60:
        return "OPTIMAL - Good utilization"
    
    else:
        return "ALERT - High utilization, consider scaling up"


def calculate_average(values):
    """
    Calculate average from a list of values
    Parameters: values (list of floats)
    Returns: average (float)
    """
    total = 0
    # for loop: iterate through list
    for value in values:
        # arithmetic operator: addition (+=)
        total += value
    
    # arithmetic operator: division
    average = total / len(values)
    return average


# --- Main Analysis Logic ---
print("=" * 60)
print("AZURE VM COST OPTIMIZATION REPORT")
print("=" * 60)

# Display VM details from dictionary
print(f"\nVM Name: {vm_config['name']}")
print(f"VM Size: {vm_config['size']}")
print(f"Region: {vm_config['region']}")
print(f"CPU Cores: {vm_config['cpu_cores']}")
print(f"Monthly Cost: ${vm_config['monthly_cost']:.2f}")

# Calculate actual average from samples
calculated_avg = calculate_average(cpu_samples)
print(f"\nAverage CPU Usage: {calculated_avg:.2f}%")
print(f"Monitoring Period: {monitoring_days} days")

# Get recommendation by calling function
recommendation = recommend_action(calculated_avg, is_production)
print(f"\n>>> RECOMMENDATION: {recommendation}")

# --- Cost Analysis with Control Flow ---
print("\n" + "-" * 60)
print("COST IMPACT ANALYSIS")
print("-" * 60)

# comparison operator: check if underutilized
if calculated_avg < 20:
    print("⚠️  VM is UNDERUTILIZED!")
    
    # Calculate savings for different scenarios
    # 50% savings if downsizing
    downsize_savings = calculate_potential_savings(monthly_cost, 0.50)
    # 100% savings if stopping
    stop_savings = calculate_potential_savings(monthly_cost, 1.0)
    
    print(f"\nPotential Monthly Savings:")
    print(f"  - If Downsized (50%): ${downsize_savings:.2f}")
    print(f"  - If Stopped (100%): ${stop_savings:.2f}")
    
    # arithmetic operator: multiplication for annual savings
    annual_savings = downsize_savings * 12
    print(f"  - Annual Savings (Downsize): ${annual_savings:.2f}")

else:
    print("✓ VM utilization is acceptable")

# --- Working with Tuples ---
# Unpack tuple values
low_threshold, medium_threshold, high_threshold = cost_thresholds

print(f"\n" + "-" * 60)
print("COST CATEGORY ANALYSIS")
print("-" * 60)

# Control flow: categorize VM by cost using elif
if monthly_cost < low_threshold:
    cost_category = "Low Cost"
    priority = "Monitor quarterly"
elif monthly_cost >= low_threshold and monthly_cost < medium_threshold:
    cost_category = "Medium Cost"
    priority = "Monitor monthly"
elif monthly_cost >= medium_threshold and monthly_cost < high_threshold:
    cost_category = "High Cost"
    priority = "Monitor weekly"
else:
    cost_category = "Very High Cost"
    priority = "Monitor daily"

print(f"Cost Category: {cost_category}")
print(f"Review Priority: {priority}")

# --- Multiple VMs Analysis with While Loop ---
print("\n" + "=" * 60)
print("BATCH VM ANALYSIS")
print("=" * 60)

# list: multiple VMs to analyze
vm_list = [
    {"name": "dev-vm-01", "cpu": 8.5, "cost": 120.00},
    {"name": "prod-db-vm", "cpu": 45.2, "cost": 380.00},
    {"name": "test-vm-03", "cpu": 5.1, "cost": 95.00},
]

# while loop: process VMs using index
index = 0
total_wasted_cost = 0

# comparison operator: less than
while index < len(vm_list):
    vm = vm_list[index]
    
    print(f"\nAnalyzing: {vm['name']}")
    print(f"  CPU: {vm['cpu']}% | Cost: ${vm['cost']:.2f}")
    
    # logical operator: 'and' to combine conditions
    if vm['cpu'] < 15 and vm['cost'] > 50:
        waste = calculate_potential_savings(vm['cost'], 0.5)
        # arithmetic operator: addition (+=)
        total_wasted_cost += waste
        print(f"  ⚠️  Wasting: ${waste:.2f}/month")
    else:
        print(f"  ✓ Efficiently utilized")
    
    # arithmetic operator: increment
    index += 1

print(f"\n>>> Total Potential Monthly Savings: ${total_wasted_cost:.2f}")
print(f">>> Annual Savings Opportunity: ${total_wasted_cost * 12:.2f}")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)