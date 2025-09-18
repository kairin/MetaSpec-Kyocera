"""
Configuration for CLI-based models.

This configuration replaces API-based models with CLI tool adapters.
"""

# Agent configuration using CLI models
agent_config = dict(
    description='A planning agent that can plan the steps using CLI tools.',
    managed_agents=[
        'deep_analyzer_agent',
        'browser_use_agent',
        'deep_researcher_agent',
    ],
    max_steps=20,
    model_id='claude-code',  # Use Claude Code CLI
    name='planning_agent',
    provide_run_summary=True,
    template_path='src/agent/planning_agent/prompts/planning_agent.yaml',
    tools=[
        'planning_tool',
    ],
    type='planning_agent'
)

# Deep analyzer using Claude Code for file operations and analysis
deep_analyzer_agent_config = dict(
    description='A deep analyzer agent using Claude Code for systematic analysis.',
    max_steps=3,
    model_id='claude-code',
    name='deep_analyzer_agent',
    provide_run_summary=True,
    template_path='src/agent/deep_analyzer_agent/prompts/deep_analyzer_agent.yaml',
    tools=[
        'deep_analyzer_tool',
        'python_interpreter_tool',
    ],
    type='deep_analyzer_agent'
)

# Browser use agent using Gemini for web-based reasoning
browser_use_agent_config = dict(
    description='A browser use agent using Gemini for web searches and interaction.',
    max_steps=5,
    model_id='gemini-pro',
    name='browser_use_agent',
    provide_run_summary=True,
    template_path='src/agent/browser_use_agent/prompts/browser_use_agent.yaml',
    tools=[
        'auto_browser_use_tool',
        'python_interpreter_tool',
    ],
    type='browser_use_agent'
)

# Deep researcher using intelligent CLI bridge
deep_researcher_agent_config = dict(
    description='A deep researcher agent using CLI bridge for extensive searches.',
    max_steps=3,
    model_id='cli-bridge',  # Use the intelligent CLI bridge
    name='deep_researcher_agent',
    provide_run_summary=True,
    template_path='src/agent/deep_researcher_agent/prompts/deep_researcher_agent.yaml',
    tools=[
        'deep_researcher_tool',
        'python_interpreter_tool',
    ],
    type='deep_researcher_agent'
)

# Planning agent configuration
planning_agent_config = agent_config

# Tool configurations (unchanged)
deep_analyzer_tool_config = dict(
    analyzer_model_ids=['gemini-pro'],
    summarizer_model_id='gemini-pro',
    type='deep_analyzer_tool'
)

deep_researcher_tool_config = dict(
    max_depth=2,
    max_follow_ups=3,
    max_insights=20,
    model_id='cli-bridge',
    time_limit_seconds=60,
    type='deep_researcher_tool'
)

auto_browser_use_tool_config = dict(
    model_id='gemini-pro',
    type='auto_browser_use_tool'
)

# Other configurations
concurrency = 1
use_hierarchical_agent = True
use_local_proxy = False
workdir = 'workdir'
tag = 'cli'
exp_path = '/home/kkk/Apps/DeepResearchAgent/workdir/cli'
log_path = '/home/kkk/Apps/DeepResearchAgent/workdir/cli/log.txt'
save_path = '/home/kkk/Apps/DeepResearchAgent/workdir/cli/dra.jsonl'

# CLI-specific configurations
cli_config = dict(
    # Claude Code CLI configuration
    claude_code_command='claude-code',  # CLI command
    claude_code_timeout=300,  # 5 minutes

    # Gemini CLI configuration
    gemini_command='gemini',  # CLI command
    gemini_model='gemini-pro',
    gemini_timeout=180,  # 3 minutes

    # Bridge configuration
    enable_intelligent_routing=True,
    conversation_memory_limit=10,  # Keep last 10 exchanges

    # CLI session management
    use_persistent_sessions=False,  # Set to True for better performance
    session_timeout=1800,  # 30 minutes

    # Error handling
    max_retries=3,
    fallback_to_local_model=False,  # Could fallback to local models if CLI fails
)

# File and tool configurations (unchanged from main config)
file_reader_tool_config = dict(type='file_reader_tool')
web_fetcher_tool_config = dict(type='web_fetcher_tool')
web_searcher_tool_config = dict(
    country='us',
    engine='Firecrawl',
    fetch_content=True,
    lang='en',
    max_length=4096,
    max_retries=3,
    num_results=5,
    retry_delay=10,
    type='web_searcher_tool'
)

# MCP tools configuration (can work with CLI models too)
mcp_tools_config = dict(
    mcpServers=dict(
        LocalMCP=dict(
            args=['/home/kkk/Apps/DeepResearchAgent/src/mcp/server.py'],
            command='python',
            env=dict(DEBUG='true')
        )
    )
)