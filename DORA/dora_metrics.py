#!/usr/bin/env python3
"""
DORA Metrics Analyzer
==================================================

This script provides a complete DORA metrics analysis for any JIRA project
using real data fetched via MCP tools. It calculates:
1. Lead Time for Changes
2. Deployment Frequency  
3. Mean Time to Recovery (MTTR)
4. Change Failure Rate

Usage:
    python3 dora_metrics_integrated.py --project-name "Project Name" --project-key "PROJ"

Requirements:
    - pip install python-dateutil
    - MCP tools for Atlassian integration
"""

import json
import argparse
from datetime import datetime, timedelta
from dateutil import parser
import statistics
from typing import List, Dict, Any

class DORAMetrics:
    def __init__(self, project_name: str, project_key: str):
        self.project_name = project_name
        self.project_key = project_key
        self.issues_data = []
        
    def set_issues_data(self, issues: List[Dict[str, Any]]):
        """Set the issues data for analysis"""
        self.issues_data = issues
        
    def get_issues_data(self) -> List[Dict[str, Any]]:
        """Get the issues data for analysis"""
        return self.issues_data


    
    def calculate_lead_time(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate Lead Time for Changes"""
        lead_times = []
        
        for issue in issues:
            # Handle both data structures: direct fields or nested in "fields"
            created = issue.get("created") or issue.get("fields", {}).get("created")
            resolved = issue.get("resolutiondate") or issue.get("fields", {}).get("resolutiondate")
            
            if created and resolved:
                try:
                    created_date = parser.parse(created)
                    resolved_date = parser.parse(resolved)
                    lead_time_days = (resolved_date - created_date).total_seconds() / (24 * 3600)
                    lead_times.append(lead_time_days)
                except Exception as e:
                    continue
        
        if not lead_times:
            return {"average": 0, "median": 0, "min": 0, "max": 0, "count": 0}
        
        return {
            "average": round(statistics.mean(lead_times), 1),
            "median": round(statistics.median(lead_times), 1),
            "min": round(min(lead_times), 1),
            "max": round(max(lead_times), 1),
            "count": len(lead_times)
        }
    
    def calculate_deployment_frequency(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate Deployment Frequency based on resolution patterns"""
        resolution_dates = []
        
        for issue in issues:
            # Handle both data structures: direct fields or nested in "fields"
            resolved = issue.get("resolutiondate") or issue.get("fields", {}).get("resolutiondate")
            if resolved:
                try:
                    resolved_date = parser.parse(resolved)
                    resolution_dates.append(resolved_date.date())
                except Exception:
                    continue
        
        if not resolution_dates:
            return {"frequency": "No data", "deployments_per_week": 0}
        
        # Count unique deployment days
        unique_days = len(set(resolution_dates))
        days_analyzed = 90  # Last 90 days
        deployments_per_week = round((unique_days / days_analyzed) * 7, 1)
        
        return {
            "frequency": f"{unique_days} deployment days in 90 days",
            "deployments_per_week": deployments_per_week,
            "total_deployments": unique_days
        }
    
    def calculate_mttr(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate Mean Time to Recovery for bugs"""
        bug_issues = [issue for issue in issues 
                     if (issue.get("issuetype", {}).get("name") == "Bug" or 
                         issue.get("fields", {}).get("issuetype", {}).get("name") == "Bug")]
        
        recovery_times = []
        
        for issue in bug_issues:
            # Handle both data structures: direct fields or nested in "fields"
            created = issue.get("created") or issue.get("fields", {}).get("created")
            resolved = issue.get("resolutiondate") or issue.get("fields", {}).get("resolutiondate")
            
            if created and resolved:
                try:
                    created_date = parser.parse(created)
                    resolved_date = parser.parse(resolved)
                    recovery_time_hours = (resolved_date - created_date).total_seconds() / 3600
                    recovery_times.append(recovery_time_hours)
                except Exception:
                    continue
        
        if not recovery_times:
            return {"average_hours": 0, "average_days": 0, "count": 0}
        
        avg_hours = statistics.mean(recovery_times)
        avg_days = avg_hours / 24
        
        return {
            "average_hours": round(avg_hours, 1),
            "average_days": round(avg_days, 1),
            "count": len(recovery_times)
        }
    
    def calculate_change_failure_rate(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate Change Failure Rate"""
        total_issues = len(issues)
        bug_issues = [issue for issue in issues 
                     if (issue.get("issuetype", {}).get("name") == "Bug" or 
                         issue.get("fields", {}).get("issuetype", {}).get("name") == "Bug")]
        
        bug_count = len(bug_issues)
        failure_rate = (bug_count / total_issues * 100) if total_issues > 0 else 0
        
        # Categorize by priority
        critical_bugs = [issue for issue in bug_issues 
                        if ((issue.get("priority", {}).get("name") in ["Highest", "High"]) or
                            (issue.get("fields", {}).get("priority", {}).get("name") in ["Highest", "High"]))]
        
        return {
            "total_issues": total_issues,
            "bug_issues": bug_count,
            "critical_bugs": len(critical_bugs),
            "failure_rate_percent": round(failure_rate, 1),
            "critical_failure_rate_percent": round((len(critical_bugs) / total_issues * 100), 1) if total_issues > 0 else 0
        }
    
    def get_performance_level(self, metric: str, value: float) -> str:
        """Determine performance level based on DORA benchmarks"""
        benchmarks = {
            "lead_time_days": {"elite": 1, "high": 7, "medium": 30},
            "deployments_per_week": {"elite": 7, "high": 1, "medium": 0.2},
            "mttr_hours": {"elite": 1, "high": 24, "medium": 168},
            "failure_rate": {"elite": 5, "high": 15, "medium": 30}
        }
        
        if metric not in benchmarks:
            return "Unknown"
        
        if value <= benchmarks[metric]["elite"]:
            return "Elite"
        elif value <= benchmarks[metric]["high"]:
            return "High"
        elif value <= benchmarks[metric]["medium"]:
            return "Medium"
        else:
            return "Low"
    
    def analyze_dora_metrics(self) -> Dict[str, Any]:
        """Main method to analyze all DORA metrics"""
        
        # Get issues data
        issues = self.get_issues_data()
        if not issues:
            print("❌ No issues data available for analysis")
            return {}
            
        print(f"🔍 Analyzing DORA metrics for {len(issues)} issues")
        
        # Calculate metrics
        lead_time = self.calculate_lead_time(issues)
        deployment_freq = self.calculate_deployment_frequency(issues)
        mttr = self.calculate_mttr(issues)
        failure_rate = self.calculate_change_failure_rate(issues)
        
        # Determine performance levels
        lead_time_level = self.get_performance_level("lead_time_days", lead_time["average"])
        deployment_level = self.get_performance_level("deployments_per_week", deployment_freq["deployments_per_week"])
        mttr_level = self.get_performance_level("mttr_hours", mttr["average_hours"])
        failure_level = self.get_performance_level("failure_rate", failure_rate["failure_rate_percent"])
        
        return {
            "lead_time": {**lead_time, "performance_level": lead_time_level},
            "deployment_frequency": {**deployment_freq, "performance_level": deployment_level},
            "mttr": {**mttr, "performance_level": mttr_level},
            "change_failure_rate": {**failure_rate, "performance_level": failure_level},
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_issues_analyzed": len(issues),
            "data_source": "Real JIRA Data (MCP)"
        }
    
    def print_report(self, metrics: Dict[str, Any]):
        """Print a formatted DORA metrics report in table format"""
        if not metrics:
            return
        
        print("\n" + "="*80)
        print(f"📊 DORA METRICS REPORT - {self.project_name.upper()} PROJECT")
        print("="*80)
        print(f"📅 Analysis Date: {metrics['analysis_date']}")
        print(f"📈 Issues Analyzed: {metrics['total_issues_analyzed']}")
        print(f"🔧 Data Source: {metrics.get('data_source', 'Unknown')}")
        print("="*80)
        
        # Extract metrics
        lt = metrics["lead_time"]
        df = metrics["deployment_frequency"]
        mttr = metrics["mttr"]
        cfr = metrics["change_failure_rate"]
        
        # Format current levels for display
        lead_time_display = f"~{int(lt['average'])} days"
        deployment_freq_display = f"{df['deployments_per_week']:.1f}/week"
        mttr_display = f"{mttr['average_days']:.1f} days"
        failure_rate_display = f"{cfr['failure_rate_percent']:.1f}%"
        
        # Get status icons and text
        def get_status_icon(level):
            if level == "Elite":
                return "🤩"
            elif level == "High":
                return "✅"
            elif level == "Medium":
                return "⚠️"
            else:  # Low
                return "🚨"
        
        def get_status_text(level):
            if level == "Elite":
                return "Excellent"
            elif level == "High":
                return "Good"
            elif level == "Medium":
                return "Needs Improvement"
            else:  # Low
                return "Needs Improvement"
        
        # Print table header
        print(f"\n{'Overall DORA Performance Summary':<50} 📈")
        print("="*80)
        print(f"{'Metric':<20} {'Current Level':<20} {'Industry Benchmark':<25} {'Status':<15}")
        print("="*80)
        print(f"{'📊 Tickets Analyzed':<20} {metrics['total_issues_analyzed']:<20} {'':<25} {'':<15}")
        print("-"*80)
        
        # Lead Time row
        print(f"{'Lead Time':<20} {lead_time_display:<20} {'< 1 week (Elite)':<25} {get_status_icon(lt['performance_level'])} {get_status_text(lt['performance_level'])}")
        
        # Deployment Frequency row
        print(f"{'Deployment Freq':<20} {deployment_freq_display:<20} {'Daily (Elite)':<25} {get_status_icon(df['performance_level'])} {get_status_text(df['performance_level'])}")
        
        # MTTR row
        print(f"{'MTTR':<20} {mttr_display:<20} {'< 1 hour (Elite)':<25} {get_status_icon(mttr['performance_level'])} {get_status_text(mttr['performance_level'])}")
        
        # Change Failure Rate row
        print(f"{'Change Failure Rate':<20} {failure_rate_display:<20} {'< 15% (Elite)':<25} {get_status_icon(cfr['performance_level'])} {get_status_text(cfr['performance_level'])}")
        
        print("="*80)
        
        # Detailed breakdown
        print(f"\n📋 DETAILED BREAKDOWN")
        print(f"   Lead Time:        {lt['average']} days avg, {lt['median']} days median")
        print(f"   Deployment Freq:  {df['frequency']}")
        print(f"   MTTR:            {mttr['average_hours']} hours ({mttr['average_days']} days)")
        print(f"   Failure Rate:    {cfr['bug_issues']}/{cfr['total_issues']} issues ({cfr['failure_rate_percent']}%)")
        print(f"   Critical Bugs:   {cfr['critical_bugs']} ({cfr['critical_failure_rate_percent']}%)")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        if lt['performance_level'] in ['Low', 'Medium']:
            print("   • Reduce lead time by implementing smaller, more frequent releases")
        if df['performance_level'] in ['Low', 'Medium']:
            print("   • Increase deployment frequency to daily or multiple times per day")
        if mttr['performance_level'] in ['Low', 'Medium']:
            print("   • Improve incident response and monitoring capabilities")
        if cfr['performance_level'] in ['Low', 'Medium']:
            print("   • Enhance testing coverage and implement better quality gates")
        
        print("\n" + "="*80)


def main():
    """Main function to run the DORA metrics analysis"""
    parser = argparse.ArgumentParser(description="DORA Metrics Analyzer for JIRA Projects")
    parser.add_argument("--project-name", required=True,
                       help="Project name (required)")
    parser.add_argument("--project-key", required=True,
                       help="Project key (any valid JIRA project key)")
    
    args = parser.parse_args()
    
    print(f"🚀 DORA Metrics Analyzer - {args.project_name} Project")
    print("=" * 60)
    print(f"🏷️  Project: {args.project_name} ({args.project_key})")
    
    try:
        analyzer = DORAMetrics(args.project_name, args.project_key)
        
        # Load data from file
        data_file = f"tmp/dora_metrics_{args.project_key.lower()}_data.json"
        print(f"🔄 Loading data from: {data_file}")
        
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            issues = data.get('issues', [])
            print(f"✅ Loaded {len(issues)} issues from {data_file}")
            print(f"📅 Data fetched at: {data.get('fetched_at', 'Unknown')}")
            print(f"📊 Data source: {data.get('data_source', 'Unknown')}")
            
        except FileNotFoundError:
            print(f"❌ Data file not found: {data_file}")
            print("💡 Please ensure the data file exists or run the script with MCP tools available")
            return
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing data file: {e}")
            return
        
        if not issues:
            print(f"❌ No issues found in data file for project {args.project_key}")
            return
        
        # Set the data for analysis
        analyzer.set_issues_data(issues)
        
        metrics = analyzer.analyze_dora_metrics()
        if metrics:
            analyzer.print_report(metrics)
            
            # Save results to file
            filename = f"tmp/dora_metrics_{args.project_key.lower()}_results.json"
            with open(filename, "w") as f:
                json.dump(metrics, f, indent=2)
            print(f"\n💾 Results saved to: {filename}")
        else:
            print("❌ No metrics calculated - no data available")
        
    except Exception as e:
        print(f"❌ Error running analysis: {e}")

if __name__ == "__main__":
    main()
