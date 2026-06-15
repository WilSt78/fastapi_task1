import asyncio
import logging

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.infrastructure.database import Base  # noqa
from src.infrastructure.models import (  # noqa
    categoriesModel,
    commentsModel,
    locationsModel,
    postsModel,
    usersModel,
)

config = context.config
target_metadata = Base.metadata

logger = logging.getLogger("alembic.env")


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    try:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
        logger.info("Async migrations completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise
    finally:
        await connectable.dispose()


def run_migrations_online():
    logger.info("Starting online migrations")
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
