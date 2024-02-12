import gpsd

host = "localhost"
port = 2947

try:
    gpsd.connect(host=host, port=port)
    loc = gpsd.get_current()

    print(loc.position())

except Exception as e:
    print(f"Error: {e}")