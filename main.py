from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send-location")
async def send_location(latitude: float, longitude: float):
    print(f"Latitude: {latitude}, Longitude: {longitude}")
    return {"latitude": latitude, "longitude": longitude}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
