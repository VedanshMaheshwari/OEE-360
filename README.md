# OEE-360 - Project Submission for NTT DATA
AI-Powered Chat Assistant for Manufacturing Analytics


# 💬 OEE-360: GenAI-Powered OEE Chat Assistant

**OEE-360** is an intelligent, conversational web application that allows users to analyze and interact with IoT sensor data from packaging devices in a biscuit manufacturing facility. Built using **Streamlit**, **Gemini LLM**, and **Plotly**, it enables real-time calculation and visualization of **Original Equipment Efficiency (OEE)** using natural language queries.

---

## 🚀 Features

- **ChatGPT-style Interface**: Interact with your IoT data using plain English questions.
- **OEE Breakdown**: Calculates and displays OEE along with Availability, Performance, and Quality KPIs.
- **Dynamic Filtering**: Filter data by Device ID, Location, and Month using natural queries.
- **Dashboard Visualization**: Beautiful KPI cards and interactive bar charts via Plotly.
- **GenAI Integration**: Uses **Google's Gemini LLM** to intelligently parse user queries.
- **Fallback Regex Parser**: Ensures reliability even when GenAI parsing fails.

---

## 🧠 Technologies Used

- **Python 3.10+**
- **Streamlit** – for the interactive web UI
- **Google Gemini API** – for GenAI-powered natural language understanding
- **Plotly** – for clean and modern charts
- **Pandas** – for data manipulation
- **OpenAI / Google Generative AI SDK** – for LLM integration

---

## 📁 Project Structure

📦 oee-360/ ├── app.py # Main Streamlit app ├── utils.py # All utility functions (OEE calc, data load, Gemini parsing) ├── data/ │ └── oee_data.xlsx # Default synthetic dataset ├── .env # Your Gemini API Key (not committed) ├── requirements.txt # Python dependencies └── README.md # Project documentation


---

## 📊 OEE Calculation

The app computes OEE using the standard formula:

OEE = Availability × Performance × Quality


Where:

- **Availability** = Actual Runtime / Planned Production Time
- **Performance** = Ideal Cycle Time × Total Count / Runtime
- **Quality** = Good Count / Total Count

---

## 📦 Getting Started

### 1. Clone the Repository

git clone https://github.com/your-username/oee-360.git
cd oee-360

###2. Install Dependencies
pip install -r requirements.txt

###3. Add Your Gemini API Key
Create a secret.toml file and add your API key:
GEMINI_API_KEY=your_gemini_api_key_here

###4. Run the App
streamlit run app.py


##📝 Example Queries
"OEE for PKG-005 in Mumbai in January 2025"

"How did PKG-015 perform in Hyderabad last July?"

"Show performance of PKG-010 in Chennai for March 2024"

🧪 Demo Screenshot
Add a screenshot here of your app running once available

🤝 Built For
This project was developed as part of an internship initiative for NTT DATA showcasing real-time analytics, IoT integration, and GenAI capabilities.

🛠️ Future Improvements
Add time-series graphs for trends.

Export reports as PDF/Excel.

Add more GenAI features (e.g., anomaly detection).

Enable real-time sensor data ingestion.

📄 License
MIT License — free for personal and educational use.

🙌 Acknowledgements
NTT Data

Streamlit

Google Gemini

Plotly
