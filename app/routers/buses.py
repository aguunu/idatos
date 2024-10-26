from ..dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from geoalchemy2.shape import to_shape
from ..models import Location
from ..schemas import (
    FeatureCollection,
    LocationProperties,
    LocationResponse,
    LocationsResponse,
)
from sqlalchemy.orm import (
    Session,
)

router = APIRouter(prefix="/locations")


@router.get("/", response_model=LocationsResponse)
def get_locations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    locations = db.query(Location).offset(skip).limit(limit).all()
    features = [
        LocationResponse(
            type="Feature",
            geometry=to_shape(
                location.geom
            ),  # Point(type="Point", coordinates=Position2D(0.123, 132.13)),
            properties=LocationProperties(id=location.id, name=location.name),
        )
        for location in locations
    ]
    response = FeatureCollection(type="FeatureCollection", features=features)
    return response


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db)):
    # location = db.query(
    #     Location.id, Location.name, func.ST_AsGeoJSON(Location.geom).label("geom")
    # ).filter(Location.id == location_id).first()
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    geometry = to_shape(location.geom)
    response = LocationResponse(
        type="Feature",
        geometry=geometry,  # json.loads(location.geom),
        properties=LocationProperties(id=location.id, name=location.name),
    )
    return response
