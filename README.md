# JIRA-tooling

Simple JIRA ticket management with MCP integration for Cursor IDE.

## Setup

1. **Set environment variables:**
   ```bash
   export JIRA_BASE_URL="https://fielmann.atlassian.net"
   export JIRA_EMAIL="your-email@example.com"
   export JIRA_API_TOKEN="your_jira_api_token_here"
   ```

2. **Test:**
   ```bash
   ./get-ticket.sh TEV-6778
   ```

## Usage

Get ticket details:
```bash
./get-ticket.sh <TICKET-KEY>
```

## MCP Integration with Cursor

1. **Update your Cursor MCP configuration** (`~/.cursor/mcp.json`):
   ```json
   {
     "mcpServers": {
       "jira": {
         "command": "npx",
         "args": [
           "-y",
           "@quialorraine/jira-mcp-server",
           "--jira-base-url=https://fielmann.atlassian.net",
           "--jira-email=your-email@example.com",
           "--jira-api-token=$JIRA_API_TOKEN",
           "--stdio"
         ]
       }
     }
   }
   ```

2. **Restart Cursor** and ask it to manage JIRA issues directly.
