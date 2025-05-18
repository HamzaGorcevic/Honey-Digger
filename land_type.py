import requests

def get_land_type_nominatim(lat: float, lon: float) -> str:
    """
    Queries Nominatim Reverse API and returns the object's 'class' or 'type' (or 'category') tag.
    """
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "jsonv2",      
        "zoom": 18,
        "addressdetails": 0
    }
    headers = {"User-Agent": "honey-predictor-script"}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()     # error if non-200
    place = resp.json()
    
    land_type = place.get("category") or place.get("class") or place.get("type") or "unknown"
    return land_type.lower()
