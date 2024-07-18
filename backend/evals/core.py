import os
from config import ANTHROPIC_API_KEY

from llm import Llm, stream_claude_response, stream_openai_response, stream_azure_openai_response
from prompts import assemble_prompt
from prompts.types import Stack


async def generate_code_core(image_url: str, stack: Stack, model: Llm) -> str:
    prompt_messages = assemble_prompt(image_url, stack)
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    anthropic_api_key = ANTHROPIC_API_KEY
    openai_base_url = None
    azure_openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    azure_openai_resource_name = os.environ.get("AZURE_OPENAI_RESOURCE_NAME")
    azure_openai_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION")

    async def process_chunk(content: str):
        pass

    if model == Llm.CLAUDE_3_SONNET or model == Llm.CLAUDE_3_5_SONNET_2024_06_20:
        if not anthropic_api_key:
            raise Exception("Anthropic API key not found")

        completion = await stream_claude_response(
            prompt_messages,
            api_key=anthropic_api_key,
            callback=lambda x: process_chunk(x),
            model=model,
        )
    else:
        if not openai_api_key and not azure_openai_api_key:
            raise Exception("OpenAI API or Azure key not found")

        completion = await stream_openai_response(
            prompt_messages,
            api_key=openai_api_key,
            base_url=openai_base_url,
            callback=lambda x: process_chunk(x),
            model=model,
        )

    return completion
