from decimal import Decimal
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field


class CreateCommonListingRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0, decimal_places=2)
    description: str = Field(max_length=500)
    category_id: int = Field(gt=0)
    game_id: int = Field(gt=0)


class CreateSkinListingRequest(CreateCommonListingRequest):
    type: Literal['skin']

    float_value: float = Field(ge=0, le=1)
    skin_name: str = Field(min_length=1, max_length=100)


class CreateServiceListingRequest(CreateCommonListingRequest):
    type: Literal['service']

    duration: int = Field(gt=0)
    service_type: str = Field(min_length=1, max_length=100)


class CreateGameListingRequest(CreateCommonListingRequest):
    type: Literal['game']

    platform: str = Field(min_length=1, max_length=50)
    game_type: str = Field(min_length=1, max_length=50)


CreateListingRequest = Annotated[
    Union[CreateSkinListingRequest, 
          CreateServiceListingRequest, 
          CreateGameListingRequest],
    Field(discriminator="type"),
]
