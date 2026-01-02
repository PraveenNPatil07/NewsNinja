from typing import List
import os
# UPDATED: Use ChatOpenAI for OpenRouter compatibility
from langchain_openai import ChatOpenAI 
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from tenacity import (
    retry, 
    stop_after_attempt,
    wait_exponential, 
    retry_if_exception_type
)
import asyncio
from datetime import datetime, timedelta

load_dotenv()

two_weeks_ago = datetime.today() - timedelta(days=14)
two_weeks_ago_str = two_weeks_ago.strftime('%Y-%m-%d')

class MCPOverloadedError(Exception):
    pass

mcp_limiter = AsyncLimiter(1, 15)

# UPDATED: Switched to a model that supports Tool Calling
# "google/gemini-2.0-flash-exp:free" is a good free option with tool support.
# Alternatives if this fails: "meta-llama/llama-3.1-70b-instruct:free" or "mistralai/mistral-7b-instruct:free"
model = ChatOpenAI(
    model="google/gemini-2.0-flash-exp:free", 
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)

# UPDATED: Fixed typo in package name (@brighdata -> @brightdata)
server_params = StdioServerParameters(
    command="npx",
    env={
        "API_TOKEN": os.getenv("BRIGHTDATA_API_TOKEN"),
        "WEB_UNLOCKER_ZONE": os.getenv("WEB_UNLOCKER_ZONE"),
    },
    args=["@brightdata/mcp"], 
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=15, max=60),
    retry=retry_if_exception_type(MCPOverloadedError),
    reraise=True
)
async def process_topic(agent, topic: str):
    async with mcp_limiter:
        message = [
            {
                "role": "system",
                "content": f"""You are a Reddit analysis expert. Use available tools to:
                1. Find top 2 posts about the given topic BUT only after {two_weeks_ago_str}, NOTHING before this date strictly!
                2. Analyze their content and sentiment
                3. Create a summary of discussions and overall sentiment"""
            },
            {
                "role": "user",
                "content": f"""Analyze Reddit posts about '{topic}'. 
                Provide a comprehensive summary including:
                - Main discussion points
                - Key opinions expressed
                - Any notable trends or patterns
                - Summarize the overall narrative, discussion points and also quote interesting comments without mentioning names
                - Overall sentiment (positive/neutral/negative)"""
            }
        ]

        try:
            # LangGraph agent invocation
            response = await agent.ainvoke({"messages": message})
            return response["messages"][-1].content
        except Exception as e:
            if "Overload" in str(e):
                raise MCPOverloadedError("Service overload")
            else:
                raise

async def scrape_reddit_topics(topics: List[str]) -> dict[str, dict]:
    """Process list of topics and return analysis results"""
    # Initialize the MCP client (BrightData)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Load tools from MCP and create the Agent
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)

            reddit_results = {}

            for topic in topics:
                print(f"Analyzing Reddit topic: {topic}...")
                try:
                    summary = await process_topic(agent, topic)
                    reddit_results[topic] = summary
                except Exception as e:
                    print(f"Failed to process topic {topic}: {e}")
                    reddit_results[topic] = "Error retrieving Reddit data."
                    
                await asyncio.sleep(5) # Rate limiting pause

            return {"reddit_analysis": reddit_results}