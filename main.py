from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import googlemaps
import mysql.connector

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Function to read database credentials from the file
def read_db_config(filename):
    db_config = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            db_config[key] = value
    return db_config

# Read database credentials from the file
db_credentials = read_db_config('dbconfig.txt')

print("db_credentials from txt: ", db_credentials)

# mysql database connection
db_connection = mysql.connector.connect(
    host=db_credentials['host'],
    user=db_credentials['user'],
    password=db_credentials['password'],
    database=db_credentials['database']
)
db_cursor = db_connection.cursor()

@app.on_event("shutdown")
def shutdown_event():
    db_cursor.close()
    db_connection.close()

# current_address = "some place on earth"
session_addresses = {}
dest = {}
alarmflag = {}

@app.get("/")
async def read_index(request: Request, latitude: float = None, longitude: float = None, destination: str = None):
    global session_addresses
    global dest
    global alarmflag
    ip_address = request.client.host
    current_address = session_addresses.get(ip_address, "some place on earth")

    try:
        if (latitude is not None) and (longitude is not None):
            f = open('api_key.txt', 'r')
            api_key = f.read()

            gmaps = googlemaps.Client(key=api_key)
            reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
            current_address = reverse_geocode_result[0]['formatted_address']
            session_addresses[ip_address] = current_address
            dest[ip_address] = destination

            # Check if the IP address already exists in the database
            db_cursor.execute("SELECT * FROM users WHERE ip = %s", (ip_address,))
            existing_user = db_cursor.fetchone()

            if existing_user:
                # Update the existing user's data
                db_cursor.execute("UPDATE users SET latitude = %s, longitude = %s, lastonline = CONVERT_TZ(NOW(), '+00:00', '+05:30') WHERE ip = %s", (latitude, longitude, ip_address))
            
            else:
                # Insert new user's data
                db_cursor.execute("INSERT INTO users (ip, latitude, longitude, lastonline) VALUES (%s, %s, %s, CONVERT_TZ(NOW(), '+00:00', '+05:30'))", (ip_address, latitude, longitude))

            db_connection.commit()

            if str(dest[ip_address]).lower() in str(session_addresses[ip_address]).lower() and str(dest[ip_address]).lower() != '':
                alarmflag[ip_address] = '1'
                print("UTH MADARCHOD!..")
            else:
                alarmflag[ip_address] = ''

            print("IP addess: ", ip_address)
            print("session_addresses: ", session_addresses)
            print("dest: ", dest)

    except Exception as e:
        print("Error in latitude and longitude: ", e)
    return templates.TemplateResponse("index.html", {"request": request, "latitude": latitude, "longitude": longitude, "current_address": current_address, "alarmflag": alarmflag})


@app.get("/get-current-address")
async def send_location(request: Request):
    global session_addresses
    ip_address = request.client.host
    current_address = session_addresses.get(ip_address, "some place on earth")


    return templates.TemplateResponse("index.html", {"request": request, "current_address": current_address})

