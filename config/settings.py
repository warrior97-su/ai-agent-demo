import os
import sys

import httpx
from dotenv import load_dotenv
from openai import APIConnectionError, AuthenticationError, OpenAI, PermissionDeniedError, RateLimitError

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_FALLBACK_API_KEY = os.environ.get("OPENAI_FALLBACK_API_KEY", OPENAI_API_KEY)
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_FALLBACK_BASE_URL = os.environ.get(
    "OPENAI_FALLBACK_BASE_URL", "https://work.freemodel.dev/v1"
)
OPENAI_FALLBACK_ENABLED = os.environ.get("OPENAI_FALLBACK_ENABLED", "true").lower() == "true"
MODEL = os.environ["MODEL"]

_RETRYABLE_ERRORS = (
    PermissionDeniedError,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
)

WORKBUDDY_HEADERS = {
    "x-requested-with": "XMLHttpRequest",
    "x-stainless-arch": "x64",
    "x-stainless-lang": "python",
    "x-stainless-os": "Windows",
    "x-stainless-package-version": "2.50.0",
    "x-stainless-runtime": "python",
    "x-stainless-runtime-version": sys.version.split()[0],
    "x-agent-intent": "craft",
    "x-ide-type": "WorkBuddy",
    "x-ide-name": "WorkBuddy",
    "x-ide-version": "5.3.5",
    "x-domain": "www.codebuddy.cn",
    "x-product": "SaaS",
    "user-agent": "WorkBuddy/5.3.5 WorkBuddy/5.3.5 CLI/2.115.0",
}

# 主线路：标准 OpenAI 兼容接口
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

# 备用线路：WorkBuddy / work.freemodel.dev（HTTP/2 + 同款请求头）
_fallback_http = httpx.Client(http2=True, verify=False)
fallback_client = (
    OpenAI(
        api_key=OPENAI_FALLBACK_API_KEY,
        base_url=OPENAI_FALLBACK_BASE_URL,
        default_headers=WORKBUDDY_HEADERS,
        http_client=_fallback_http,
    )
    if OPENAI_FALLBACK_ENABLED
    else None
)

_active_client = None


def chat_create(**kwargs):
    """调用 chat.completions.create，主线路失败时自动切换备用线路。"""
    global _active_client

    if _active_client is not None:
        clients = [_active_client]
    else:
        clients = [client]
        if fallback_client is not None:
            clients.append(fallback_client)

    last_error = None
    for index, current_client in enumerate(clients):
        label = "主线路" if current_client is client else "备用线路(WorkBuddy)"
        try:
            if index > 0:
                print(f"[API] 切换至{label}...")
            response = current_client.chat.completions.create(**kwargs)
            _active_client = current_client
            return response
        except _RETRYABLE_ERRORS as exc:
            print(f"[API] {label}失败: {exc}")
            last_error = exc
            continue

    if last_error is not None:
        raise last_error
    raise RuntimeError("没有可用的 API 客户端")
