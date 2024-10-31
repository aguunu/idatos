from fastapi import APIRouter, Depends
from sqlalchemy.orm import (
    Session,
    aliased,
)

from ..dependencies import get_db
from ..models import Schedule, Trip

router = APIRouter(prefix="/schedule")


@router.get(
    "/{id}", description="Obtiene los horarios para el viaje con identificación `id`."
)
def get_trip_scheduling(id: int, db: Session = Depends(get_db)):
    response = [
        {
            "ordinal": x.ordinal,
            "arrivalTime": x.arrival_time,
        }
        for x in db.query(Schedule)
        .where(Schedule.trip_id == id)
        .order_by(Schedule.ordinal)
        .all()
    ]

    return response


@router.get(
    "/trips/{id}",
    description="Obtiene la lista de viajes que realiza la variante con identificación `id`.",
)
def get_trips(id: int, db: Session = Depends(get_db)):
    trips = aliased(Trip)
    schedule = aliased(Schedule)

    response = [
        {
            "tripId": x.id,
            "serviceId": x.service_id,
            "departure": z.arrival_time,
        }
        for (x, z) in db.query(trips, schedule)
        .filter((trips.variant_id == id) & (schedule.ordinal == 1))
        .join(schedule, onclause=schedule.trip_id == trips.id)
        .all()
    ]

    return response
