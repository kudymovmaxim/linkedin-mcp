# linkedin-mcp

## What is this?

**Nano LinkedIn MCP server for LLM agents & Cursor**
A developer tool to automate LinkedIn workflows using agents. You can scrape profiles, companies, inbox, threads, and send messages via LinkedIn, all through a local MCP server. Built for pipeline automation and easy integration with other tools.

---

## Features

- Scrape LinkedIn profiles (name, experience, etc.)
- Scrape company pages (industry, size, etc.)
- Scrape inbox threads and messages
- Send messages to users or threads
- Easily extendable for new LinkedIn actions

---

## Quickstart

### 1. Install dependencies

You'll need Python 3.8+.

This project uses the [Phantombuster](https://phantombuster.com) service for LinkedIn automation. You need an account and API key from Phantombuster to use all features.

```bash
pip install python-dotenv requests pydantic
```

### 2. Set up environment variables

Create a `.env` file in the root:

```
PHANTOMBUSTER_API_KEY=your_phantombuster_key
LINKEDIN_COOKIE_LI=your_linkedin_cookie
LINKEDIN_BROWSER_AGENT=your_browser_user_agent
```

How to get these values:
- **LINKEDIN_BROWSER_AGENT**: This is your browser user agent. Open Google and search for "my browser user agent", then copy the value.
- **LINKEDIN_COOKIE_LI**: This is your LinkedIn cookie. In Chrome: open LinkedIn, right-click and choose "Inspect", go to the "Application" tab, select "Cookies" > "https://linkedin.com", find "li_at" and copy its value.

### 3. Run the server

```bash
python mcp_server/linkedin-server.py
```

### 4. Example: Call from an agent

You can connect the MCP server to your Agent

```python
async with MCPServerStdio(
    params={
        "command": "python",
        "args": [
            "{pathtoproject}/linkedin-mcp/mcp_server/linkedin-server.py"
        ],
        "env": {
            "PYTHONPATH": "{pathtoproject}/linkedin-mcp",
            "PHANTOMBUSTER_API_KEY": phantombuster_api_key or "",
            "LINKEDIN_COOKIE_LI": linkedin_cookie_li or "",
            "LINKEDIN_BROWSER_AGENT": linkedin_browser_agent or ""
        },
        "description": "LinkedIn MCP server: scrap profile,. "
    }
) as server:
    await server.connect()

    tools = await server.list_tools()

    agent=Agent(
        name="Assistant",
        instructions="Use the tools to achieve the task",
        mcp_servers=[server]
    )
```

### 5. Add to Cursor

- Open Cursor
- Go to MCP settings
- Add a new server with:
```json
"linkedin-server": {
    "command": "python",
    "args": [
        "{pathtoproject}/linkedin-server.py"
    ],
    "env": {
        "PYTHONPATH": "{pathtoproject}",
        "PHANTOMBUSTER_API_KEY": "",
        "LINKEDIN_COOKIE_LI": "",
        "LINKEDIN_BROWSER_AGENT": ""
    },
    "description": "LinkedIn MCP server: scrap profile,. "
}
```

---

## Roadmap

- Scrape user posts
- Collect more detailed company info
- Support other providers (e.g., browser automation, not just Phantombuster)
- Integrate with LinkedIn Sales Navigator
- Add memory (agent context, history)
- Add cache for requests/results
- Add limits (rate limiting, quotas)

> ⚠️ **Important:** LinkedIn does not like automation. Always respect daily limits to avoid account restrictions:
>
> **Free LinkedIn:**
> - 100 messages per day
> - 100 profiles per day
> - 20 connection requests per day
>
> **Premium LinkedIn:**
> - 150 messages per day
> - 200 profiles per day
> - 40 connection requests per day

---

## About the Author

Maksim K. — Building Radr: Cursor for Pipeline. Ex-Product Lead (YC, TeachStars). CEO at Radr. Contact: max@radr.xyz