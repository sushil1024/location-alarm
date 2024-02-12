from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import gpsd

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    # return templates.TemplateResponse("index.html", {"request": request})

    loct = None

    try:
        gpsd.connect()
        loct = gpsd.get_current()

        print(loct.position())

    except Exception as e:
        print(f"Error: {e}")

    if loct is None:
        return {"location": "No location data available"}
    else:
        return {"location": f"{loct.position()}"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)