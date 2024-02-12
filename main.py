from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import gpsd

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Location(BaseModel):
    latitude: float
    longitude: float

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send-location")
async def send_location(location: Location):
    print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
    

    return {"latitude": location.latitude, "longitude": location.longitude}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
