from decimal import Decimal
from typing import Annotated, Literal, Optional, Union
from pydantic import BaseModel, Field
from app.models.listing import ListingUpdateStatus


class CreateGeneralListingRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0, decimal_places=2)
    description: str = Field(max_length=500)
    game_id: int = Field(gt=0)


class CreateSkinListingRequest(CreateGeneralListingRequest):
    type: Literal['skin']

    float_value: float = Field(ge=0, le=1)
    skin_name: str = Field(min_length=1, max_length=100)


class CreateServiceListingRequest(CreateGeneralListingRequest):
    type: Literal['service']

    duration: int = Field(gt=0)
    service_type: str = Field(min_length=1, max_length=100)


class CreateGameListingRequest(CreateGeneralListingRequest):
    type: Literal['game']

    platform: str = Field(min_length=1, max_length=50)
    game_type: str = Field(min_length=1, max_length=50)


CreateListingRequest = Annotated[
    Union[CreateSkinListingRequest, 
          CreateServiceListingRequest, 
          CreateGameListingRequest],
    Field(discriminator="type"),
]


class CreateListingResponse(BaseModel):
    message: str


class PatchGeneralListingRequest(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=50, default=None)
    price: Optional[Decimal] = Field(gt=0, decimal_places=2, default=None)
    description: Optional[str] = Field(max_length=500, default=None)
    status: Optional[ListingUpdateStatus] = None


class PatchSkinListingRequest(PatchGeneralListingRequest):
    type: Literal['skin']

    float_value: Optional[float] = Field(ge=0, le=1, default=None)
    skin_name: Optional[str] = Field(min_length=1, max_length=100, default=None)


class PatchServiceListingRequest(PatchGeneralListingRequest):
    type: Literal['service']

    duration: Optional[int] = Field(gt=0, default=None)
    service_type: Optional[str] = Field(min_length=1, max_length=100, default=None)


class PatchGameListingRequest(PatchGeneralListingRequest):
    type: Literal['game']

    platform: Optional[str] = Field(min_length=1, max_length=50, default=None)
    game_type: Optional[str] = Field(min_length=1, max_length=50, default=None)


PatchListingRequest = Annotated[
    Union[PatchGameListingRequest,
          PatchServiceListingRequest,
          PatchSkinListingRequest],
    Field(discriminator="type"),
]