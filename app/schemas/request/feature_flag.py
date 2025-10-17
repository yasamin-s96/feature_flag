from pydantic import BaseModel, Field, ConfigDict


class CreateFeatureFlagRequestModel(BaseModel):
    name: str = Field(..., max_length=100)
    key: str = Field(..., max_length=100)
    description: str | None = None
    is_enabled: bool = False
    rollout_percentage: float | None = Field(None, ge=0, le=100)

    model_config = ConfigDict(
        str_min_length=1,
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "Enable dark mode",
                "key": "dark_mode",
                "description": "Toggles dark mode for users",
                "is_enabled": True,
                "rollout_percentage": 50.0,
            }
        },
    )