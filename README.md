# 🍯 Honey Digger – Honey Prediction App

This Python application predicts honey production potential by collecting and analyzing data from:

- Weather APIs (temperature, humidity, wind speed)
- NDVI data from Google Earth Engine
- Land type data from Nominatim (OpenStreetMap)

## ✨ Features

- Fetches and processes environmental data
- Uses machine learning techniques to estimate honey yield
- Configurable via latitude and longitude values in the script

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Key packages used include:
- `earthengine-api`
- `google-api-python-client`
- `scikit-learn`
- `pandas`, `numpy`, `matplotlib`

## 🚧 Setup Instructions

### 1. Google Earth Engine Setup

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the following APIs:
   - Earth Engine API
   - Cloud Storage API
3. Install Earth Engine CLI and authenticate:

```bash
earthengine authenticate
```

4. Set your project ID (replace with your actual ID):

```bash
earthengine set_project your-project-id
```

## 🔄 Usage

1. Open `honey_digger.py`
2. Modify the `lat` and `lon` variables to the location of interest
3. Run the script:

```bash
python honey_digger.py
```

## 📊 Output

- Prints environmental data for the selected location
- Displays NDVI and land type
- Shows basic prediction for honey production potential

## 📅 Status

Tested and returns accurate results for honey yield estimation. Great starting point for beginners in ML and environmental data.

## 🙋 Contributing

Open to improvements! Feel free to submit pull requests or file issues.

## 📄 License

This project is licensed under the MIT License.

---

*Beginner-friendly, created for experimenting with ML and real-world data integration.*

