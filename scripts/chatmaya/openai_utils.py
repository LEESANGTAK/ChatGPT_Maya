# -*- coding: utf-8 -*-
from typing import List
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

import openai
import tiktoken

DEFAULT_CHAT_MODEL = "gpt-3.5-turbo"
DEFAULT_ENCODING = "cl100k_base"

MAX_ATTEMPT = 3 # Number of retries
MIN_SECONDS = 5 # Minimum retry seconds
MAX_SECONDS = 15 # Maximum retry seconds


def retry_decorator(func):
    return retry(
        #reraise=True,
        stop=stop_after_attempt(MAX_ATTEMPT),
        wait=wait_exponential(multiplier=1, min=MIN_SECONDS, max=MAX_SECONDS),
        retry=(
            retry_if_exception_type(openai.APIError)
            | retry_if_exception_type(openai.OpenAIError)
            | retry_if_exception_type(openai.ConflictError)
            | retry_if_exception_type(openai.NotFoundError)
            | retry_if_exception_type(openai.APIStatusError)
            | retry_if_exception_type(openai.RateLimitError)
            | retry_if_exception_type(openai.APITimeoutError)
            | retry_if_exception_type(openai.BadRequestError)
            | retry_if_exception_type(openai.APIConnectionError)
            | retry_if_exception_type(openai.AuthenticationError)
            | retry_if_exception_type(openai.InternalServerError)
            | retry_if_exception_type(openai.PermissionDeniedError)
            | retry_if_exception_type(openai.UnprocessableEntityError)
            | retry_if_exception_type(openai.APIResponseValidationError)
        )
    )(func)

def num_tokens_from_text(text:str, encoding_name:str=DEFAULT_ENCODING) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens

@retry_decorator
def chat_completion_stream(messages:List, model:str=DEFAULT_CHAT_MODEL, **kwargs) -> str:

        result = openai.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            **kwargs
        )

        for chunk in result:
            if chunk:
                content = chunk.choices[0].delta.content
                if content:
                    yield content