from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.listing import IncorrectListingCategoryError


async def incorrect_listing_category_error_handler(
    _: Request,
    exc: IncorrectListingCategoryError,
):
    return JSONResponse(
        status_code=422,
        content={
            "detail": str(exc)
        }
    )
