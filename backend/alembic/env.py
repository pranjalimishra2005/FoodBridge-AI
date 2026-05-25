import os
from logging.config import fileConfig
from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# ---------------------------------------------------------
# 1. BULLETPROOF .ENV LOADING
# ---------------------------------------------------------
# Explicitly get the absolute path to backend/.env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# Grab the Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------
# 2. MODEL METADATA LINKING
# ---------------------------------------------------------
from backend.db.database import Base
from backend.models import user, donation, ngo, claim, food_item # This triggers __init__.py so Alembic sees your tables

target_metadata = Base.metadata

# ---------------------------------------------------------
# 3. THE "KILL SWITCH" URL OVERRIDE
# ---------------------------------------------------------
sync_url = os.getenv("DATABASE_URL_SYNC")

# If it can't find the URL, crash loudly with a clear message:
if not sync_url:
    raise ValueError(
        f"\n🚨 CRITICAL ERROR: Alembic cannot find 'DATABASE_URL_SYNC'!\n"
        f"Looking for .env file at: {env_path}\n"
        f"Make sure the file exists and contains DATABASE_URL_SYNC=postgresql://..."
    )

# Inject the real URL into Alembic (bypassing alembic.ini)
config.set_main_option("sqlalchemy.url", sync_url)


# ---------------------------------------------------------
# 4. STANDARD ALEMBIC RUNNERS
# ---------------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()