import json

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import (
    Session,
    aliased,
)

from ..dependencies import get_db
from ..models import MainRoutes, RouteVariants

router = APIRouter(prefix="/routes")


@router.get("/")
def get_main_routes(db: Session = Depends(get_db)):
    response = [{"id": r.id, "name": r.name} for r in db.query(MainRoutes).all()]
    return response


@router.get("/{name}")
def get_main_route(name: str, db: Session = Depends(get_db)):
    main_routes = aliased(MainRoutes)
    route_variants = aliased(RouteVariants)

    response = {
        "name": name,
        "variants": [
            {
                "variantId": r.id,
                "origin": r.origin,
                "destination": r.destination,
                "upward": r.upward,
            }
            for r in db.query(route_variants)
            .join(main_routes, onclause=main_routes.id == route_variants.route_id)
            .where(main_routes.name == name)
            .all()
        ],
    }

    return response


@router.get("/variants/{id}")
def get_variant_info(id: str, db: Session = Depends(get_db)):
    route_variants = aliased(RouteVariants)
    r = db.query(route_variants, func.ST_AsGeoJSON(route_variants.path).label("path")).filter(route_variants.id == id).first()

    if not r:
        return {}

    r, path = r

    response = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": json.loads(path),
                "properties": {
                    "variantId": r.id,
                    "origin": r.origin,
                    "destination": r.destination,
                    "upward": r.upward,
                }
            }
        ]
    }

    return response
