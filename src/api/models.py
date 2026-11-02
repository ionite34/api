from __future__ import annotations

from fastapi_camelcase import CamelModel


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
    def from_dict(cls, data: dict) -> RollDetResponse:
        """Construct a RollDetResponse from a dict"""
        return cls(
            url=str(data.get("url")),
            redirect_url=(
                str(data.get("redirect_url")) if data.get("redirect_url") else None
            ),
            is_roll=data.get("is_roll"),
            error=data.get("error") if data.get("error") else None,
            song=data.get("song") if data.get("song") else None,
            artist=data.get("artist") if data.get("artist") else None,
        )
