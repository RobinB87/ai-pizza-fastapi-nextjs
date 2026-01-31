from datetime import datetime

from pydantic import BaseModel, model_validator
from sqlmodel import Field, SQLModel


class Location(BaseModel):
    lat: float
    lng: float


class Pizzeria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    address: str
    lat: float | None = None
    lng: float | None = None
    rating: float | None = None
    google_maps_url: str | None = None
    review: str | None = None
    visited_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PizzeriaCreate(BaseModel):
    name: str
    address: str
    location: Location | None = None
    rating: float | None = None
    google_maps_url: str | None = None
    review: str | None = None
    visited_at: datetime | None = None

    def to_db_model(self) -> dict:
        data = self.model_dump(exclude={"location"})
        if self.location:
            data["lat"] = self.location.lat
            data["lng"] = self.location.lng
        return data


class PizzeriaRead(BaseModel):
    id: int
    name: str
    address: str
    location: Location | None = None
    rating: float | None = None
    google_maps_url: str | None = None
    review: str | None = None
    visited_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="before")
    @classmethod
    def wrap_location(cls, data):
        if isinstance(data, dict):
            lat = data.pop("lat", None)
            lng = data.pop("lng", None)
        else:
            lat = getattr(data, "lat", None)
            lng = getattr(data, "lng", None)
        if lat is not None and lng is not None:
            if isinstance(data, dict):
                data["location"] = {"lat": lat, "lng": lng}
            else:
                data = dict(data.__dict__)
                data["location"] = {"lat": lat, "lng": lng}
        return data
