#!/bin/bash

# Usage: ./get-ticket.sh TEV-6778
# Requires JIRA_API_TOKEN environment variable to be set

if [ $# -ne 1 ]; then
    echo "Usage: $0 <issue-key>"
    echo "Example: $0 TEV-6778"
    echo ""
    echo "Make sure JIRA_API_TOKEN environment variable is set:"
    echo "export JIRA_API_TOKEN=\"your_api_token_here\""
    exit 1
fi

ISSUE_KEY=$1
API_TOKEN=${JIRA_API_TOKEN}

if [ -z "$API_TOKEN" ]; then
    echo "Error: JIRA_API_TOKEN environment variable is not set"
    echo "Please set it with: export JIRA_API_TOKEN=\"your_api_token_here\""
    exit 1
fi

BASE_URL="https://fielmann.atlassian.net"
EMAIL="julika.boedewadt@fielmann.com"

echo "Fetching ticket: $ISSUE_KEY"
echo "---"

# Get the raw JSON response
RESPONSE=$(curl -s -u "$EMAIL:$API_TOKEN" \
  -H "Accept: application/json" \
  "$BASE_URL/rest/api/3/issue/$ISSUE_KEY?fields=description,summary,status,assignee,reporter,created,updated")

# Check if we got an error
if echo "$RESPONSE" | grep -q '"errorMessages"'; then
    echo "Error: $(echo "$RESPONSE" | grep -o '"errorMessages":\["[^"]*"' | cut -d'"' -f4)"
    exit 1
fi

# Extract fields using basic text processing
echo "Ticket: $(echo "$RESPONSE" | grep -o '"key":"[^"]*"' | cut -d'"' -f4)"
echo "Summary: $(echo "$RESPONSE" | grep -o '"summary":"[^"]*"' | cut -d'"' -f4)"
echo "Status: $(echo "$RESPONSE" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)"
echo "Assignee: $(echo "$RESPONSE" | grep -o '"displayName":"[^"]*"' | head -1 | cut -d'"' -f4 || echo "Unassigned")"
echo "Reporter: $(echo "$RESPONSE" | grep -o '"displayName":"[^"]*"' | tail -1 | cut -d'"' -f4)"
echo "Created: $(echo "$RESPONSE" | grep -o '"created":"[^"]*"' | cut -d'"' -f4)"
echo "Updated: $(echo "$RESPONSE" | grep -o '"updated":"[^"]*"' | cut -d'"' -f4)"
echo ""
echo "Description:"
echo "$RESPONSE" | grep -o '"description":"[^"]*"' | cut -d'"' -f4 | sed 's/\\n/\n/g' | sed 's/\\"/"/g'
