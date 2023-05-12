from typing import TypeVar

from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from pydantic.schema import schema

from response.generic import R

Model = TypeVar("Model", bound=BaseModel)


def custom_openapi(app):
    def wrap():
        if not app.openapi_schema:
            app.openapi_schema = get_openapi(
                    title=app.title,
                    version=app.version,
                    openapi_version=app.openapi_version,
                    description=app.description,
                    terms_of_service=app.terms_of_service,
                    contact=app.contact,
                    license_info=app.license_info,
                    routes=app.routes,
                    tags=app.openapi_tags,
                    servers=app.servers,
                    )
            for _, method_item in app.openapi_schema.get("paths").items():
                for _, param in method_item.items():
                    responses = param.get("responses")
                    # remove 422 response, also can remove other status code
                    if "422" in responses:
                        del responses["422"]
                    responses["400"] = {
                            "description": "Request Error",
                            "content"    : {"application/json": {"schema": {"$ref": f"{REF_PREFIX}ErrorResponse"}}},
                            }
            error_response_schema = schema((R,), ref_prefix=REF_PREFIX, ref_template=f"{REF_PREFIX}{{model}}")
            error_response_schema = {"ErrorResponse": list(error_response_schema["definitions"].values())[0]}

            properties = error_response_schema["ErrorResponse"]["properties"]
            properties["code"]["default"] = 400
            properties["msg"]["default"] = "request failed"

            openapi_schemas = app.openapi_schema["components"]["schemas"]
            openapi_schemas.update(error_response_schema)
            openapi_schemas.pop("ValidationError")
            openapi_schemas.pop("HTTPValidationError")
        return app.openapi_schema

    return wrap
