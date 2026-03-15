# Community Fever & Malaria Surveillance Initiative
### End-to-end digital disease surveillance system for rural Uganda

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

---

## What This Project Does

Rural clinics and schools in Uganda rely on paper-based health reporting. This causes delays in detecting fever and malaria clusters — meaning outbreaks grow before anyone notices.

This project builds a complete digital surveillance system:

- Field workers report cases via **KoboCollect mobile app**
- Data flows automatically through a **Python ETL pipeline**
- Records are stored in a **SQLite relational database**
- A live **Streamlit dashboard** shows trends, maps, and actionable insights in real time

**Result:** Health coordinators can see where fever and malaria are spreading — by district, by week, by rainfall — and act before cases surge.

---

## Live Dashboard

👉 **[Launch Dashboard →](https://community-fever-surveillance.streamlit.app/)**

---

## Project Scope

| Item | Detail |
|---|---|
| Geography | 4 districts — Arua, Gulu, Lira, Kampala |
| Data Volume | 1,000 records across districts |
| Collection Method | KoboCollect mobile app + KoboToolbox API |
| Database | SQLite (upgradeable to PostgreSQL) |
| Dashboard | Streamlit + folium maps |

---

## System Architecture
```
KoboCollect App
      ↓
KoboToolbox Server (API)
      ↓
Python ETL Pipeline
(extract → clean → validate → load)
      ↓
SQLite Database (surveillance.db)
      ↓
Analytics + Visualizations
      ↓
Streamlit Dashboard (live)
```

---

## Key Findings

- 🌧️ Fever cases spike **4–6 weeks after high rainfall** periods
- 🦟 Districts with low mosquito net usage show **significantly higher malaria positivity**
- 📍 Certain districts are consistent **hotspots** — identifiable on the heatmap
- 📊 Dashboard enables coordinators to filter by district and week in real time

---

## Dashboard Features

- **Top metrics** — total reports, fever cases, malaria positives
- **Weekly fever trend** — line chart per district
- **Malaria positivity rate** — bar chart by district
- **Mosquito net effect table** — positivity rate vs net usage
- **Interactive map** — markers + heatmap layer for fever clusters
- **Download buttons** — filtered CSV and chart PNGs

---

## Folder Structure
```
community_surveillance/
│
├── data/               # CSVs, saved plots, maps
├── database/           # surveillance.db
├── dashboard/
│    └── app.py         # Streamlit dashboard
├── notebooks/          # Jupyter notebooks — ETL, analysis, viz
├── forms/              # KoboToolbox XLSForm survey
├── requirements.txt
└── README.md
```

---

## How to Run Locally
```bash
# 1. Clone the repo
git clone https://github.com/chris-asianzu/community-malaria-surveillance.git
cd community-malaria-surveillance

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
cd dashboard
streamlit run app.py
```

---

## Technologies

| Layer | Tools |
|---|---|
| Data Collection | KoboCollect, KoboToolbox |
| ETL & Analysis | Python, pandas, SQLAlchemy, matplotlib, seaborn, folium |
| Database | SQLite |
| Dashboard | Streamlit, streamlit-folium |
| Version Control | Git, GitHub |

---

## What This Demonstrates

- End-to-end mobile data engineering
- API integration with real-world mobile survey platform
- ETL pipeline — extraction, cleaning, validation, loading
- Health data analytics with district-level trends
- Interactive dashboard built for non-technical decision makers

---

## Author

**Chris Asianzu Benjamin** — Data Analyst, Kampala Uganda  
[GitHub](https://github.com/chris-asianzu) · [LinkedIn](https://www.linkedin.com/in/chris-asianzu-9b52a538b) · b3ntana@gmail.com
