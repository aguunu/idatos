from geojson_pydantic import Feature, FeatureCollection, Point
from pydantic import BaseModel, Field

class RouteVariantProperties(BaseModel):
    id: int = Field()
    route_id: int = Field()
    upward: bool = Field()
    origin: str = Field()
    destination: str = Field()

class StopProperties(BaseModel):
    id: int = Field()


class RouteVariantStopsProperties(BaseModel):
    stop: StopProperties = Field()
    ordinal: int = Field()

class MainRouteVariantsResponse(BaseModel):
    name: str = Field()
    id: int = Field()
    variants: list[RouteVariantProperties]

StopResponse = Feature[Point, StopProperties]
StopsResponse = FeatureCollection[StopResponse]
