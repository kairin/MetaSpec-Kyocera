import argparse
import json
from copy import deepcopy
from typing import Any

from mmengine import DictAction
from PIL import Image

from src.config import config
from src.logger import logger
from src.models import ChatMessage, MessageManager, model_manager
from src.utils import assemble_project_path


def parse_args():
    parser = argparse.ArgumentParser(description='main')
    parser.add_argument(
        "--config",
        default=assemble_project_path("configs/config_general.py"),
        help="config file path"
    )

    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.')
    args = parser.parse_args()
    return args


def log_message_list(prefix: str, message_list: list[dict[str, Any]]):
    message_list = deepcopy(message_list)
    for message in message_list:
        content = message.get("content")
        if isinstance(content, list):
            for item in content:
                if item.get("type") == "image_url":
                    base64_image = item["image_url"]["url"]
                    item["image_url"]["url"] = base64_image[:30] + "..."
                elif item.get("type") == "image":
                    base64_image = item["image"]
                    item["image"] = base64_image[:30] + "..."
    logger.info(f"| {prefix}: {json.dumps(message_list, indent=4)}")


if __name__ == "__main__":

    # Parse command line arguments
    args = parse_args()

    # Initialize the configuration
    config.init_config(args.config, args)

    # Initialize the logger
    logger.init_logger(log_path=config.log_path)
    logger.info(f"| Logger initialized at: {config.log_path}")
    logger.info(f"| Config:\n{config.pretty_text}")

    # Registered models
    model_manager.init_models(use_local_proxy=False)
    image = Image.open(assemble_project_path("docs/assets/architecture.png"))
    registered_models = ", ".join(model_manager.registered_models.keys())
    logger.info("Registered models: %s", registered_models)

    # Test message manager
    message_manager = MessageManager(
        model_id="gpt-4.1", api_type="chat/completions"
    )

    # Test Single Text Message
    text_messages = [
        ChatMessage(role="user", content="What is the capital of France?"),
    ]
    message_list = message_manager.get_clean_message_list(text_messages)
    log_message_list("Single Text Message", message_list)

    # Test Multiple Text Messages
    text_messages = [
        ChatMessage(role="user", content=[
            {
                "type": "text",
                "text": "What is the capital of France?"
            },
            {
                "type": "text",
                "text": "What is the capital of Germany?"
            }
        ])
    ]
    message_list = message_manager.get_clean_message_list(text_messages)
    log_message_list("Multiple Text Messages", message_list)

    # Test Single Text Message with Image
    text_messages = [
        ChatMessage(role="user", content=[
            {
                "type": "text",
                "text": "What is the capital of France?"
            },
            {
                "type": "image",
                "image": image
            }
        ])
    ]
    message_list = message_manager.get_clean_message_list(
        text_messages, convert_images_to_image_urls=True
    )
    log_message_list("Single Text Message with Image", message_list)
    message_list = message_manager.get_clean_message_list(
        text_messages, convert_images_to_image_urls=False
    )
    log_message_list("Single Text Message with Image (No Convert)", message_list)

    # Test Single Text Message with Response API
    text_messages = [
        ChatMessage(role="user", content="What is the capital of France?")
    ]
    message_list = message_manager.get_clean_message_list(
        text_messages, api_type="responses"
    )
    log_message_list("Single Text Message with Response API", message_list)

    # Test Multiple Text Messages with Response API
    text_messages = [
        ChatMessage(role="user", content=[
            {
                "type": "text",
                "text": "What is the capital of France?"
            },
            {
                "type": "text",
                "text": "What is the capital of Germany?"
            }
        ])
    ]
    message_list = message_manager.get_clean_message_list(
        text_messages, api_type="responses"
    )
    log_message_list("Multiple Text Messages with Response API", message_list)
