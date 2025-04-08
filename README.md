# LiveKit Agent with MCP Tools

A voice assistant application built using the LiveKit Agents framework, capable of using Multimodal Control Protocol (MCP) tools to interact with external services.

## Features

- Voice-based interaction with a helpful AI assistant
- Integration with MCP tools from external servers
- Speech-to-text using Deepgram
- Natural language processing using OpenAI's GPT-4o
- Text-to-speech using OpenAI
- Voice activity detection using Silero

## Prerequisites

- Python 3.9+
- API keys for OpenAI and Deepgram
- MCP server endpoint

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/livekit-examples/basic-mcp.git
   cd basic-mcp
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys and configuration:
   ```
   OPENAI_API_KEY=your_openai_api_key
   DEEPGRAM_API_KEY=your_deepgram_api_key
   ZAPIER_MCP_URL=your_mcp_server_url
   ```

## Usage

Run the agent with the LiveKit CLI:

```
python agent.py console
```

The agent will connect to the specified LiveKit room and start listening for voice commands.

## Project Structure

- `agent.py`: Main agent implementation and entrypoint
- `mcp_client/`: Package for MCP server integration
  - `server.py`: MCP server connection handlers
  - `agent_tools.py`: Integration of MCP tools with LiveKit agents
  - `util.py`: Utility functions for MCP client

## Acknowledgements

- [LiveKit](https://livekit.io/) for the underlying real-time communication infrastructure
- [OpenAI](https://openai.com/) for GPT-4o and text-to-speech
- [Deepgram](https://deepgram.com/) for speech-to-text
- [Silero](https://github.com/snakers4/silero-vad) for Voice Activity Detection