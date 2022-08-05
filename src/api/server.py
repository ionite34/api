from __future__ import annotations

import logging
from functools import cached_property
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import AnyUrl
from rolldet import Detector

from api import __version__
from api.models import MessageResponse, RollDetResponse, VersionResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi() -> dict[str, Any]:
    """Custom OpenAPI generator"""
    if app.openapi_schema:  # caching
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Ionite API",
        version=__version__,
        description="https://github.com/ionite34/api",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore


class RunnerStore:
    """Stores persistent runners."""

    @cached_property
    def rolldet(self) -> Detector:
        """Lazy loaded rolldet.Detector"""
        return Detector()


runner_store = RunnerStore()


@app.get("/")
async def root() -> VersionResponse:
    return VersionResponse(
        message="You've reached the root of the Ionite API",
        version=__version__,
    )


@app.get("/hello/{name}", response_model=MessageResponse)
async def hello(name: str) -> MessageResponse:
    logger.info(f"GET /hello/{name}")
    return MessageResponse(message=f"Hello {name}")


@app.get("/rolldet/{url:path}", response_model=RollDetResponse)
async def rolldet(url: AnyUrl, request: Request) -> RollDetResponse:
    logger.info(f"GET /rolldet/{url}")
    full_url = str(url)
    # If parameter present
    if q := request.query_params:
        full_url = f"{full_url}?{q}"

    # noinspection HttpUrlsUsage
    if not full_url.startswith(("https://", "http://")):
        full_url = f"https://{full_url}"

    logger.info(f"Parsed /rolldet/ url: {full_url}")
    detector = runner_store.rolldet
    result = await detector.find(full_url)
    return RollDetResponse.from_dict(result.as_dict())
