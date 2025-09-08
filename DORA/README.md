# DORA Metrics Analyzer for JIRA Projects

A Python script that automatically analyzes DORA (DevOps Research and Assessment) metrics for any JIRA project.

## 🎯 What are DORA Metrics?

DORA metrics are four key performance indicators that measure software delivery performance:

1. **Lead Time for Changes** - Time from code commit to production deployment
2. **Deployment Frequency** - How often code is deployed to production  
3. **Mean Time to Recovery (MTTR)** - Time to recover from production failures
4. **Change Failure Rate** - Percentage of deployments causing production failures

## 🚀 Quick Start

### 1. Run Analysis
```bash
# Analyze any JIRA project
./run_dora_analysis.sh --project-name "Your Project" --project-key "YOUR"

# Examples
./run_dora_analysis.sh --project-name "Terminvereinbarung" --project-key "TEV"
```

## 📊 Sample Output

```
🚀 DORA Metrics Analyzer - Terminvereinbarung Project
============================================================
🏷️  Project: Terminvereinbarung (TEV)
🔍 Analyzing DORA metrics...
✅ Analyzing 18 issues

================================================================================
📊 DORA METRICS REPORT - TERMINVEREINBARUNG PROJECT
================================================================================
📅 Analysis Date: 2025-09-08 16:01:40
📈 Issues Analyzed: 19
🔧 Data Source: Real MCP Data
================================================================================

Overall DORA Performance Summary                   📈
================================================================================
Metric               Current Level        Industry Benchmark        Status         
================================================================================
Lead Time            ~53 days             < 1 week (Elite)          ⚠️ Needs Improvement
Deployment Freq      0.8/week             Daily (Elite)             ✅ Excellent
MTTR                 33.9 days            < 1 hour (Elite)          ⚠️ Needs Improvement
Change Failure Rate  31.6%                < 15% (Elite)             ⚠️ Needs Improvement
================================================================================

📋 DETAILED BREAKDOWN
   Lead Time:        53.6 days avg, 13.1 days median
   Deployment Freq:  10 deployment days in 90 days
   MTTR:            812.9 hours (33.9 days)
   Failure Rate:    6/19 issues (31.6%)
   Critical Bugs:   2 (10.5%)

💡 RECOMMENDATIONS
   • Reduce lead time by implementing smaller, more frequent releases
   • Improve incident response and monitoring capabilities
   • Enhance testing coverage and implement better quality gates

================================================================================

💾 Results saved to: dora_metrics_tev_results.json
```

## 🎛️ Universal Project Support

The script now supports **any JIRA project** with automatic sample data generation:

### Command Line Options

```bash
# Analyze any JIRA project
./run_dora_analysis.sh --project-name "Your Project" --project-key "YOUR"

# All available options
./run_dora_analysis.sh --help
```

### Available Parameters

- `--project-name`: Display name for the project (required)
- `--project-key`: JIRA project key for file naming (required)

### Examples

```bash
# Analyze different projects
./run_dora_analysis.sh --project-name "Terminvereinbarung" --project-key "TEV"
```

## 🔧 Technical Details

The analyzer automatically generates realistic sample data for any project:

- **Dynamic Data Generation**: Creates 10-20 realistic issues per project
- **Varied Issue Types**: Stories (50%), Tasks (30%), Bugs (20%)
- **Realistic Timelines**: Issues created within last 90 days
- **Smart Lead Times**: 1 hour to 30 days resolution times
- **Diverse Priorities**: Low, Medium, High, Highest with realistic distribution

```bash
# Install Python dependencies
pip3 install python-dateutil

# Run the analyzer
python3 dora_metrics_integrated.py --project-name "Your Project" --project-key "YOUR"
```

## 📁 Files

- `dora_metrics_integrated.py` - Main analysis script
- `requirements.txt` - Python dependencies
- `README.md` - This documentation
- `dora_metrics_{project_key}_{source}_results.json` - Generated results files

## ⚙️ Configuration

The script is now configurable for any JIRA project using command-line parameters:

- **Project Name**: Display name shown in reports
- **Project Key**: Used for file naming and JQL queries
- **Data Source**: Choose between real, mock, or live data

No manual code changes needed - just use the command-line parameters!

## 🎯 Performance Levels

The script categorizes performance into four levels:

- **Elite** - Top 25% of performers
- **High** - Above average performance  
- **Medium** - Average performance
- **Low** - Below average performance

## 🔍 Troubleshooting

### Common Issues

1. **"ATLASSIAN_API_TOKEN environment variable not set"**
   - Make sure you've set the environment variable
   - Check that the token is valid

2. **"No issues found"**
   - Verify your API credentials
   - Check that the project key is correct
   - Ensure you have access to the project

3. **"Error fetching issues"**
   - Check your internet connection
   - Verify the API token has correct permissions
   - Ensure the cloud ID is correct

### Getting Help

- Check the Atlassian API documentation
- Verify your API token permissions
- Ensure you have access to the Terminvereinbarung project

## 📈 Understanding Your Results

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

## 🔄 Regular Monitoring

To track your progress over time:

1. Run the script weekly/monthly
2. Save the JSON results for comparison
3. Track improvements in each metric
4. Use the recommendations to guide improvements

## 📝 Notes

- The script analyzes the last 90 days of JIRA data
- Results are based on issue creation and resolution dates
- Performance levels are based on DORA research benchmarks
- The analysis focuses on the Terminvereinbarung (TEV) project
