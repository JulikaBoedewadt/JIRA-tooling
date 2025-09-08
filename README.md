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
   ./get-my-recent-issues.sh
   ```

## Usage

Get your recent issues (last 7 days):
```bash
./get-my-recent-issues.sh
```

## MCP Integration with Cursor

Use Atlassian's official remote MCP server for secure and feature-rich integration:

1. **Configure Cursor MCP settings** (`~/.cursor/mcp.json`):
   ```json
   {
     "mcpServers": {
       "Atlassian-MCP-Server": {
         "url": "https://mcp.atlassian.com/v1/sse"
       }
     }
   }
   ```

2. **Restart Cursor** and authenticate with your Atlassian account when prompted.

## Official Documentation

- **[Atlassian Remote MCP Server](https://www.atlassian.com/platform/remote-mcp-server)** - Official Atlassian MCP server with OAuth authentication and enterprise security
- **[Setting up IDEs with MCP](https://support.atlassian.com/rovo/docs/setting-up-ides/)** - Detailed setup instructions for Cursor, VS Code, and other IDEs

## Features

- **Secure Authentication**: OAuth-based authentication with granular permissions
- **Enterprise Security**: Protected data with trusted AI partner integrations
- **Cross-Platform**: Works with Cursor, VS Code, Claude, and other MCP-compatible tools
- **Real-time Access**: Direct integration with Jira and Confluence data
