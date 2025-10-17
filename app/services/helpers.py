
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository, T
from app.core.exceptions import BadRequestException, NotFoundException


async def raise_if_not_exists(
    db: AsyncSession,
    repository: BaseRepository,
    err_message: str = "Item not found",
    return_obj: bool = False,
    **filters,
) -> T | None:
    """
    Raises NotFoundException if no matching item exists in the repository.

    Args:
        db: The SQLAlchemy async session.
        repository: Repository instance with `exists` and `get_by_filter` methods.
        err_message: Message for the NotFoundException.
        return_obj: Whether to return the found object instead of None.
        **filters: Criteria used for lookup.
    """

    if return_obj:
        result = await repository.get_by_filter(db, limit=1, **filters)
    else:
        result = await repository.exists(db, **filters)

    if not result:
        raise NotFoundException(err_message)

    return result[0] if return_obj else None

async def raise_if_exists(
    db: AsyncSession,
    repository: BaseRepository,
    err_message: str,
    **filters,
):
    item_exists = await repository.exists(db, **filters)
    if item_exists:
        raise BadRequestException(detail=err_message)