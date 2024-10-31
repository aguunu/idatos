import json

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import (
    Session,
    aliased,
)

from ..dependencies import get_db
from ..models import MainRoutes, RouteVariants, RouteVariantStops

router = APIRouter(prefix="/routes")


@router.get("/", description="Obtiene la lista de líneas registradas en el sistema.")
def get_main_routes(db: Session = Depends(get_db)):
    response = [{"id": r.id, "name": r.name} for r in db.query(MainRoutes).all()]
    return response


@router.get(
    "/{name}",
    description="Obtiene la lista de variantes asociadas a la línea especificada por el parámetro `name`.",
)
def get_main_route(name: str, db: Session = Depends(get_db)):
    main_routes = aliased(MainRoutes)
    route_variants = aliased(RouteVariants)

    response = [
        {
            "routeId": r.route_id,
            "variantId": r.id,
            "origin": r.origin,
            "destination": r.destination,
            "upward": r.upward,
        }
        for r in db.query(route_variants)
        .join(main_routes, onclause=main_routes.id == route_variants.route_id)
        .where(main_routes.name == name)
        .all()
    ]

    return response


@router.get(
    "/variants/{id}",
    description="Obtiene los detalles de una variante específica identificada por su `id`. La respuesta incluye todos los atributos asociados a la variante, así como su representación geoespacial en formato GeoJSON.",
)
def get_variant_info(id: str, db: Session = Depends(get_db)):
    route_variants = aliased(RouteVariants)
    r = (
        db.query(route_variants, func.ST_AsGeoJSON(route_variants.path).label("path"))
        .filter(route_variants.id == id)
        .first()
    )

    if not r:
        return {}

    r, path = r

    response = {
        "type": "Feature",
        "geometry": json.loads(path) if path else None,
        "properties": {
            "variantId": r.id,
            "routeId": r.route_id,
            "origin": r.origin,
            "destination": r.destination,
            "upward": r.upward,
        },
    }

    return response


@router.get(
    "/variants/stop/{stop_id}",
    description="Obtiene todas las variantes de ruta asociadas a la parada con el `id` especificado.",
)
def get_variants_by_stop(stop_id: int, db: Session = Depends(get_db)):
    route_variants = aliased(RouteVariants)
    route_variant_stops = aliased(RouteVariantStops)

    variants = (
        db.query(route_variants)
        .join(route_variant_stops, route_variant_stops.variant_id == route_variants.id)
        .filter(route_variant_stops.stop_id == stop_id)
        .all()
    )

    response = [
        {
            "variantId": variant.id,
            "routeId": variant.route_id,
            "origin": variant.origin,
            "destination": variant.destination,
            "upward": variant.upward,
        }
        for variant in variants
    ]

    return response
