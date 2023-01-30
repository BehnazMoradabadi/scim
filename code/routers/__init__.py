# routers/__init__.py

from fastapi import HTTPException

from schema import ListResponse
from filter import Filter

from data.users import get_user_resources
from data.groups import get_group_resources

reader = {
    'User': get_user_resources,
    'Group': get_group_resources,
}


def get_all_resources(
    resource_type, startindex, count, query
) -> ListResponse:
    """ Read all resource of resource type"""

    try:
        resource_reader = reader.get(resource_type)
        if not resource_reader:
            raise Exception(f"No reader for: {resource_type}")

        startindex = max(1, startindex)
        count = max(0, count)

        totalresults = (
            resource_reader(
                Filter(query)
            ) or []
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    resources = totalresults[startindex-1:][:count]

    return ListResponse(
        Resources=resources,
        itemsPerPage=len(resources),
        schemas=[
            "urn:ietf:params:scim:api:messages:2.0:ListResponse"
        ],
        startIndex=startindex,
        totalResults=len(totalresults)
    )
