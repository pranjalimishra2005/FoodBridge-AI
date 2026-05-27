import os
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

# ---------------------------------------------------------
# LOAD ENV
# ---------------------------------------------------------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------
# IMPORT MODELS
# ---------------------------------------------------------
from backend.db.database import Base

from backend.models.user import User
from backend.models.donation import Donation
from backend.models.ngo import NGO
from backend.models.claim import Claim
from backend.models.food_item import FoodItem

target_metadata = Base.metadata

# ---------------------------------------------------------
# DATABASE URL
# ---------------------------------------------------------
sync_url = os.getenv("DATABASE_URL_SYNC")

if not sync_url:
    raise ValueError(
        f"\n🚨 DATABASE_URL_SYNC not found.\n"
        f"Expected .env at: {env_path}"
    )

config.set_main_option("sqlalchemy.url", sync_url)

# ---------------------------------------------------------
# OFFLINE MIGRATIONS
# ---------------------------------------------------------
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# ---------------------------------------------------------
# ONLINE MIGRATIONS
# ---------------------------------------------------------
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()