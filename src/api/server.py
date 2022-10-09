from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AnyUrl

from api import __version__
from api.docs import custom_openapi
from api.endpoints import rolldet
from api.models import MessageResponse, RollDetResponse, VersionResponse

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Create FastAPI app
app = FastAPI(debug=True)
# Add custom OpenAPI for swagger docs
app.openapi = custom_openapi(app)  # type: ignore
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(rolldet.router)


@app.on_event("startup")
async def startup() -> None:
    ...
    # await database.connect()


@app.get("/")
async def root() -> VersionResponse:
    """Root endpoint."""
    return VersionResponse(
        message="You've reached the root of the Ionite API",
        version=__version__,
    )


@app.get("/hello/{name}", response_model=MessageResponse)
async def hello(name: str) -> MessageResponse:
    """Hello endpoint."""
    log.info(f"GET /hello/{name}")
    return MessageResponse(message=f"Hello {name}")
