import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.llm import function_tool, ChatChunk
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import deepgram, openai, silero
from livekit.agents import JobContext, WorkerOptions, cli, Agent, AgentSession
from livekit.plugins import deepgram, openai, silero

from mcp_client import MCPServerSse
from mcp_client.agent_tools import MCPToolsIntegration

load_dotenv()

class FunctionAgent(Agent):
    """A LiveKit agent that uses MCP tools from one or more MCP servers."""

    def __init__(self):
        super().__init__(
            instructions="""
                You are a helpful assistant communicating through voice.
                Use the available MCP tools to answer questions.
            """,
            stt=deepgram.STT(),
            llm=openai.LLM(model="gpt-4o"),
            tts=openai.TTS(),
            vad=silero.VAD.load(),
            allow_interruptions=True
        )

    async def llm_node(self, chat_ctx, tools, model_settings):
        """Override the llm_node to say a message when a tool call is detected."""
        activity = self._activity
        tool_call_detected = False

        # Get the original response from the parent class
        async for chunk in super().llm_node(chat_ctx, tools, model_settings):
            # Check if this chunk contains a tool call
            if isinstance(chunk, ChatChunk) and chunk.delta and chunk.delta.tool_calls and not tool_call_detected:
                # Say the checking message only once when we detect the first tool call
                tool_call_detected = True
                activity.agent.say("Sure, I'll check that for you.")

            yield chunk

async def entrypoint(ctx: JobContext):
    """Main entrypoint for the LiveKit agent application."""
    mcp_server = MCPServerSse(
        params={"url": os.environ.get("ZAPIER_MCP_URL")},
        cache_tools_list=True,
        name="SSE MCP Server"
    )

    agent = await MCPToolsIntegration.create_agent_with_tools(
        agent_class=FunctionAgent,
        mcp_servers=[mcp_server]
    )

    await ctx.connect()

    session = AgentSession()
    await session.start(agent=agent, room=ctx.room)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
