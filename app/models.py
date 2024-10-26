from .dependencies import Base
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    geom: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )
    # geom = Column(Geometry("POINT", srid=4326))
