# 🔴 Mars Explorer Hub

A stunning Streamlit dashboard that brings Mars to your screen! Explore real-time Martian weather conditions and the latest rover imagery from NASA's Mars missions.

![Mars Explorer Hub](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **🌡️ Martian Weather Dashboard**: View temperature, atmospheric pressure, and seasonal data from NASA's InSight lander
- **📊 Interactive Temperature Trends**: Plotly-powered charts showing temperature fluctuations over the last 7 Sols (Martian days)
- **📸 Live Rover Gallery**: Browse the latest photos from Curiosity and Perseverance rovers
- **🔄 Unit Converter**: Toggle between Celsius and Fahrenheit with a single click
- **⚡ Smart Caching**: Efficient API calls with Streamlit's caching to respect NASA's rate limits
- **🎨 Mars-Themed UI**: Beautiful dark theme with red/orange accents inspired by the Red Planet

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- NASA API key (free from [api.nasa.gov](https://api.nasa.gov))

### Local Installation

1. **Clone the repository**
   ```bash
   cd /home/ofri/code/Dataloom/Mars
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   NASA_API_KEY = "your_api_key_here"
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Mars Explorer Hub"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository and `app.py`
   - Add your NASA API key in **App Settings → Secrets**:
     ```toml
     NASA_API_KEY = "your_api_key_here"
     ```
   - Click "Deploy"!

## 📁 Project Structure

```
Mars/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration and API settings
├── requirements.txt                # Python dependencies
│
├── .streamlit/
│   ├── config.toml                # Streamlit theme configuration
│   └── secrets.toml               # API keys (not committed)
│
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   └── nasa_client.py         # NASA API client with caching
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── weather_components.py  # Weather UI components
│   │   └── photo_gallery.py       # Photo gallery components
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py              # Utility functions
│
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore file
└── README.md                       # This file
```

## 🛠️ Tech Stack

- **Frontend Framework**: [Streamlit](https://streamlit.io) 1.30+
- **Data Processing**: [Pandas](https://pandas.pydata.org) 2.0+
- **Visualizations**: [Plotly](https://plotly.com) 5.18+
- **HTTP Requests**: [Requests](https://requests.readthedocs.io) 2.31+
- **Image Processing**: [Pillow](https://pillow.readthedocs.io) 10.0+
- **Configuration**: [python-dotenv](https://pypi.org/project/python-dotenv/) 1.0+

## 📡 NASA APIs Used

### InSight Weather API
Historical Mars weather data from the InSight lander (mission ended December 2022).

**Endpoint**: `https://api.nasa.gov/insight_weather/`

**Data Includes**:
- Temperature (min, max, average)
- Atmospheric pressure
- Martian season
- Sol (Martian day) number

### Mars Rover Photos API
Latest images from active Mars rovers.

**Endpoint**: `https://api.nasa.gov/mars-photos/api/v1`

**Rovers Supported**:
- Curiosity (2012 - Present)
- Perseverance (2021 - Present)

## 🎯 Key Features Explained

### Smart Caching
The app uses Streamlit's `@st.cache_data` decorator to cache API responses for 1 hour, minimizing redundant calls and respecting NASA's rate limits (1,000 requests/hour).

### Error Handling
Comprehensive error handling for:
- API timeouts
- Rate limit exceeded (HTTP 429)
- Missing or malformed data
- Network connectivity issues

### Responsive Design
The UI adapts to different screen sizes using Streamlit's column layout and responsive image handling.

## 📝 Configuration

All configuration is centralized in `config.py`:

- `CACHE_TTL_SECONDS`: Cache duration (default: 3600s)
- `DEFAULT_NUM_PHOTOS`: Number of rover photos to display (default: 5)
- `MAX_SOLS_FOR_CHART`: Number of Sols for temperature chart (default: 7)

## 🔒 Security Notes

- ✅ API keys stored in `.streamlit/secrets.toml` (gitignored)
- ✅ `.env` file excluded from version control
- ✅ Secrets template provided in `.env.example`
- ⚠️ Never commit API keys to GitHub!

## 🐛 Troubleshooting

### "NASA API key not found"
- Ensure `.streamlit/secrets.toml` exists with your API key
- For Streamlit Cloud, check App Settings → Secrets

### "Rate limit exceeded"
- Wait a few minutes before refreshing
- NASA limits API calls to 1,000/hour

### "No weather data available"
- This is expected! InSight mission ended in December 2022
- The app displays historical data with appropriate warnings

### Photos not loading
- Check internet connectivity
- Verify the selected rover has recent photos
- Try switching to a different rover

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Add support for Mars 2020 Helicopter (Ingenuity) data
- Implement more weather visualization options
- Add downloadable photo gallery
- Include Mars facts and educational content

## 📄 License

MIT License - feel free to use this project for learning and portfolio purposes!

## 🙏 Acknowledgments

- **NASA** for providing free, open access to Mars mission data
- **Streamlit** for the amazing framework
- **Mars Rover Teams** for their incredible work exploring Mars

## 📧 Contact

Created as a portfolio project demonstrating:
- Python data science skills
- API integration
- Interactive data visualization
- Cloud deployment
- Production-ready code architecture

---

**Made with ❤️ and curiosity about the Red Planet** 🔴
