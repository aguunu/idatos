import json

from fastapi import APIRouter, Depends
from geoalchemy2.shape import to_shape
from sqlalchemy import func
from sqlalchemy.orm import (
    Session,
)

from ..dependencies import get_db
from ..models import RouteVariantStops, Stops
from ..schemas import StopProperties, StopResponse, StopsResponse

router = APIRouter(prefix="/stops")


@router.get("/")
def get_stops(db: Session = Depends(get_db)) -> StopsResponse:
    stops = db.query(Stops).all()

    response = StopsResponse(
        type="FeatureCollection",
        features=[
            StopResponse(
                type="Feature",
                geometry=to_shape(s.point),
                properties=StopProperties(id=s.id),
            )
            for s in stops
        ],
    )

    return response


@router.get("/{id}")
def get_variant_stops(id: int, db: Session = Depends(get_db)):
    response = {
        "type": "Feature Collection",
        "features": [
            {
                "geometry": json.loads(geom),
                "properties": {
                    "stopId": y.id,
                    "ordinal": x.ordinal,
                },
            }
            for (x, y, geom) in db.query(
                RouteVariantStops, Stops, func.ST_AsGeoJSON(Stops.point)
            )
            .filter(RouteVariantStops.variant_id == id)
            .join(Stops, onclause=Stops.id == RouteVariantStops.stop_id)
            .all()
        ],
    }

    return response
