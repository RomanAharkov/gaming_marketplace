from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import get_current_user
from app.database import get_db
from app.schemas.listing import (
    CreateListingRequest,
    CreateSkinListingRequest,
    CreateServiceListingRequest,
    CreateGameListingRequest
)
from app.models.user import User
from app.models.listing import Listing
from app.models.game_listing import GameListing
from app.models.skin_listing import SkinListing
from app.models.service_listing import ServiceListing


listingRouter = APIRouter()

@listingRouter.post('/listings')
async def post_listing(session: Annotated[AsyncSession, Depends(get_db)],
                       user: Annotated[User, Depends(get_current_user)],
                       listing_data: Annotated[CreateListingRequest, Body()]):

    listing = Listing(
        name = listing_data.name,
        price = listing_data.price,
        description = listing_data.description,
        category_id = listing_data.category_id,
        seller_id = user.id,
        game_id = listing_data.game_id
    )
    
    session.add(listing)

    await session.flush()

    if isinstance(listing_data, CreateSkinListingRequest):
        category_listing = SkinListing(
            listing_id = listing.id,
            float_value = listing_data.float_value,
            name = listing_data.skin_name
        )
    elif isinstance(listing_data, CreateServiceListingRequest):
        category_listing = ServiceListing(
            listing_id = listing.id,
            duration = listing_data.duration,
            service_type = listing_data.service_type
        )
    elif isinstance(listing_data, CreateGameListingRequest):
        category_listing = GameListing(
            listing_id = listing.id,
            platform = listing_data.platform,
            type = listing_data.game_type
        )

    session.add(category_listing)

    return {'message': 'Listing created successfully!'}
    

