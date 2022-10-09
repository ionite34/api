from __future__ import annotations

from fastapi_camelcase import CamelModel
from rolldet.result import DetectResult


class MessageResponse(CamelModel):
    """
    Response Model for simple messages.
    """

    message: str


class VersionResponse(CamelModel):
    """
    Response Model for version information.
    """

    message: str
    version: str


class RollDetResponse(CamelModel):
    """
    Response Model for rolldet results.
    """

    url: str
    redirect_url: str | None = None
    is_roll: bool = False
    error: str | None = None
    song: str | None = None
    artist: str | None = None

    @classmethod
    def from_result(cls, data: DetectResult) -> RollDetResponse:
        """Construct a RollDetResponse from a DetectResult"""
        return cls(
            url=str(data.url),
            redirect_url=str(data.redirect_url) if data.redirect_url else None,
            is_roll=data.is_roll,
            error=data.error,
            song=data.song,
            artist=data.artist,
        )
