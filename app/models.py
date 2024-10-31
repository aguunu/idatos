from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, ForeignKey, String, Time
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .dependencies import Base


class MainRoutes(Base):
    __tablename__ = "mainRoutes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)


class RouteVariants(Base):
    __tablename__ = "variantRoutes"

    id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("mainRoutes.id"), nullable=False)
    origin: Mapped[str] = mapped_column(String(128), nullable=False)
    destination: Mapped[str] = mapped_column(String(128), nullable=False)
    upward: Mapped[bool] = mapped_column(Boolean, nullable=True)
    path: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="LINESTRING", srid=4326, spatial_index=True),
        nullable=True,
    )


class Stops(Base):
    __tablename__ = "stops"

    id: Mapped[int] = mapped_column(primary_key=True)
    point: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )


class RouteVariantStops(Base):
    __tablename__ = "variantRoutesStops"

    stop_id: Mapped[int] = mapped_column(ForeignKey("stops.id"), primary_key=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("variantRoutes.id"), primary_key=True
    )
    ordinal: Mapped[int] = mapped_column(primary_key=True)


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(ForeignKey("variantRoutes.id"))
    service_id: Mapped[int] = mapped_column()


class Schedule(Base):
    __tablename__ = "schedule"

    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), primary_key=True)
    ordinal: Mapped[int] = mapped_column(primary_key=True)
    arrival_time: Mapped[datetime] = mapped_column(Time)
    previous_day: Mapped[int] = mapped_column()
