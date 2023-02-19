# routers/schema.py

import json

from routers import BASE_PATH
from typing import Any
from fastapi import APIRouter, HTTPException
from schema import SCIM_API_MESSAGES, ListResponse, Schemas

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=BASE_PATH+"/Schemas",
    tags=["SCIM Schemas"],
)


@router.get("")
async def get_schemas() -> ListResponse:
    """ Return Schemas """

    resources = []

    for schema in Schemas.keys():
        resources.append(
            json.loads(Schemas[schema].schema_json(by_alias=True))
        )

    return ListResponse(
        Resources=resources,
        itemsPerPage=len(resources),
        schemas=[
            SCIM_API_MESSAGES+":ListResponse"
        ],
        startIndex=1,
        totalResults=len(resources)
    )


@router.get("/{id}")
async def get_schema(id: str) -> Any:
    """ Return Schemas """

    resource = Schemas.get(id)
    logger.debug(resource)
    if not resource:
        raise HTTPException(status_code=404, detail=f"Schema {id} not found")

    return json.loads(resource.schema_json(by_alias=True))
