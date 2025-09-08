#!/bin/bash

# Usage: ./get-my-recent-issues.sh
# Fetches all issues assigned to you in the last 7 days
# Requires JIRA_API_TOKEN environment variable to be set

API_TOKEN=${JIRA_API_TOKEN}

if [ -z "$API_TOKEN" ]; then
    echo "Error: JIRA_API_TOKEN environment variable is not set"
    echo "Please set it with: export JIRA_API_TOKEN=\"your_api_token_here\""
    exit 1
fi

BASE_URL="https://fielmann.atlassian.net"
EMAIL="julika.boedewadt@fielmann.com"

echo "Fetching issues assigned to you in the last 7 days..."
echo "---"

# Calculate date 7 days ago in ISO format
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    SEVEN_DAYS_AGO=$(date -u -v-7d +"%Y-%m-%d")
else
    # Linux
    SEVEN_DAYS_AGO=$(date -u -d "7 days ago" +"%Y-%m-%d")
fi

echo "Searching for issues updated since: $SEVEN_DAYS_AGO"
echo ""

# JQL query to get issues assigned to current user updated in last 7 days
JQL="assignee = currentUser() AND updated >= \"$SEVEN_DAYS_AGO\" ORDER BY updated DESC"

# URL encode the JQL query
ENCODED_JQL=$(printf '%s\n' "$JQL" | jq -sRr @uri)

# Get the issues using JIRA REST API
RESPONSE=$(curl -s -u "$EMAIL:$API_TOKEN" \
  -H "Accept: application/json" \
  "$BASE_URL/rest/api/3/search?jql=$ENCODED_JQL&fields=key,summary,status,assignee,updated,created,priority,issuetype&maxResults=50")

# Check if we got an error
if echo "$RESPONSE" | grep -q '"errorMessages"'; then
    echo "Error: $(echo "$RESPONSE" | grep -o '"errorMessages":\["[^"]*"' | cut -d'"' -f4)"
    exit 1
fi

# Extract the total count
TOTAL=$(echo "$RESPONSE" | grep -o '"total":[0-9]*' | cut -d':' -f2)

if [ "$TOTAL" = "0" ]; then
    echo "No issues found assigned to you in the last 7 days."
    exit 0
fi

echo "Found $TOTAL issue(s) assigned to you in the last 7 days:"
echo ""

# Parse and display each issue
echo "$RESPONSE" | jq -r '.issues[] | 
  "\(.key): \(.fields.summary)
  Status: \(.fields.status.name)
  Type: \(.fields.issuetype.name)
  Priority: \(.fields.priority.name // "None")
  Updated: \(.fields.updated | split("T")[0])
  Created: \(.fields.created | split("T")[0])
  ---"'

echo ""
echo "Total: $TOTAL issue(s)"
