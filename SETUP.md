# Setup & Installation Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Quick Start (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/Rahul2899/berlin-bike-theft-analysis.git
cd berlin-bike-theft-analysis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Analysis
```bash
python src/analysis.py
```

You should see the key findings printed to console:
- Peak theft hour (6 PM)
- Weekday effect (3.1x multiplier)
- Bike value distribution
- Success rate (99.5%)

---

## What You Get

✅ **Analysis Results:** Key statistics printed to console  
✅ **Verified Data:** 21,403 cleaned records ready to explore  
✅ **Visualizations:** 4 professional charts in `visualizations/`  
✅ **Full Documentation:** Complete methodology in `ANALYSIS.md`

---

## Files Explained

```
berlin-bike-theft-analysis/
├── README.md                          ← Start here
├── ANALYSIS.md                        ← Detailed findings
├── SETUP.md                           ← This file
├── requirements.txt                   ← Dependencies
├── LICENSE                            ← MIT (open source)
│
├── data/
│   └── processed/
│       └── geocoded_data.csv          ← 21,403 incidents
│
├── visualizations/
│   ├── viz_1_peak_hour_expert.png     ← 6 PM peak
│   ├── viz_2_weekday_expert.png       ← Weekday effect
│   ├── viz_3_bike_value_expert.png    ← Price distribution
│   └── viz_4_success_rate_expert.png  ← 99.5% success
│
└── src/
    └── analysis.py                    ← Run this to verify
```

---

## Verify Installation

Run this command to verify everything works:

```bash
python src/analysis.py
```

**Expected output:**
- Dataset loaded: 21,403 records
- 4 findings printed with statistics
- No errors

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install -r requirements.txt
```

### "FileNotFoundError: data/processed/geocoded_data.csv"
Make sure you cloned the full repository with data files:
```bash
git clone https://github.com/Rahul2899/berlin-bike-theft-analysis.git
```

### Python version too old
```bash
python3 --version  # Should be 3.9+
```

---

## Next Steps

After installation:

1. **Read the findings:** `ANALYSIS.md`
2. **Explore the data:** `data/processed/geocoded_data.csv`
3. **View visualizations:** Open PNG files in `visualizations/`
4. **Understand the code:** Read comments in `src/analysis.py`

---

## Using the Data

The cleaned dataset is ready for your own analysis:

```python
import pandas as pd

df = pd.read_csv('data/processed/geocoded_data.csv')
print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
```

---

## Contributing

Found something interesting? Want to extend this analysis?

1. Fork the repository
2. Create a branch (`git checkout -b feature/your-insight`)
3. Make changes
4. Submit a pull request

---

## Questions?

- Check the README.md for overview
- Check ANALYSIS.md for detailed findings
- Open an issue on GitHub

---

**Status:** ✅ Ready to use  
**Last updated:** May 18, 2026
