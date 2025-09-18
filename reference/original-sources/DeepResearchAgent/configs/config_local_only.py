"""
Configuration for local-only setup with minimal dependencies.
This config uses only models that don't require external API keys.
"""

# Experiment settings - organized directory structure
tag = 'local_only'
workdir = 'outputs'  # Cleaner name than 'workdir'
log_path = 'local_only.log'  # System will place in exp_path automatically
save_path = 'local_only_results.jsonl'  # System will place in exp_path automatically

# Use hierarchical agent structure
use_hierarchical_agent = True
use_local_proxy = False  # Using direct model access
concurrency = 1

# Model configurations using Hugging Face models (no API keys needed)
planning_agent_config = dict(
    type='planning_agent',
    name='planning_agent',
    description='A planning agent that can plan the steps to complete the task.',
    model_id='qwen2.5-7b-instruct',  # Local HuggingFace model
    max_steps=20,
    template_path='src/agent/planning_agent/prompts/planning_agent.yaml',
    tools=['planning_tool'],
    managed_agents=[
        'deep_analyzer_agent',
        'browser_use_agent',
        'deep_researcher_agent',
    ],
    provide_run_summary=True,
)

# Set the main agent configuration
agent_config = planning_agent_config

# Deep analyzer with local models
deep_analyzer_agent_config = dict(
    type='deep_analyzer_agent',
    name='deep_analyzer_agent',
    description='A deep analyzer agent that can perform systematic, step-by-step analysis.',
    model_id='qwen2.5-7b-instruct',  # Local model
    max_steps=3,
    template_path='src/agent/deep_analyzer_agent/prompts/deep_analyzer_agent.yaml',
    tools=['deep_analyzer_tool', 'python_interpreter_tool'],
    provide_run_summary=True,
)

deep_analyzer_tool_config = dict(
    type='deep_analyzer_tool',
    analyzer_model_ids=['qwen2.5-7b-instruct'],  # Local models
    summarizer_model_id='qwen2.5-7b-instruct',   # Local model
)

# Browser use agent with local models
browser_use_agent_config = dict(
    type='browser_use_agent',
    name='browser_use_agent',
    description='A browser use agent that can search relevant web pages and interact with them.',
    model_id='qwen2.5-7b-instruct',  # Local model
    max_steps=5,
    template_path='src/agent/browser_use_agent/prompts/browser_use_agent.yaml',
    tools=['auto_browser_use_tool', 'python_interpreter_tool'],
    provide_run_summary=True,
)

auto_browser_use_tool_config = dict(
    type='auto_browser_use_tool',
    model_id='qwen2.5-7b-instruct',  # Local model
)

# Deep researcher with local models
deep_researcher_agent_config = dict(
    type='deep_researcher_agent',
    name='deep_researcher_agent',
    description='A deep researcher agent that can conduct extensive web searches.',
    model_id='qwen2.5-7b-instruct',  # Local model
    max_steps=3,
    template_path='src/agent/deep_researcher_agent/prompts/deep_researcher_agent.yaml',
    tools=['deep_researcher_tool', 'python_interpreter_tool'],
    provide_run_summary=True,
)

deep_researcher_tool_config = dict(
    type='deep_researcher_tool',
    model_id='qwen2.5-7b-instruct',  # Local model
    max_depth=2,
    max_follow_ups=3,
    max_insights=20,
    time_limit_seconds=60,
)

# Web tools configuration
web_searcher_tool_config = dict(
    type='web_searcher_tool',
    engine='Firecrawl',  # Note: Requires FIRECRAWL_API_KEY or will fall back
    country='us',
    lang='en',
    num_results=5,
    max_retries=3,
    retry_delay=10,
    fetch_content=True,
    max_length=4096,
)

web_fetcher_tool_config = dict(
    type='web_fetcher_tool',
)

file_reader_tool_config = dict(
    type='file_reader_tool',
)

# MCP tools configuration (optional)
mcp_tools_config = dict(
    mcpServers=dict(
        LocalMCP=dict(
            command='python',
            args=['/home/kkk/Apps/DeepResearchAgent/src/mcp/server.py'],
            env=dict(DEBUG='true')
        )
    )
)