from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import googlemaps

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class Location(BaseModel):
    latitude: float
    longitude: float

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send-location")
async def send_location(location: Location, request: Request):
    latitude = location.latitude
    longitude = location.longitude
    print(f"Latitude, Longitude: {location.latitude}, {location.longitude}")

    f = open('api_key.txt', 'r')
    api_key = f.read()

    gmaps = googlemaps.Client(key=api_key)
    reverse_geocode_result = gmaps.reverse_geocode((19.013944, 72.827631))

    current_address = reverse_geocode_result[0]['formatted_address']

    print(current_address)

    if 'grant road' in str(current_address).lower():
        print("We're in grant road")
    else:
        print("We're not anywhere")

    return templates.TemplateResponse("index.html", {"request": request, "latitude": latitude, "longitude": longitude})

