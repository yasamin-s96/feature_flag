from app.models.feature_flag import FeatureFlag
from app.core.base_repository import BaseRepository


class FeatureFlagRepository(BaseRepository[FeatureFlag]):
    model = FeatureFlag