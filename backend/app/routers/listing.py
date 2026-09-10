from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import get_current_user
from app.database import get_db
from app.schemas.listing import (
    CreateListingRequest,
    PatchListingRequest,
    CreateListingResponse,
)
from app.models.user import User
from app.services.listing import create_listing, modify_listing, remove_listing


listingRouter = APIRouter(prefix='/listings')

@listingRouter.post('', status_code=201, response_model=CreateListingResponse)
async def post_listing(session: Annotated[AsyncSession, Depends(get_db)],
                       user: Annotated[User, Depends(get_current_user)],
                       listing_data: Annotated[CreateListingRequest, Body()]):

    await create_listing(session, user, listing_data)

    return CreateListingResponse(
        message = f"Listing {listing_data.name} created successfully!"
    )


@listingRouter.patch("/{listing_id}", status_code=204)
async def patch_listing(session: Annotated[AsyncSession, Depends(get_db)],
                        user: Annotated[User, Depends(get_current_user)],
                        listing_id: Annotated[int, Path()],
                        listing_data: Annotated[PatchListingRequest, Body()]):
    
    await modify_listing(session, user, listing_id, listing_data)


@listingRouter.delete("/{listing_id}", status_code=204)
async def delete_listing(session: Annotated[AsyncSession, Depends(get_db)],
                         user: Annotated[User, Depends(get_current_user)],
                         listing_id: Annotated[int, Path()]):

    await remove_listing(session, user, listing_id)