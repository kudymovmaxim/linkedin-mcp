import os
import asyncio
import argparse
from dotenv import load_dotenv
from agents.mcp import MCPServerStdio

load_dotenv()

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-key', type=str, help='Phantombuster API key')
    parser.add_argument('--cookie', type=str, help='LinkedIn cookie')
    parser.add_argument('--browser', type=str, help='LinkedIn browser agent')
    args = parser.parse_args()

    phantombuster_api_key = os.environ.get('PHANTOMBUSTER_API_KEY') or args.api_key
    linkedin_cookie_li = os.environ.get('LINKEDIN_COOKIE_LI') or args.cookie
    linkedin_browser_agent = os.environ.get('LINKEDIN_BROWSER_AGENT') or args.browser

    print("Запуск MCP агента...")
    async with MCPServerStdio(
        # params={
        #     "command": "python",
        #     # "args": [os.path.join(os.getcwd(), "mcp_server", "linkedin-server.py")],
        #     "args": ["-m", "mcp_server.linkedin-server"],
        #     "env": {
        #         "PHANTOMBUSTER_API_KEY": phantombuster_api_key or "",
        #         "LINKEDIN_COOKIE_LI": linkedin_cookie_li or "",
        #         "LINKEDIN_BROWSER_AGENT": linkedin_browser_agent or ""
        #     }
        # }

        params={
            "command": "python",
            "args": [
                "/Users/kudymov/work/linkedin-mcp/mcp_server/linkedin-server.py"
            ],
            "env": {
                "PYTHONPATH": "/Users/kudymov/work/linkedin-mcp",
                "PHANTOMBUSTER_API_KEY": phantombuster_api_key or "",
                "LINKEDIN_COOKIE_LI": linkedin_cookie_li or "",
                "LINKEDIN_BROWSER_AGENT": linkedin_browser_agent or ""
            },
            "description": "LinkedIn MCP server: scrap profile,. "
        }
    ) as server:
        await server.connect()

        tools = await server.list_tools()
        print("\nList of tools MCP:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

        # result = await server.call_tool("scrap_profile", {"linkedin": "https://www.linkedin.com/in/maxim-kudymov/"})
        # print(f"ping -> {result}")

        result = await server.call_tool(tool_name="scrap_inbox", arguments={
            "count_to_scrape": 10,
            "inbox_filter": "unread"
        })
        print(f"[scrap_inbox]: {result}")

if __name__ == "__main__":
    asyncio.run(main()) 