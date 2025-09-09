# 🚀 DORA Metrics Analyzer for JIRA Projects

A unified Python script that automatically analyzes DORA (DevOps Research and Assessment) metrics for any JIRA project using real data.

## 🎯 What are DORA Metrics?

DORA metrics are four key performance indicators that measure software delivery performance:

1. **Lead Time for Changes** - Time from code commit to production deployment
2. **Deployment Frequency** - How often code is deployed to production  
3. **Mean Time to Recovery (MTTR)** - Time to recover from production failures
4. **Change Failure Rate** - Percentage of deployments causing production failures

## 🚀 Quick Start (5 minutes)

### Run Analysis (in Cursor IDE)
```bash
./analyze.sh --project-name "Your Project" --project-key "YOUR_PROJECT"
```

## 📊 Sample Output

```
🚀 DORA Metrics Analyzer
========================
🔧 Activating virtual environment...
🚀 Starting DORA analysis...
🚀 Unified DORA Metrics Analyzer
==================================================
🏷️  Project: Terminvereinbarung (TEV)

🔄 Fetching fresh data...
🔍 Fetching data for project: TEV
🔍 Getting accessible Atlassian resources...
🔍 Searching JIRA issues...
✅ Fetched 29 issues from JIRA
💾 Data saved to: tmp/dora_metrics_tev_data.json

📊 Running DORA analysis...
📊 Running DORA analysis for: Terminvereinbarung
✅ Analysis completed successfully!

================================================================================
📋 DORA METRICS RESULTS:
================================================================================
🚀 DORA Metrics Analyzer - Terminvereinbarung Project
============================================================
🏷️  Project: Terminvereinbarung (TEV)
🔄 Loading data from: tmp/dora_metrics_tev_data.json
✅ Loaded 29 issues from tmp/dora_metrics_tev_data.json
📅 Data fetched at: 2025-01-27T12:30:00.000Z
📊 Data source: Real JIRA Data (MCP) - Last 30 days (Done status)
🔍 Analyzing DORA metrics for 29 issues

================================================================================
📊 DORA METRICS REPORT - TERMINVEREINBARUNG PROJECT
================================================================================
📅 Analysis Date: 2025-09-09 17:17:00
📈 Issues Analyzed: 29
🔧 Data Source: Real JIRA Data (MCP)
================================================================================

Overall DORA Performance Summary                   📈
================================================================================
Metric               Current Level        Industry Benchmark        Status         
================================================================================
📊 Tickets Analyzed   29                                                            
--------------------------------------------------------------------------------
Lead Time            ~36 days             < 1 week (Elite)          🚨 Needs Improvement
Deployment Freq      0.9/week             Daily (Elite)             🤩 Excellent
MTTR                 49.3 days            < 1 hour (Elite)          🚨 Needs Improvement
Change Failure Rate  13.8%                < 15% (Elite)             ✅ Good
================================================================================

📋 DETAILED BREAKDOWN
   Lead Time:        36.5 days avg, 13.7 days median
   Deployment Freq:  12 deployment days in 90 days
   MTTR:            1182.1 hours (49.3 days)
   Failure Rate:    4/29 issues (13.8%)
   Critical Bugs:   1 (3.4%)

💡 RECOMMENDATIONS
   • Reduce lead time by implementing smaller, more frequent releases
   • Improve incident response and monitoring capabilities

================================================================================

💾 Results saved to: tmp/dora_metrics_tev_results.json

🎉 DORA analysis completed successfully!
📁 Results saved to: dora_metrics_tev_results.json
📁 Data saved to: tmp/dora_metrics_tev_data.json
```

## 🎛️ Command Options

### Basic Usage
```bash
# Analyze any JIRA project
./analyze.sh --project-name "Your Project" --project-key "YOUR_PROJECT"


```

### Direct Python Execution
```bash
# Run the unified analyzer directly
python3 analyze_dora.py --project-name "Your Project" --project-key "YOUR_PROJECT"
```

## 🔧 How It Works

### 1. Automatic Setup
- Creates virtual environment if needed
- Installs required dependencies (`python-dateutil`)
- Activates environment
- All happens automatically when you run `./analyze.sh`

### 2. Fresh Data Fetching
- **Always fetches fresh data** via MCP tools (last 30 days, Done status only)
- **Saves data** to `tmp/` folder for reference
- **No caching** - ensures you always get the most recent metrics

### 3. Complete Analysis
- Runs DORA metrics calculation
- Displays comprehensive report
- Saves results to JSON file in `tmp/` folder

## 📁 File Structure

```
DORA/
├── analyze.sh                    # Main entry point (shell wrapper)
├── analyze_dora.py              # Unified analyzer with MCP integration
├── dora_metrics.py              # Core metrics calculation
├── tmp/                         # Generated data files (git-ignored)
│   ├── dora_metrics_{project}_data.json      # Project data
│   └── dora_metrics_{project}_results.json  # Analysis results
├── dora_env/                    # Virtual environment (git-ignored)
└── README.md                    # This documentation
```

## 🎯 Performance Levels

The script categorizes performance into four levels based on DORA research:

### Lead Time for Changes
- **Elite**: < 1 day
- **High**: 1-7 days  
- **Medium**: 1-30 days
- **Low**: > 30 days

### Deployment Frequency
- **Elite**: Multiple times per day
- **High**: Daily
- **Medium**: Weekly
- **Low**: Monthly or less

### Mean Time to Recovery
- **Elite**: < 1 hour
- **High**: 1-24 hours
- **Medium**: 1-7 days
- **Low**: > 7 days

### Change Failure Rate
- **Elite**: 0-5%
- **High**: 5-15%
- **Medium**: 15-30%
- **Low**: > 30%

## 🔍 Troubleshooting

### Common Issues

1. **"MCP tools not available"**
   - **Solution**: Run in Cursor IDE, not terminal
   - **Why**: MCP tools only work in Cursor IDE context

2. **"No issues found"**
   - **Solution**: Check your project key is correct
   - **Verify**: You have access to the JIRA project
   - **Check**: The project has issues closed in the last 30 days

3. **"Data file not found"**
   - **Solution**: Run with `--force-refresh` to fetch data
   - **Check**: The data file exists in `tmp/` folder

4. **"No data available for analysis"**
   - **Solution**: Ensure you have access to the project
   - **Check**: The data file contains issues

### Getting Help

- Check the MCP configuration in Cursor
- Verify your Atlassian account permissions
- Ensure you have access to the target JIRA project

## 📋 Prerequisites

1. **Cursor IDE** with MCP tools enabled
2. **Atlassian access** to your JIRA instance
3. **Python 3.7+** with `python-dateutil` package

## 🔄 Regular Monitoring

To track your progress over time:

1. Run the script weekly/monthly
2. Save the JSON results for comparison
3. Track improvements in each metric
4. Use the recommendations to guide improvements

## 💡 Tips for Better Results

1. **Fetch Recent Data**: Uses issues closed in the last 30 days for relevant metrics
2. **Include All Issue Types**: Stories, Tasks, and Bugs all contribute to DORA metrics
3. **Check Data Quality**: Review the fetched data to ensure it looks correct
4. **Run Regularly**: Track your DORA metrics over time to see improvements

## 🎉 Success!

Once you've successfully run the analysis, you'll have valuable insights into your team's DevOps performance and can use the recommendations to improve your development process!

---

**Note**: This analyzer uses real JIRA data fetched via MCP tools and focuses on issues that were closed with "Done" status in the last 30 days for the most relevant and recent performance metrics.