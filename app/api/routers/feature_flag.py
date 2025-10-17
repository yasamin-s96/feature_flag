from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker

from app.core.response_wrapper import Response
from app.database.connections.async_postgres import get_session_maker
from app.repositories.feature_flag import FeatureFlagRepository
from app.schemas.request.feature_flag import CreateFeatureFlagRequestModel
from app.schemas.response.feature_flag import CreateFeatureFlagResponseModel
from app.services.feature_flag import FeatureFlagService

router = APIRouter(prefix="/feature_flags", tags=["Feature"])


@router.post(
    "",
    summary="Create new feature flag",
    response_model=Response[CreateFeatureFlagResponseModel],
)
async def create_feature_flag(
    feature_flag: CreateFeatureFlagRequestModel,
    session_maker: sessionmaker = Depends(get_session_maker),
):
    async with session_maker.begin() as session:
        new_feature = await FeatureFlagService(FeatureFlagRepository()).create(
            session, feature_flag
        )

    return Response(data=new_feature)