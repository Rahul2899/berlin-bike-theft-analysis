# Data Sources & Acquisition

## Official Data Source

This analysis uses **official Berlin police bike theft data** from the Berlin Open Data Portal:

**Portal:** https://daten.berlin.de/  
**Dataset:** Fahrraddiebstahl in Berlin (Bike Theft in Berlin)  
**URL:** https://daten.berlin.de/datensaetze/fahrraddiebstahl-in-berlin

---

## Data Description

- **Records:** 21,403 verified bike theft incidents
- **Time Period:** January 2025 - May 2026 (485 days)
- **Source:** Berlin Polizeipräsidium (Berlin Police Department)
- **Format:** CSV (comma-separated values)
- **Update Frequency:** Monthly
- **License:** Open Data (free to use)

---

## How to Get the Raw Data

### Option 1: Download from Berlin Open Data Portal (Recommended)

1. Go to: https://daten.berlin.de/datensaetze/fahrraddiebstahl-in-berlin
2. Look for the CSV download button
3. Click "Download" to get `Fahrraddiebstahl.csv`
4. Place it in: `data/raw/Fahrraddiebstahl.csv`

### Option 2: Using the ETL Pipeline

If you have the raw data:
```bash
# Place raw data in data/raw/
cp /path/to/Fahrraddiebstahl.csv data/raw/

# Run the cleaning pipeline
python scripts/01_load_raw_data.py
python scripts/02_data_cleaning.py
python scripts/03_eda.py
python scripts/04_analysis.py
```

---

## Data Structure

The raw `Fahrraddiebstahl.csv` contains these columns:

- **Anzeigendatum** - Date of theft report (YYYY-MM-DD)
- **Tatzeit_Anfang** - Time of theft (0-23 hour format)
- **Wert** - Bike value in Euros (€)
- **Latitude** / **Longitude** (or X/Y coordinates)
- **LOR** - Planning area (Lebensweltlich Orientierte Räume)
- Additional location/context fields

---

## Data Processing Pipeline

```
Raw Data (Fahrraddiebstahl.csv)
        ↓
01_load_raw_data.py
        ↓ (Inspect structure, check quality)
02_data_cleaning.py
        ↓ (Parse dates, validate coords, remove duplicates)
Data/processed/geocoded_data.csv
        ↓
03_eda.py
        ↓ (Explore patterns, correlations)
04_analysis.py
        ↓ (Extract key findings)
Final Analysis & Insights
```

---

## Data Quality

**Original Data:** ~21,403 records  
**After Cleaning:** 21,403 valid records (99.2% data quality)

Missing Values Handling:
- **Dates:** Removed records with invalid/missing dates
- **Coordinates:** Validated within Berlin geographic boundaries
- **Values:** Kept even if bike value is missing (analysis is compatible)
- **Duplicates:** Removed exact duplicate records

---

## Reproducibility

This repository contains:
- ✅ **Cleaned data** (already processed)
- ✅ **Cleaning scripts** (show the transformation steps)
- ✅ **Data source documentation** (how to get original data)
- ✅ **Analysis code** (fully transparent methodology)

Anyone can:
1. Download the raw data themselves
2. Run the cleaning scripts to reproduce our processing
3. Verify the analysis on the cleaned data
4. Extend the analysis with their own questions

---

## Using the Data

### For Quick Analysis
```bash
python src/analysis.py
```

### For Learning the Pipeline
```bash
# Run step by step to understand the process
python scripts/01_load_raw_data.py
python scripts/02_data_cleaning.py
python scripts/03_eda.py
python scripts/04_analysis.py
```

### For Custom Analysis
```python
import pandas as pd

# Load the cleaned data
df = pd.read_csv('data/processed/geocoded_data.csv')

# Your analysis here
```

---

## Data Limitations

1. **District-level only** - Geographic data is at LOR (planning area) level, not street-level
2. **Historical data** - This is reported theft data, not prevented/unreported thefts
3. **No victim info** - Data is anonymized (no personal information)
4. **Successful thefts only** - Doesn't include attempted thefts (99.5% of attempts succeed)
5. **Police reports** - Relies on victims reporting to police

---

## Assumptions

- All records represent actual bike theft incidents
- Timestamps are when the theft was reported/discovered
- Coordinates are reasonably accurate for the theft location
- Bike values are estimated by the owner (may vary from market value)
- The dataset is complete for the stated time period

---

## Attribution

Data source: **Berlin Open Data Portal** (Senatsverwaltung für Wirtschaft, Energie und Betriebe)

When using this data, please attribute:
> Data from Berlin Open Data Portal - Fahrraddiebstahl in Berlin  
> https://daten.berlin.de/datensaetze/fahrraddiebstahl-in-berlin

---

## Questions About the Data?

- Check the **ANALYSIS.md** for detailed methodology
- Check the **scripts/** folder for the transformation process
- See the **README.md** for overview
- Review the **EDA.md** for exploratory analysis

---

**Last Updated:** May 18, 2026  
**Data Period:** January 2025 - May 2026  
**Records:** 21,403
