from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.repositories.feature_flag import FeatureFlagRepository
from app.schemas.request.feature_flag import CreateFeatureFlagRequestModel
from app.services.helpers import raise_if_exists, raise_if_not_exists


class FeatureFlagService:
    def __init__(self, feature_flag_repo: FeatureFlagRepository):
        self.feature_flag_repo = feature_flag_repo

    async def create(self, db: AsyncSession, input_data: CreateFeatureFlagRequestModel):
        await raise_if_exists(db,
                self.feature_flag_repo,
                err_message="There's already a feature flag with this key",
                key=input_data.key)
        return await self.feature_flag_repo.create(db, **input_data.model_dump(exclude_unset=True))

