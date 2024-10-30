import json

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import (
    Session,
    aliased,
)

from ..dependencies import get_db
from ..models import RouteVariants, RouteVariantStops, Schedule, Stops, Trip

router = APIRouter(prefix="/schedule")


@router.get("/{id}")
def get_trip_scheduling(id: int, db: Session = Depends(get_db)):
    trip1 = aliased(Trip)
    route_variants = aliased(RouteVariants)
    route_variant_stops = aliased(RouteVariantStops)
    stops = aliased(Stops)

    response = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": json.loads(geom),
                "properties": {
                    "stopId": z.id,
                    "ordinal": x.ordinal,
                    "arrivalTime": x.arrival_time,
                },
            }
            for (x, z, geom) in db.query(
                Schedule, stops, func.ST_AsGeoJSON(stops.point)
            )
            .join(trip1, onclause=trip1.id == Schedule.trip_id)
            .join(route_variants, onclause=route_variants.id == trip1.variant_id)
            .join(
                route_variant_stops,
                onclause=(route_variant_stops.ordinal == Schedule.ordinal)
                & (trip1.variant_id == route_variant_stops.variant_id),
            )
            .join(stops, onclause=route_variant_stops.stop_id == stops.id)
            .where(Schedule.trip_id == id)
            .order_by(Schedule.ordinal)
            .all()
        ],
    }

    return response


@router.get("/trips/{variant_id}")
def get_trips(variant_id: int, db: Session = Depends(get_db)):
    trips = aliased(Trip)
    schedule = aliased(Schedule)

    response = [
        {
            "tripId": x.id,
            "serviceId": x.service_id,
            "departure": z.arrival_time,
        }
        for (x, z) in db.query(trips, schedule)
        .filter((trips.variant_id == variant_id) & (schedule.ordinal == 1))
        .join(schedule, onclause=schedule.trip_id == trips.id)
        .all()
    ]

    return response
