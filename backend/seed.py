#!/usr/bin/env python
"""Seed the database with initial pizzeria data."""

import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from app.config import settings
from app.models import Pizzeria

SEED_FILE = Path(__file__).parent / "seed_data.json"


async def seed_database(force: bool = False):
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    with open(SEED_FILE) as f:
        data = json.load(f)

    async with async_session() as session:
        # Check if already seeded
        result = await session.execute(select(Pizzeria))
        existing = result.scalars().all()

        if existing and not force:
            print(f"Database already has {len(existing)} pizzerias. Use --force to reseed.")
            return

        if existing and force:
            print(f"Deleting {len(existing)} existing pizzerias...")
            for p in existing:
                await session.delete(p)
            await session.commit()

        # Insert pizzerias
        for pizzeria_data in data["pizzerias"]:
            # Convert nested location to flat lat/lng
            location = pizzeria_data.pop("location", None)
            if location:
                pizzeria_data["lat"] = location["lat"]
                pizzeria_data["lng"] = location["lng"]
            # Parse visited_at date string
            if pizzeria_data.get("visited_at"):
                pizzeria_data["visited_at"] = datetime.fromisoformat(pizzeria_data["visited_at"])
            pizzeria = Pizzeria(**pizzeria_data)
            session.add(pizzeria)
            print(f"Adding: {pizzeria.name}")

        await session.commit()
        print(f"\nSeeded {len(data['pizzerias'])} pizzerias!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database with pizzeria data")
    parser.add_argument("--force", action="store_true", help="Delete existing data and reseed")
    args = parser.parse_args()

    asyncio.run(seed_database(force=args.force))
