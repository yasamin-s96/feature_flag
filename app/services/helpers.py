
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.core.exceptions import BadRequestException


async def raise_if_not_exists(
    db: AsyncSession,
    repository: BaseRepository,
    err_message: str = "Item not found",
    **condition_criteria,
):
    item_exists = await repository.exists(db, **condition_criteria)
    if not item_exists:
        raise HTTPException(status_code=404, detail=err_message)

async def raise_if_exists(
    db: AsyncSession,
    repository: BaseRepository,
    err_message: str,
    **condition_criteria,
):
    item_exists = await repository.exists(db, **condition_criteria)
    if item_exists:
        raise BadRequestException(detail=err_message)