from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.auth import User, auth_router, get_current_user
from app.database import create_db_and_tables, get_session
from app.models import Pizzeria, PizzeriaCreate, PizzeriaRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    title="AI Pizza API",
    description="API for tracking pizzerias visited in Berlin",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to AI Pizza API"}


@app.get("/pizzerias", response_model=list[PizzeriaRead])
async def get_all_pizzerias(session: AsyncSession = Depends(get_session)):
    """Get all pizzerias."""
    result = await session.execute(select(Pizzeria))
    pizzerias = result.scalars().all()
    return pizzerias


@app.post("/pizzerias", response_model=PizzeriaRead, status_code=201)
async def create_pizzeria(
    pizzeria: PizzeriaCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create a new pizzeria. Requires authentication."""
    db_pizzeria = Pizzeria.model_validate(pizzeria)
    session.add(db_pizzeria)
    await session.commit()
    await session.refresh(db_pizzeria)
    return db_pizzeria
