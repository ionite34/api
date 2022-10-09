from __future__ import annotations

import logging
from functools import cached_property

from fastapi import APIRouter, Request
from pydantic import AnyUrl
from rolldet.detector import Detector
from rolldet.result import DetectResult

from api.database import db
from api.models import RollDetResponse

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

router = APIRouter(
    prefix="/rolldet",
    tags=["Utilities"],
    responses={404: {"description": "Not found"}},
)


class DetectorWorker:
    """Rolldet Worker."""

    @cached_property
    def detector(self) -> Detector:
        """Lazy loaded rolldet.Detector"""
        return Detector()

    def cache_lookup(self, url: str) -> DetectResult | None:
        """Check cache for result."""
        key = db.key("rolldet", url)
        result = db.get(key)
        if not result:
            return None
        return DetectResult

    async def find(self, url: str) -> DetectResult:
        """Find roll."""
        # First check if in db
        result = await self.detector.find(url)
        return result


detector = DetectorWorker()


@router.get("{url:path}", response_model=RollDetResponse)
async def rolldet(url: AnyUrl, request: Request) -> RollDetResponse:
    """Rolldet API."""
    log.info(f"GET /rolldet/{url}")
    full_url = str(url)

    if q := request.query_params:
        full_url = f"{full_url}?{q}"

    result = await detector.find(full_url)
    return RollDetResponse.from_result(result)
