import enum


class TargetTypeEnum(str, enum.Enum):
    user = "user"
    group = "group"
    environment = "environment"
