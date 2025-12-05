# Project 2: Azure Security Alert Analyzer
# Problem: Analyze Azure Security Center alerts to prioritize threats
# Solution: Use NumPy to process security scores and identify critical risks

# Import NumPy library for numerical operations
import numpy as np

print("=" * 70)
print("AZURE SECURITY CENTER - THREAT ANALYSIS DASHBOARD")
print("=" * 70)

# --- Creating NumPy Arrays ---
# np.array(): Create array from Python list
# Security severity scores (0-100) for different resources
security_scores = np.array([85, 42, 91, 38, 76, 95, 29, 88, 45, 82])

# Failed login attempts per resource (suspicious activity indicator)
failed_logins = np.array([3, 45, 1, 78, 12, 0, 102, 5, 38, 8])

# Open ports detected on each resource
open_ports = np.array([22, 135, 22, 3389, 80, 443, 3389, 22, 445, 80])

# Days since last security patch applied
days_since_patch = np.array([5, 45, 3, 89, 22, 1, 120, 10, 67, 8])

# Resource names (for reference)
resource_names = np.array([
    "web-vm-01", "db-vm-01", "web-vm-02", "legacy-vm", 
    "app-vm-01", "api-vm-01", "old-test-vm", "web-vm-03",
    "file-server", "app-vm-02"
])


# --- Basic NumPy Operations ---
print("\n--- OVERALL SECURITY METRICS ---")

# Calculate mean: average security score across all resources
mean_score = np.mean(security_scores)
print(f"Average Security Score: {mean_score:.2f}/100")

# Calculate median: middle value, less affected by outliers
median_score = np.median(security_scores)
print(f"Median Security Score: {median_score:.2f}/100")

# Calculate standard deviation: measure of score variation
std_score = np.std(security_scores)
print(f"Score Standard Deviation: {std_score:.2f}")

# Find minimum and maximum scores
min_score = np.min(security_scores)
max_score = np.max(security_scores)
print(f"Lowest Security Score: {min_score}")
print(f"Highest Security Score: {max_score}")

# Count total resources being monitored
total_resources = len(security_scores)
print(f"Total Resources Monitored: {total_resources}")


# --- Array Indexing ---
print("\n--- CRITICAL RESOURCES (Indexing Examples) ---")

# Index 0: Access first element
print(f"First Resource: {resource_names[0]} - Score: {security_scores[0]}")

# Index -1: Access last element
print(f"Last Resource: {resource_names[-1]} - Score: {security_scores[-1]}")

# Index 3: Access specific element (4th resource)
print(f"Resource at index 3: {resource_names[3]} - Score: {security_scores[3]}")


# --- Array Slicing ---
print("\n--- RESOURCE GROUPS (Slicing Examples) ---")

# Slice [0:3]: Get first 3 resources
print("First 3 Resources:")
print(f"  Names: {resource_names[0:3]}")
print(f"  Scores: {security_scores[0:3]}")

# Slice [5:]: Get resources from index 5 to end
print("\nResources from index 5 onwards:")
print(f"  Names: {resource_names[5:]}")
print(f"  Scores: {security_scores[5:]}")

# Slice [:4]: Get first 4 resources
print("\nFirst 4 Resources:")
print(f"  Failed Logins: {failed_logins[:4]}")

# Slice [-3:]: Get last 3 resources
print("\nLast 3 Resources:")
print(f"  Days Since Patch: {days_since_patch[-3:]}")


# --- Boolean Indexing (Advanced Filtering) ---
print("\n" + "=" * 70)
print("🚨 THREAT IDENTIFICATION")
print("=" * 70)

# Create boolean mask: Find resources with score < 50 (critical threshold)
critical_mask = security_scores < 50
print(f"\nCritical Security Score Resources (< 50):")
print(f"  Resources: {resource_names[critical_mask]}")
print(f"  Scores: {security_scores[critical_mask]}")
print(f"  Count: {np.sum(critical_mask)}")  # np.sum counts True values

# Find resources with excessive failed logins (> 30)
login_threat_mask = failed_logins > 30
print(f"\nResources with Excessive Failed Logins (> 30):")
print(f"  Resources: {resource_names[login_threat_mask]}")
print(f"  Failed Attempts: {failed_logins[login_threat_mask]}")
print(f"  Count: {np.sum(login_threat_mask)}")

# Find resources with risky open ports (3389=RDP, 445=SMB)
risky_ports_mask = (open_ports == 3389) | (open_ports == 445)  # | is OR operator
print(f"\nResources with Risky Ports (RDP/SMB):")
print(f"  Resources: {resource_names[risky_ports_mask]}")
print(f"  Ports: {open_ports[risky_ports_mask]}")

# Find outdated systems (not patched in 60+ days)
outdated_mask = days_since_patch > 60
print(f"\nOutdated Resources (60+ days without patch):")
print(f"  Resources: {resource_names[outdated_mask]}")
print(f"  Days: {days_since_patch[outdated_mask]}")


# --- Array Arithmetic Operations ---
print("\n" + "=" * 70)
print("RISK SCORE CALCULATIONS")
print("=" * 70)

# Calculate inverse security score (100 - score = risk)
# Higher risk score = more dangerous
risk_scores = 100 - security_scores
print(f"\nRisk Scores (100 - Security Score):")
print(f"  {risk_scores}")

# Normalize failed logins to 0-100 scale
# Divide by max value and multiply by 100
max_logins = np.max(failed_logins)
normalized_logins = (failed_logins / max_logins) * 100
print(f"\nNormalized Login Threat Scores (0-100):")
print(f"  {normalized_logins.astype(int)}")  # .astype(int) converts to integers

# Calculate composite threat score
# Formula: (Risk Score * 0.4) + (Login Threat * 0.3) + (Patch Delay * 0.3)
normalized_patch = (days_since_patch / np.max(days_since_patch)) * 100
composite_threat = (risk_scores * 0.4) + (normalized_logins * 0.3) + (normalized_patch * 0.3)

print(f"\nComposite Threat Scores:")
for i in range(len(resource_names)):
    print(f"  {resource_names[i]}: {composite_threat[i]:.2f}")


# --- Finding Top Threats ---
print("\n" + "=" * 70)
print("🎯 TOP 3 CRITICAL THREATS")
print("=" * 70)

# np.argsort(): Returns indices that would sort array
# [-3:]: Get last 3 indices (highest values)
# [::-1]: Reverse to get descending order
top_threat_indices = np.argsort(composite_threat)[-3:][::-1]

for rank, idx in enumerate(top_threat_indices, 1):
    print(f"\n#{rank} - {resource_names[idx]}")
    print(f"  Composite Threat Score: {composite_threat[idx]:.2f}")
    print(f"  Security Score: {security_scores[idx]}/100")
    print(f"  Failed Logins: {failed_logins[idx]}")
    print(f"  Open Port: {open_ports[idx]}")
    print(f"  Days Since Patch: {days_since_patch[idx]}")


# --- Statistical Summary ---
print("\n" + "=" * 70)
print("SECURITY POSTURE SUMMARY")
print("=" * 70)

# Count resources in different risk categories
high_risk_count = np.sum(composite_threat > 60)
medium_risk_count = np.sum((composite_threat >= 30) & (composite_threat <= 60))
low_risk_count = np.sum(composite_threat < 30)

print(f"\nRisk Distribution:")
print(f"  🔴 High Risk (>60): {high_risk_count} resources")
print(f"  🟡 Medium Risk (30-60): {medium_risk_count} resources")
print(f"  🟢 Low Risk (<30): {low_risk_count} resources")

# Calculate percentage of compliant resources (score > 70)
compliant_resources = np.sum(security_scores > 70)
compliance_rate = (compliant_resources / total_resources) * 100
print(f"\nCompliance Rate: {compliance_rate:.1f}%")
print(f"  ({compliant_resources}/{total_resources} resources with score > 70)")

print("\n" + "=" * 70)
print("⚠️  RECOMMENDATION: Prioritize patching and hardening top 3 threats")
print("=" * 70)