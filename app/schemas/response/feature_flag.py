from pydantic import BaseModel


class CreateFeatureFlagResponseModel(BaseModel):
    id: int
    name: str
    key: str
    description: str | None = None
    is_enabled: bool = False
    rollout_percentage: float | None = None