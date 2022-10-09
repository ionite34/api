from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from api import __version__


def custom_openapi(app: FastAPI) -> dict[str, Any]:
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
