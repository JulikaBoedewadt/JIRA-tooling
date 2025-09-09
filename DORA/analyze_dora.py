#!/usr/bin/env python3
"""
Unified DORA Metrics Analyzer
============================

This script provides a complete DORA metrics analysis workflow.
It automatically fetches data and runs analysis with just project name and key.

Usage:
    python3 analyze_dora.py --project-name "Your Project" --project-key "YOUR_PROJECT"

Requirements:
    - MCP tools for Atlassian integration (run in Cursor IDE)
    - python-dateutil package
"""

import json
import argparse
import subprocess
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional

def check_mcp_available() -> bool:
    """Check if MCP tools are available"""
    try:
        # Try to call MCP function to check availability
        mcp_Atlassian-MCP-Server_getAccessibleAtlassianResources(random_string="check")
        return True
    except NameError:
        return False
    except Exception:
        return False

def fetch_jira_data(project_key: str) -> Optional[Dict[str, Any]]:
    """
    Fetch JIRA data for a project using MCP tools.
    Returns None if MCP tools are not available.
    """
    print(f"🔍 Fetching data for project: {project_key}")
    
    if not check_mcp_available():
        print("❌ MCP tools not available. Please run this script in Cursor IDE.")
        return None
    
    try:
        # Get accessible Atlassian resources
        print("🔍 Getting accessible Atlassian resources...")
        resources = mcp_Atlassian-MCP-Server_getAccessibleAtlassianResources(random_string="check")
        
        if not resources or not resources.get('resources'):
            print("❌ No accessible Atlassian resources found")
            return None
        
        # Get the first available cloud ID
        cloud_id = resources['resources'][0]['id']
        print(f"✅ Using cloud ID: {cloud_id}")
        
        # Search for issues in the project that were closed with status "Done" in the last 30 days
        jql_query = f"project = {project_key} AND status = Done AND resolved >= -30d ORDER BY resolved DESC"
        print(f"🔍 Searching for issues with JQL: {jql_query}")
        
        # Search JIRA issues using MCP tool
        search_result = mcp_Atlassian-MCP-Server_searchJiraIssuesUsingJql(
            cloudId=cloud_id,
            jql=jql_query,
            maxResults=100,
            fields=["key", "summary", "issuetype", "created", "resolutiondate", "priority", "status"]
        )
        
        if not search_result or not search_result.get('issues'):
            print(f"❌ No issues found for project {project_key}")
            return None
        
        issues = search_result['issues']
        print(f"✅ Found {len(issues)} issues closed with 'Done' status in the last 30 days for project {project_key}")
        
        # Create data structure
        data = {
            "project_key": project_key,
            "fetched_at": datetime.now().isoformat(),
            "data_source": "Real JIRA Data (MCP) - Last 30 days (Done status)",
            "total_issues": len(issues),
            "issues": issues
        }
        
        return data
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

def save_data(data: Dict[str, Any], filename: str) -> bool:
    """Save the fetched data to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"💾 Data saved to: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving data: {e}")
        return False

def run_dora_analysis(project_name: str, project_key: str) -> bool:
    """Run the DORA metrics analysis"""
    print(f"📊 Running DORA analysis for: {project_name}")
    
    try:
        # Run the DORA metrics script
        cmd = [
            "python3", "dora_metrics.py",
            "--project-name", project_name,
            "--project-key", project_key
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Analysis completed successfully!")
            print("\n" + "="*80)
            print("📋 DORA METRICS RESULTS:")
            print("="*80)
            print(result.stdout)
            return True
        else:
            print(f"❌ Analysis failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return False

def main():
    """Main unified workflow function"""
    parser = argparse.ArgumentParser(
        description="Unified DORA Metrics Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 analyze_dora.py --project-name "My Project" --project-key "PROJ"
  python3 analyze_dora.py --project-name "Terminvereinbarung" --project-key "TEV"
  python3 analyze_dora.py --project-name "E-commerce" --project-key "ECP"
        """
    )
    
    parser.add_argument("--project-name", required=True,
                       help="Project name for display")
    parser.add_argument("--project-key", required=True,
                       help="JIRA project key (e.g., TEV, ECP, MAP)")
    
    args = parser.parse_args()
    
    print("🚀 Unified DORA Metrics Analyzer")
    print("=" * 50)
    print(f"🏷️  Project: {args.project_name} ({args.project_key})")
    print()
    
    # Step 1: Try to fetch fresh data, fallback to existing data
    print("🔄 Fetching fresh data...")
    data = fetch_jira_data(args.project_key)
    
    if not data:
        print("⚠️  MCP tools not available, trying to use existing data...")
        data_file = f"tmp/dora_metrics_{args.project_key.lower()}_data.json"
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                print(f"✅ Using existing data from {data_file}")
                print(f"📅 Data fetched at: {data.get('fetched_at', 'Unknown')}")
                print(f"📊 Issues in file: {data.get('total_issues', 0)}")
            except Exception as e:
                print(f"❌ Error loading existing data: {e}")
                return 1
        else:
            print("❌ No data available for analysis.")
            return 1
    else:
        # Save the fresh data
        data_file = f"tmp/dora_metrics_{args.project_key.lower()}_data.json"
        if not save_data(data, data_file):
            print("❌ Failed to save data.")
            return 1
    
    print()
    
    # Step 2: Run DORA analysis
    print("📊 Running DORA analysis...")
    success = run_dora_analysis(args.project_name, args.project_key)
    
    if success:
        print("\n🎉 DORA analysis completed successfully!")
        print(f"📁 Results saved to: dora_metrics_{args.project_key.lower()}_results.json")
        print(f"📁 Data saved to: {data_file}")
        return 0
    else:
        print("\n❌ DORA analysis failed.")
        return 1

if __name__ == "__main__":
    exit(main())
