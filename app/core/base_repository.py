from typing import Any, Generic, Type, TypeVar

from sqlalchemy import (
    Select,
    asc,
    delete,
    desc,
    false,
    func,
    inspect,
    literal,
    select,
    update,
)
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.database.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    model: Type[T]

    async def get_by_id(
        self,
        db: AsyncSession,
        id: int,
        load: list[str | tuple[str, str]] = None,
        exclude_inactive: bool = True,
    ) -> T | None:
        statement = self._resolve_base_query(exclude_inactive=exclude_inactive).where(
            self.model.id == literal(id)
        )

        if load:
            _options = []
            for item in load:
                if isinstance(item, str):
                    relation, loader_type = item, "selectin"
                else:
                    relation, loader_type = item
                if hasattr(self.model, relation):
                    _options.append(self._build_loader(relation, loader_type))

            if _options:
                statement = statement.options(*_options)

        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
        columns: list[str] | None = None,
        limit: int | None = None,
        sort: list[str] | None = None,
        search: dict[str, Any] | None = None,
        exclude_inactive: bool = True,
    ):
        """Get all records with optional column selection, limit, and sorting."""
        statement = self._resolve_base_query(
            columns=columns, exclude_inactive=exclude_inactive
        )
        statement = self._apply_sorting(statement, sort)

        statement = self._apply_search(statement, search)

        if limit:
            statement = statement.limit(limit)

        result = await db.execute(statement)
        return self._determine_return_format(result, custom_columns=columns)

    async def get_by_filter(
        self,
        db: AsyncSession,
        columns: list[str] | None = None,
        limit: int | None = None,
        sort: list[str] | None = None,
        exclude_inactive: bool = True,
        first: bool = False,
        **filters,
    ):
        """Get records by filters with optional column selection, limit, and sorting."""
        statement = self._resolve_base_query(
            columns=columns, exclude_inactive=exclude_inactive
        )

        for field, value in filters.items():
            if hasattr(self.model, field):
                column = getattr(self.model, field)
                # Handle lists/tuples/sets in queries
                if isinstance(value, (list, tuple, set)):
                    # Empty iterable means no matches
                    if not value:
                        statement = statement.where(false())
                    else:
                        statement = statement.where(column.in_(value))
                else:
                    statement = statement.where(column == literal(value))

        statement = self._apply_sorting(statement, sort)

        if limit:
            statement = statement.limit(limit)

        result = await db.execute(statement)
        return self._determine_return_format(result, custom_columns=columns)

    async def exists(self, db: AsyncSession, exclude_inactive=True, **filters) -> bool:
        """Check if a record exists with the given filters."""
        statement = self._resolve_base_query(exclude_inactive=exclude_inactive)

        # Apply filters
        for key, value in filters.items():
            if hasattr(self.model, key):
                statement = statement.where(getattr(self.model, key) == value)

        # Use EXISTS for better performance
        exists_statement = select(statement.exists())
        result = await db.execute(exists_statement)
        return bool(result.scalar())

    async def create(self, db: AsyncSession, **kwargs: Any) -> T:
        """Create a new record."""
        instance = self.model(**kwargs)

        if hasattr(instance, "created_at"):
            instance.created_at = func.now()
        if hasattr(instance, "updated_at"):
            instance.updated_at = func.now()

        db.add(instance)
        await db.flush()
        return instance

    async def update_by_filters(
        self, db: AsyncSession, values: dict, exclude_inactive: bool = True, **filters
    ) -> T | None:
        """Update a record by filters."""
        stmt = update(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                stmt = stmt.where(getattr(self.model, field) == value)

        stmt = self._resolve_base_query(
            statement=stmt, exclude_inactive=exclude_inactive
        )

        if hasattr(self.model, "updated_at"):
            values["updated_at"] = func.now()

        stmt = stmt.values(**values).returning(self.model)

        return (await db.execute(stmt)).scalar_one_or_none()

    async def update(self, instance: T, **kwargs: Any) -> T | None:
        """Update instance."""
        model_relations = await self._get_relationships()
        for field, value in kwargs.items():
            if field not in model_relations and hasattr(self.model, field):
                setattr(instance, field, value)

        if "updated_at" in instance.__mapper__.columns:
            instance.updated_at = func.now()

        return instance

    async def soft_delete(self, instance: T, modifier_id: int = None) -> None:
        """Soft delete an instance."""
        if hasattr(instance, "is_deleted"):
            instance.is_deleted = True
        if hasattr(instance, "deleted_at"):
            instance.deleted_at = func.now()
        if modifier_id and hasattr(self.model, "deleted_by"):
            instance.deleted_by = modifier_id

    async def hard_delete(self, db: AsyncSession, id: int) -> T | None:
        """Delete a record by its ID."""
        stmt = delete(self.model).where(id == self.model.id).returning(self.model)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def soft_delete_by_filters(
        self,
        db: AsyncSession,
        modifier_id: int = None,
        exclude_inactive=True,
        **filters,
    ):
        """Delete a record by filters."""
        stmt = update(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                stmt = stmt.where(getattr(self.model, field) == value)

        stmt = self._resolve_base_query(
            statement=stmt, exclude_inactive=exclude_inactive
        )

        # Setting soft delete values
        soft_delete_values = {"is_deleted": True, "deleted_at": func.now()}
        if modifier_id and hasattr(self.model, "deleted_by"):
            soft_delete_values["deleted_by"] = modifier_id

        stmt = stmt.values(**soft_delete_values).returning(self.model)

        return (await db.execute(stmt)).scalar_one_or_none()

    async def multiple_soft_delete_by_filters(
        self,
        db: AsyncSession,
        modifier_id: int = None,
        exclude_inactive=True,
        **filters,
    ):
        """Delete multiple records by filters."""
        stmt = update(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                stmt = stmt.where(getattr(self.model, field) == value)

        stmt = self._resolve_base_query(
            statement=stmt, exclude_inactive=exclude_inactive
        )

        # Setting soft delete values
        soft_delete_values = {"is_deleted": True, "deleted_at": func.now()}
        if modifier_id and hasattr(self.model, "deleted_by"):
            soft_delete_values["deleted_by"] = modifier_id

        stmt = stmt.values(**soft_delete_values).returning(self.model)

        return (await db.execute(stmt)).scalars().all()

    async def hard_delete_by_filters(self, db: AsyncSession, **filters):
        stmt = delete(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                stmt = stmt.where(getattr(self.model, field) == value)

        stmt = self._resolve_base_query(statement=stmt)
        stmt = stmt.returning(self.model)

        return (await db.execute(stmt)).scalar_one_or_none()

    async def multiple_hard_delete_by_filters(self, db: AsyncSession, **filters):
        """Delete multiple records by filters."""
        stmt = delete(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                stmt = stmt.where(getattr(self.model, field) == value)

        stmt = self._resolve_base_query(statement=stmt)
        stmt = stmt.returning(self.model)

        return (await db.execute(stmt)).scalars().all()

    async def count(
        self, db: AsyncSession, filters: dict[str, Any] | None = None
    ) -> int:
        """Count records with optional filters."""
        from sqlalchemy import func

        statement = select(func.count(self.model.id))

        # Apply soft delete and active filters
        if hasattr(self.model, "is_deleted"):
            statement = statement.where(self.model.is_deleted.is_(False))
        if hasattr(self.model, "is_active"):
            statement = statement.where(self.model.is_active.is_(True))

        # Apply additional filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    statement = statement.where(column == literal(value))

        result = (await db.execute(statement)).scalar()
        return 0 if result is None else int(result)

    def _resolve_base_query(
        self,
        statement=None,
        columns: list[str] | None = None,
        exclude_inactive: bool = True,
    ):
        """Resolve the base query with optional column selection and statement."""
        if statement is None:
            # Falls back to regular select statement
            if columns:
                # Select specific columns
                columns = [
                    getattr(self.model, column)
                    for column in columns
                    if hasattr(self.model, column)
                ]
                statement = select(*columns)
            else:
                # Select all columns from the model
                statement = select(self.model)

        # Apply soft delete filter
        if hasattr(self.model, "is_deleted"):
            statement = statement.where(self.model.is_deleted.is_(False))

        if exclude_inactive:
            if hasattr(self.model, "is_active"):
                statement = statement.where(self.model.is_active.is_(True))

        return statement

    def _determine_return_format(
        self, result: Result, custom_columns: list[str] | None = None, first: bool = False
    ):
        """Determine the appropriate return format based on query type."""
        if not custom_columns or len(custom_columns) == 1:
            result = result.scalars()
        else:
            result = result.mappings()

        if first:
            return result.first()
        return result.all()

    def _apply_sorting(self, statement, sort: list[str] | None = None):
        """Apply sorting to the given SQLAlchemy statement based on sort parameters."""
        if not sort:
            return statement

        for sort_item in sort:
            col, *order = sort_item.split(":")
            if hasattr(self.model, col):
                column = getattr(self.model, col)
                direction = (
                    desc(column)
                    if order and order[0].lower() == "desc"
                    else asc(column)
                )
                statement = statement.order_by(direction)

        return statement

    def _apply_search(self, statement, search: dict[str | Any] | None = None):
        """Apply search to the given SQLAlchemy statement based on search dict {'field': 'column', 'value': 'search value'}."""
        if not search:
            return statement

        field = search.get("field")
        value = search.get("value")
        if field and value:
            if hasattr(self.model, field):
                column = getattr(self.model, field)
                statement = statement.where(column.icontains(value))

        return statement

    async def _get_relationships(self):
        mapper = inspect(self.model)
        return [rel.key for rel in mapper.relationships]

    async def _resolve_extra_params(
        self,
        base_stmt: Select,
        search_column=None,
        order_by_allowed_fields: dict | None = None,
        order_by: str | None = None,
        direction: str = "asc",
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
    ):
        if search:
            base_stmt = base_stmt.where(search_column.icontains(search))

        # -------- total count query (without skip/limit) --------
        count_stmt = select(func.count().label("total")).select_from(
            base_stmt.subquery()
        )

        # -------- ordering --------
        if (
            order_by
            and order_by_allowed_fields is not None
            and order_by in order_by_allowed_fields
        ):
            order_by_field = (
                order_by_allowed_fields[order_by].asc()
                if direction == "asc"
                else order_by_allowed_fields[order_by].desc()
            )
            base_stmt = base_stmt.order_by(order_by_field)
        else:
            base_stmt = base_stmt.order_by(self.model.created_at.desc())

        # -------- pagination --------
        data_stmt = base_stmt.offset(skip).limit(limit)

        return count_stmt, data_stmt

    def _build_loader(self, relation, loader_type="selectin"):
        attr = getattr(self.model, relation)
        if loader_type == "joined":
            return joinedload(attr)
        return selectinload(attr)
