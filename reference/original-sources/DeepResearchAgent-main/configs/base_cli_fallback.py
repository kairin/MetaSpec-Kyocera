"""
Base configuration for CLI-first setup with local fallbacks
"""

web_fetcher_tool_config = dict(
    type="web_fetcher_tool",
)

web_searcher_tool_config = dict(
    type="web_searcher_tool",
    engine="Firecrawl",  # Options: "Firecrawl", "Google", "Bing", "DuckDuckGo", "Baidu"
    retry_delay=10,
    max_retries=3,
    lang="en",
    country="us",
    num_results=5,
    fetch_content=True,
    max_length=4096,
)

# Deep researcher tool - use local model instead of GPT-4.1
deep_researcher_tool_config = dict(
    type="deep_researcher_tool",
    model_id="qwen2.5-32b-instruct",  # Local fallback instead of GPT-4.1
    max_depth=2,
    max_insights=20,
    time_limit_seconds=60,
    max_follow_ups=3,
)

# Auto browser use tool - use local model
auto_browser_use_tool_config = dict(
    type="auto_browser_use_tool",
    model_id="qwen2.5-32b-instruct"  # Local fallback instead of GPT-4.1
)

# Deep analyzer tool - use local model or CLI equivalent
deep_analyzer_tool_config = dict(
    type="deep_analyzer_tool",
    analyzer_model_ids=["qwen2.5-32b-instruct"],  # Local fallback instead of Gemini
    summarizer_model_id="qwen2.5-32b-instruct",   # Local fallback instead of Gemini
)

mcp_tools_config = {
    "mcpServers": {
        # Local stdio server
        "LocalMCP": {
            "command": "python",
            "args": ["src/mcp/server.py"],
            "env": {"DEBUG": "true"}
        },
    }
}

# Use local models for image/video generation fallbacks
image_generator_tool_config = dict(
    type="image_generator_tool",
    analyzer_model_id="qwen2.5-32b-instruct",  # Local fallback
    generator_model_id="local-image-gen",      # Placeholder
)

video_generator_tool_config = dict(
    type="video_generator_tool",
    analyzer_model_id="qwen2.5-32b-instruct",   # Local fallback
    predict_model_id="local-video-predict",     # Placeholder
    fetch_model_id="local-video-fetch",         # Placeholder
)

file_reader_tool_config = dict(
    type="file_reader_tool"
)

oai_deep_research_tool_config = dict(
    type="oai_deep_research_tool",
    model_id="qwen2.5-32b-instruct",  # Local fallback instead of o3-deep-research
)