import logging
import urllib.parse

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rolldet import Detector

from api import __version__
from api.models import MessageResponse, RollDetResponse

logger = logging.getLogger(__name__)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "You've reached the root of the Ionite API",
        "version": __version__,
    }


@app.get("/hello/{name}", response_model=MessageResponse)
async def hello(name: str):
    logger.info(f"GET /hello/{name}")
    return MessageResponse(message=f"Hello {name}")


@app.get("/rolldet/{url:path}", response_model=RollDetResponse)
async def rolldet(url: str, request: Request):
    logger.info(f"GET /rolldet/{url}")
    x_url = request.path_params.get("url")
    x_query = request.query_params
    full_url = f"{x_url}?{x_query}"
    logger.warning(f"url: {full_url}")
    # Add https if not present
    if not full_url.startswith("https://") and not full_url.startswith("http://"):
        full_url = f"https://{full_url}"
    logging.info(f"Parsed URL: {full_url}")
    detector = Detector()
    result = await detector.find(full_url)
    return RollDetResponse.from_dict(result.as_dict())
