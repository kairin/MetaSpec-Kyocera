
from markitdown._markitdown import DocumentConverterResult

from src.logger import logger
from src.registry import TOOL
from src.tools.tools import AsyncTool
from src.utils import fetch_url

_WEB_FETCHER_DESCRIPTION = """Visit a webpage at a given URL and return its text. """

@TOOL.register_module(name="web_fetcher_tool", force=True)
class WebFetcherTool(AsyncTool):
    name = "web_fetcher_tool"
    description = _WEB_FETCHER_DESCRIPTION
    parameters = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The relative or absolute url of the webpage to visit."
            }
        },
        "required": ["url"],
        "additionalProperties": False
    }
    output_type = "any"

    def __init__(self):
        super(WebFetcherTool, self).__init__()

    async def forward(self, url: str) -> DocumentConverterResult | None:
        """Fetch content from a given URL."""

        # try to use asyncio to fetch the URL content
        try:
            res = await fetch_url(url)
            if not res:
                logger.error(f"Failed to fetch content from {url}")
                res = DocumentConverterResult(
                    markdown=f"Failed to fetch content from {url}",
                    title="Error",
                )
        except Exception as e:
            logger.error(f"Error fetching content: {e}")
            res = DocumentConverterResult(
                markdown=f"Failed to fetch content: {e}",
                title="Error",
            )
        return res

