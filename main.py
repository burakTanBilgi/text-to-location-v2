from fastapi import FastAPI, HTTPException, Query
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.extra.rate_limiter import RateLimiter

app = FastAPI()

@app.get("/get-location")
async def get_location(place: str = Query(..., description="Koordinatları alınacak yer ismi")):
    try:
        geolocator = Nominatim(user_agent="text-to-location", timeout=10)
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location = geocode(place)
        if location:
            return {
                "place": place,
                "latitude": location.latitude,
                "longitude": location.longitude
            }
        else:
            raise HTTPException(status_code=404, detail="Yer bulunamadı.")
    except GeocoderTimedOut:
        raise HTTPException(status_code=504, detail="Zaman aşımı hatası.")
    except GeocoderServiceError:
        raise HTTPException(status_code=502, detail="Servis hatası.")
