"""
Инициализация Alembic для миграций базы данных
"""

from alembic import command
from alembic.config import Config
import os


def init_alembic():
    """Инициализация Alembic"""
    
    # Создаем конфигурацию Alembic
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", "postgresql://user:password@localhost/fooddelivery")
    
    # Инициализируем Alembic (только если папка migrations пуста)
    if not os.path.exists("migrations/versions"):
        command.init(alembic_cfg, "migrations")
    
    return alembic_cfg


def create_migration(message: str):
    """Создать новую миграцию"""
    alembic_cfg = init_alembic()
    command.revision(alembic_cfg, autogenerate=True, message=message)


def upgrade_database():
    """Применить миграции"""
    alembic_cfg = init_alembic()
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    # Создаем первую миграцию
    create_migration("Initial migration")
    print("Migration created successfully!")
