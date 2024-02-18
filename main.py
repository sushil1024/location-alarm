from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import googlemaps

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# current_address = "some place on earth"
session_addresses = {}

@app.get("/")
async def read_index(request: Request, latitude: float = None, longitude: float = None):
    global session_addresses
    ip_address = request.client.host
    current_address = session_addresses.get(ip_address, "some place on earth")

    print("IP addess: ", ip_address)
    print("session_addresses: ", session_addresses)

    try:
        if (latitude is not None) and (longitude is not None):
            f = open('api_key.txt', 'r')
            api_key = f.read()

            gmaps = googlemaps.Client(key=api_key)
            reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
            current_address = reverse_geocode_result[0]['formatted_address']

    except Exception as e:
        print("Error in latitude and longitude: ", e)
    return templates.TemplateResponse("index.html", {"request": request, "latitude": latitude, "longitude": longitude, "current_address": current_address})


@app.get("/get-current-address")
async def send_location(request: Request):
    global session_addresses
    ip_address = request.client.host
    current_address = session_addresses.get(ip_address, "some place on earth")


    return templates.TemplateResponse("index.html", {"request": request, "current_address": current_address})

