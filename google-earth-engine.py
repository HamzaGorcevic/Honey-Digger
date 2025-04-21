import ee
import pandas as pd

ee.Initialize()

# Define location and time
latitude = 44.7866
longitude = 20.4489
point = ee.Geometry.Point([longitude, latitude])

# Read weather data (for 3 years)
weather_data = pd.read_csv('weather.csv')

# Define years for which you want NDVI data (e.g., 2021, 2022, 2023)

years = [2023,2024,2025]
print(years)

# Function to get yearly NDVI for a given year
def get_annual_ndvi(year):
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'

    # Sentinel-2 image collection
    collection = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterBounds(point) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
    
    # Function to compute NDVI for each image
    def add_ndvi(image):
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return image.addBands(ndvi)
    
    # Add NDVI band to all images in the collection
    ndvi_collection = collection.map(add_ndvi).select('NDVI')

    # Reduce to median NDVI image for the year (you could also use mean or max)
    ndvi_image = ndvi_collection.median()

    # Sample NDVI at the point location (buffered area if needed)
    sample = ndvi_image.sample(
        region=point.buffer(1000),  # 1 km radius
        scale=10,
        numPixels=50
    )

    # Get results as a list of dictionaries and extract NDVI values
    features = sample.getInfo()['features']
    ndvi_values = [f['properties']['NDVI'] for f in features]
    
    # Calculate mean NDVI for the year (you could also calculate median or other stats)
    if len(ndvi_values) > 0:
        mean_ndvi = sum(ndvi_values) / len(ndvi_values)
    else:
        mean_ndvi = None

    return mean_ndvi

# Get NDVI for each year
annual_ndvi = {}
for year in years:
    annual_ndvi[year] = get_annual_ndvi(year)

# Add NDVI to your weather dataset (assuming you want to merge it with your weather data)
weather_data['NDVI'] = weather_data['date'].apply(lambda x: annual_ndvi[int(x[:4])])

# Print the updated dataframe
print(weather_data.head())

# so here i use gee free tier, i get data from satelite on specific location with defined radius of 1 km, defined by buffer of image, 
# for each year, so now i can predict currents year NDVI of specific location my current data has already data of 2025. What i plan to do is
# to make prediction for 2025 year with data i have temp, precipitation, winspeed etc and NDVI wich i already have for those years.
#NEXT IMPORTANT TASK IS TO COMBINE ALL OF THIS IN ONE FILE SO I DONT WASTE FREE API TIER 