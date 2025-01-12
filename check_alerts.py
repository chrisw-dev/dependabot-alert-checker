#!/usr/bin/env python3
import os
from datetime import datetime, timezone
from github import Github
import sys

def get_alert_age(created_at):
    """Calculate the age of an alert in days"""
    now = datetime.now(timezone.utc)
    age = now - created_at
    return age.days

def get_thresholds_from_env():
    """Get threshold values from environment variables"""
    return {
        'CRITICAL': int(os.getenv('INPUT_CRITICAL_THRESHOLD', '3')),
        'HIGH': int(os.getenv('INPUT_HIGH_THRESHOLD', '5')),
        'MEDIUM': int(os.getenv('INPUT_MEDIUM_THRESHOLD', '14')),
        'LOW': int(os.getenv('INPUT_LOW_THRESHOLD', '30'))
    }

def check_alerts():
    # Initialize GitHub client
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN not found")
        sys.exit(1)
    
    g = Github(token)
    
    # Get repository from environment
    repo_name = os.getenv('GITHUB_REPOSITORY')
    print(f"Checking alerts for repository: {repo_name}")
    repo = g.get_repo(repo_name)
    print(f"Repository: {repo.full_name}")
    
    # Get thresholds from environment variables
    ALERT_THRESHOLDS = get_thresholds_from_env()
    
    # Get all open dependabot alerts
    alerts = repo.get_dependabot_alerts()
    
    violations = []
    all_alerts = []
    
    for alert in alerts:
        if not alert.state == "open":
            continue
            
        severity = alert.security_advisory.severity.upper()
        age = get_alert_age(alert.created_at)
        threshold = ALERT_THRESHOLDS.get(severity)
        
        alert_info = {
            'package': alert.security_advisory.package.name,
            'severity': severity,
            'age_days': age,
            'threshold_days': threshold,
            'url': alert.html_url,
            'title': alert.security_advisory.summary,
            'created_at': alert.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')
        }
        
        all_alerts.append(alert_info)
        
        if age > threshold:
            violations.append(alert_info)
    
    # Print summary as GitHub Actions output
    print("\n## Dependabot Alert Summary")
    print(f"Total open alerts: {len(all_alerts)}")
    print(f"Alerts exceeding age threshold: {len(violations)}")
    
    if all_alerts:
        print("\n### All Open Alerts")
        for alert in all_alerts:
            print(f"\n#### {alert['package']}: {alert['title']}")
            print(f"- **Severity:** {alert['severity']}")
            print(f"- **Age:** {alert['age_days']} days")
            print(f"- **Threshold:** {alert['threshold_days']} days")
            print(f"- **Created:** {alert['created_at']}")
            print(f"- **URL:** {alert['url']}")
    
    if violations:
        print("\n### :x: Violations (Alerts exceeding threshold)")
        for violation in violations:
            print(f"\n#### {violation['package']}: {violation['title']}")
            print(f"- **Severity:** {violation['severity']}")
            print(f"- **Age:** {violation['age_days']} days (Threshold: {violation['threshold_days']} days)")
            print(f"- **Created:** {violation['created_at']}")
            print(f"- **URL:** {violation['url']}")
        
        print("\n:no_entry: Action failed due to alerts exceeding age thresholds")
        sys.exit(1)
    else:
        print("\n:white_check_mark: All alerts are within acceptable age thresholds")
        sys.exit(0)

if __name__ == "__main__":
    check_alerts()
