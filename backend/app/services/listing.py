from sqlalchemy import or_, select, update
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
from app.models.user import User, UserRole
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


async def modify_listing(session: AsyncSession, user: User, listing_id: int, listing_data: PatchListingRequest) -> None:

    general_listing_fields = {
        "name",
        "price",
        "description",
        "status"
    }

    data = listing_data.model_dump(
        exclude_unset=True,
        exclude={"type"},
    )

    general_listing_data = {
        key: value
        for key, value in data.items()
        if key in general_listing_fields
    } or {
        Listing.id: Listing.id, 
    }

    category_listing_data = {
        key: value
        for key, value in data.items()
        if key not in general_listing_fields
    }

    if isinstance(listing_data, PatchSkinListingRequest):
        category_listing = SkinListing
    elif isinstance(listing_data, PatchServiceListingRequest):
        category_listing = ServiceListing
    elif isinstance(listing_data, PatchGameListingRequest):
        category_listing = GameListing

    print(category_listing)

    result = await session.execute(
        update(Listing)
        .where(
            Listing.id == listing_id,
            Listing.seller_id == user.id,
            Listing.status != ListingStatus.DELETED,
        )
        .values(general_listing_data)
    )

    if result.rowcount == 0:
        listing_state = await session.scalar(
            select(Listing).where(Listing.id == listing_id)
        )
        if listing_state is None or listing_state.status == ListingStatus.DELETED:
            raise ListingNotFoundError("Listing not found.")
        
        if listing_state.seller_id != user.id:
            raise UnauthorizedListingAccessError("Not authorized to access this listing.")
        
        raise ListingNotFoundError("Listing not found.")


    if category_listing_data:
        result = await session.execute(
            update(category_listing)
            .where(
                category_listing.listing_id == listing_id
            )
            .values(category_listing_data)
        )

        if result.rowcount == 0:
            raise IncorrectListingCategoryError("Incorrect listing category.")


async def remove_listing(session: AsyncSession, user: User, listing_id: int) -> None:

    conditions = [
        Listing.id == listing_id,
        Listing.status != ListingStatus.DELETED,
    ]

    if user.role != UserRole.ADMIN:
        conditions.append(Listing.seller_id == user.id)

    result = await session.execute(
        update(Listing)
        .where(*conditions)
        .values(
            status = ListingStatus.DELETED
        )
    )

    if result.rowcount == 0:
        listing = await session.scalar(
            select(Listing).where(Listing.id == listing_id)
        )

        if listing is None or listing.status == ListingStatus.DELETED:
            raise ListingNotFoundError("Listing not found.")

        raise UnauthorizedListingAccessError("Not authorized to access this listing.")
