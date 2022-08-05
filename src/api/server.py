from __future__ import annotations

import logging
from functools import cached_property

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
async def rolldet(url: AnyUrl) -> RollDetResponse:
    logger.info(f"GET /rolldet/{url}")
    full_url = str(url)

    # noinspection HttpUrlsUsage
    if not full_url.startswith(("https://", "http://")):
        full_url = f"https://{full_url}"

    logger.info(f"Parsed /rolldet/ url: {full_url}")
    detector = runner_store.rolldet
    result = await detector.find(full_url)
    return RollDetResponse.from_dict(result.as_dict())
