from geojson_pydantic import Feature, FeatureCollection, Point
from pydantic import BaseModel, Field


class LocationProperties(BaseModel):
    id: int = Field()
    name: str = Field()


# geojson schema
LocationResponse = Feature[Point, LocationProperties]
LocationsResponse = FeatureCollection[LocationResponse]
