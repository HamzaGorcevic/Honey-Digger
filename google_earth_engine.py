import ee
import pandas as pd
import datetime

try:
    ee.Initialize()
except ee.EEException as e:
    print("Error initializing Earth Engine:", e)
    raise

def get_ndvi_data(latitude, longitude, weather_data):
    if not isinstance(weather_data, pd.DataFrame) or 'date' not in weather_data.columns:
        raise ValueError("weather_data must be a pandas DataFrame with a 'date' column")
    
    try:
        if pd.api.types.is_datetime64_any_dtype(weather_data['date']):
            year_months = sorted(set(weather_data['date'].dt.strftime('%Y-%m')))
        elif pd.api.types.is_string_dtype(weather_data['date']):
            year_months = sorted(set(weather_data['date'].str[:7]))  # Extract YYYY-MM
        else:
            raise ValueError("Unsupported dtype for 'date' column; must be datetime or string (YYYY-MM-DD)")
    except (ValueError, TypeError) as e:
        raise ValueError("Could not extract year-month from weather_data['date']: " + str(e))

    if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
        raise ValueError("Invalid coordinates: latitude and longitude out of range")

    point = ee.Geometry.Point([longitude, latitude])

    def get_monthly_ndvi(year, month):
        if year == 2015 and month < 7:
            print(f"Skipping {year}-{month:02d}: Sentinel-2 data unavailable before July 2015.")
            return None

        start_date = f'{year}-{month:02d}-01'
        end_date = ee.Date(start_date).advance(1, 'month').advance(-1, 'day')

        def mask_clouds(image):
            scl = image.select('SCL')
            # Keep valid pixels: 2 (dark area), 4 (vegetation), 5 (bare soil), 6 (water), 7 (unclassified), 11 (snow/ice)
            mask = scl.eq(2).Or(scl.eq(4)).Or(scl.eq(5)).Or(scl.eq(6)).Or(scl.eq(7)).Or(scl.eq(11))
            return image.updateMask(mask)

        collection = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(point) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)) \
            .map(mask_clouds)

        # Check if images are available
        if collection.size().getInfo() == 0:
            print(f"Warning: No images found for {year}-{month:02d} with cloud cover < 30%. NDVI will be None.")
            return None

        # Compute NDVI
        def add_ndvi(image):
            ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
            return image.addBands(ndvi)

        ndvi_collection = collection.map(add_ndvi).select('NDVI')

        # Reduce to median NDVI
        ndvi_image = ndvi_collection.median()

        # Sample NDVI at point
        try:
            sample = ndvi_image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point.buffer(100),  # 100m buffer
                scale=10
            )
            mean_ndvi = sample.get('NDVI').getInfo()
            return mean_ndvi if mean_ndvi is not None else None
        except ee.EEException as e:
            print(f"Error fetching NDVI for {year}-{month:02d}: {e}")
            return None

    # Compute NDVI for each year-month
    monthly_ndvi = {}
    for year_month in year_months:
        year, month = map(int, year_month.split('-'))
        monthly_ndvi[year_month] = get_monthly_ndvi(year, month)

    # Assign NDVI to weather_data
    if pd.api.types.is_datetime64_any_dtype(weather_data['date']):
        weather_data['NDVI'] = weather_data['date'].apply(
            lambda x: monthly_ndvi.get(x.strftime('%Y-%m'), None) if pd.notnull(x) else None
        )
    else:
        weather_data['NDVI'] = weather_data['date'].apply(
            lambda x: monthly_ndvi.get(str(x)[:7], None) if pd.notnull(x) and len(str(x)) >= 7 else None
        )

    return weather_data