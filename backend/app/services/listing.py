from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.listing import (
    CreateListingRequest, 
    CreateGameListingRequest, 
    CreateServiceListingRequest, 
    CreateSkinListingRequest,
    PatchListingRequest,
    PatchGameListingRequest,
    PatchServiceListingRequest,
    PatchSkinListingRequest
)
from app.models.listing import Listing, ListingStatus
from app.models.user import User
from app.models.game_listing import GameListing
from app.models.service_listing import ServiceListing
from app.models.skin_listing import SkinListing
from app.exceptions.listing import ListingNotFoundError, CategoryNotFoundError, UnauthorizedListingAccessError, IncorrectListingCategoryError
from app.models.category import Category


async def create_listing(session: AsyncSession, user: User, listing_data: CreateListingRequest) -> None:
    category_id = await session.scalar(
        select(Category.id).where(Category.name == listing_data.type)
    )

    if category_id is None:
        raise CategoryNotFoundError("Category not found.")
    
    listing = Listing(
        name = listing_data.name,
        price = listing_data.price,
        description = listing_data.description,
        category_id = category_id,
        seller_id = user.id,
        game_id = listing_data.game_id
    )

    session.add(listing)

    await session.flush()

    if isinstance(listing_data, CreateSkinListingRequest):
        category_listing = SkinListing(
            listing_id = listing.id,
            float_value = listing_data.float_value,
            skin_name = listing_data.skin_name
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
            game_type = listing_data.game_type
        )

    session.add(category_listing)


async def verify_listing(session: AsyncSession, user: User, listing_id: int) -> Listing:
    listing = await session.get(Listing, listing_id)
    if listing is None:
        raise ListingNotFoundError("Listing not found.")
    elif listing.status == ListingStatus.DELETED:
        raise ListingNotFoundError("Listing not found.")
    elif listing.seller_id != user.id:
        raise UnauthorizedListingAccessError("Not authorized to access this listing.")
    return listing


async def modify_listing(session: AsyncSession, listing: Listing, listing_data: PatchListingRequest) -> None:
    if isinstance(listing_data, PatchSkinListingRequest):
        category_listing = await session.get(SkinListing, listing.id)
    elif isinstance(listing_data, PatchServiceListingRequest):
        category_listing = await session.get(ServiceListing, listing.id)
    elif isinstance(listing_data, PatchGameListingRequest):
        category_listing = await session.get(GameListing, listing.id)

    if category_listing is None:
        raise IncorrectListingCategoryError("Incorrect listing category.")

    data = listing_data.model_dump(
        exclude_unset=True,
        exclude={"type"},
    )

    general_fields = {
        "name",
        "price",
        "description",
        "status"
    }

    for field, value in data.items():
        if field in general_fields:
            setattr(listing, field, value)
        else:
            setattr(category_listing, field, value)