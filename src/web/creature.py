from fastapi import APIRouter, HTTPException, Response
from model.creature import Creature
import service.creature as service
from error import Duplicate, Missing
from collections import Counter
import plotly.express as px
from service.creature import get_all
import country_converter as coco

router = APIRouter(prefix="/creature")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()

@router.get("/map")
def map():
    creatures = service.get_all()
    iso2_codes = set(creature.country for creature in creatures)
    iso3_codes = coco.convert(names=iso2_codes, to="ISO3")
    fig = px.choropleth(
        locationmode="ISO-3",
        locations=iso3_codes
    )
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")

@router.get("/plot")
def plot():
    creatures = get_all()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    counts = Counter(creature.name[0] for creature in creatures)
    y = { letter: counts.get(letter, 0) for letter in letters }
    fig = px.histogram(x=list(letters), y=y, title="Creature Names", labels={"x": "Initial", "y": "Initial"})
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")

@router.get("/usa")
def usa():
    creatures = get_all()
    area_codes = list(set(creature.area for creature in creatures))
    print(area_codes)
    fig = px.choropleth(
        locationmode="USA-states",
        locations=area_codes
    )
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")

@router.get("/{name}")
def get_one(name) -> Creature:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch("")
@router.patch("/")
def modify(creature: Creature) -> Creature:
    try:
        return service.modify(creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{name}", status_code=204)
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)




