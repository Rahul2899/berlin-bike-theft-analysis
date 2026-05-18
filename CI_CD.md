# CI/CD: Automated Daily Analysis Updates

## Overview

This repository includes **GitHub Actions** for automatic daily analysis updates. Every day, the latest Berlin Police bike theft data is downloaded, cleaned, and analyzed — keeping the analysis always current.

---

## 🤖 How It Works

### Daily Automation Schedule

```
⏰ Every day at 6:00 AM UTC:
├─ Download latest data from Berlin Police
├─ Clean and validate
├─ Run exploratory analysis (EDA)
├─ Run final analysis
├─ Commit changes if data updated
└─ Create release tag
```

**Workflow File:** `.github/workflows/update-analysis.yml`

---

## 📋 Pipeline Steps

### Step 1: Download Latest Data
```bash
curl -L "https://www.polizei-berlin.eu/Fahrraddiebstahl/Fahrraddiebstahl.csv" \
  -o data/raw/Fahrraddiebstahl.csv
```
- Downloads official Berlin Police data
- Saves to `data/raw/`
- ~2.8 MB file

### Step 2: Clean Data
```bash
python scripts/02_data_cleaning.py
```
- Parses dates (German format DD.MM.YYYY)
- Validates coordinates
- Extracts bike values
- Removes duplicates
- Creates derived features
- Output: `data/processed/geocoded_data.csv`

### Step 3: Exploratory Analysis
```bash
python scripts/03_eda.py
```
- Explores temporal patterns
- Analyzes geographic distribution
- Examines bike value correlations
- Checks data quality
- Generates insights

### Step 4: Final Analysis
```bash
python src/analysis.py
```
- Extracts 4 key findings
- Calculates statistics
- Generates summary
- Output: Console + `analysis_latest.txt`

### Step 5: Smart Commit
```bash
git commit -m "Auto-update: Latest Berlin bike theft data (YYYY-MM-DD)"
git push
```
- Only commits if data actually changed
- Includes date in commit message
- Pushes to GitHub

### Step 6: Release Tag
- Creates GitHub Release on data update
- Tags as `data-YYYY-MM-DD`
- Includes changelog
- Version history for tracking

---

## 📊 What Gets Updated Automatically

| File | Changes | Updated |
|------|---------|---------|
| `data/raw/Fahrraddiebstahl.csv` | Latest police data | ✅ Daily |
| `data/processed/geocoded_data.csv` | Cleaned records | ✅ If raw data changed |
| `analysis_latest.txt` | Latest findings | ✅ If data changed |
| README/visualizations | Manual update | ❌ Not automatic |

---

## 🎯 Example: What Happens Tomorrow

**Scenario:** Berlin Police releases new theft data at midnight

```
05:00 UTC  → GitHub runner starts
05:02 UTC  → Downloads new data (e.g., 22,200 records instead of 22,179)
05:03 UTC  → Cleans data using scripts/02_data_cleaning.py
05:04 UTC  → Runs EDA (discovers patterns)
05:05 UTC  → Runs final analysis
05:06 UTC  → Detects: data changed (22,200 vs 22,179 records)
05:07 UTC  → Creates commit: "Auto-update: Latest Berlin bike theft data (2026-05-19)"
05:08 UTC  → Pushes to GitHub
05:09 UTC  → Creates Release: "Data Update - 2026-05-19"
✅ GitHub repo updated with latest data
```

Your LinkedIn followers see "Last updated 30 minutes ago" 🎯

---

## 🔧 Manual Trigger

You can manually trigger the workflow anytime:

**Via GitHub UI:**
1. Go to **Actions** tab
2. Select **Daily Analysis Update**
3. Click **Run workflow**
4. Wait ~2 minutes

**Via GitHub CLI:**
```bash
gh workflow run update-analysis.yml
```

**Via curl:**
```bash
curl -X POST \
  -H "Accept: application/vnd.github.v3+raw+json" \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/YOUR_USERNAME/berlin-bike-theft-analysis/actions/workflows/update-analysis.yml/dispatches \
  -d '{"ref":"main"}'
```

---

## ✅ Success Indicators

### ✓ Workflow Succeeded
- Green checkmark in **Actions** tab
- New commit on `main` branch
- `data/processed/geocoded_data.csv` updated
- New Release tag created
- GitHub shows "Updated X minutes ago"

### ✗ Workflow Failed
- Red X in **Actions** tab
- No commit created
- Check workflow logs for errors
- Common issues:
  - Data source temporarily unavailable
  - Network timeout
  - Script error (Python dependency missing)

---

## 📋 Monitoring

### Check Workflow Status
```bash
# View workflow runs
gh run list --workflow=update-analysis.yml

# View latest run details
gh run view -w update-analysis.yml

# View logs
gh run view -w update-analysis.yml --log
```

### GitHub Actions Dashboard
- Go to **Actions** tab in GitHub
- Select **Daily Analysis Update**
- See:
  - ✅ All successful runs
  - ❌ Failed runs with error logs
  - ⏱️ Execution time
  - 📅 Schedule information

---

## 🛡️ Security Notes

### No Secrets Needed
- ✅ Public data source (Berlin Police)
- ✅ Public repository
- ✅ No API keys required
- ✅ No credentials needed
- ✅ Safe to commit

### Automatic Token
- GitHub Actions provides `GITHUB_TOKEN` automatically
- Used to create releases and push commits
- Only has access to your repository
- Revoked after workflow completes

---

## 📈 Data Update Frequency

**Current Schedule:** Daily at 6:00 AM UTC

To change the schedule, edit `.github/workflows/update-analysis.yml`:

```yaml
schedule:
  - cron: '0 6 * * *'  # Change this line
```

Cron format: `minute hour day-of-month month day-of-week`

**Examples:**
- `0 6 * * *` = Every day at 6 AM
- `0 */6 * * *` = Every 6 hours
- `0 9 * * 1-5` = Every weekday at 9 AM
- `0 0 * * 0` = Every Sunday at midnight

---

## 💡 Best Practices

### 1. Monitor First Run
After pushing to GitHub, watch the first automated run:
- Go to **Actions** tab
- Verify it downloads data correctly
- Check for any encoding/script issues

### 2. Test Manually
Before relying on automation:
```bash
# Run the pipeline locally
python scripts/02_data_cleaning.py
python src/analysis.py
```

### 3. Track Releases
GitHub automatically creates release tags:
- Shows data update history
- Can rollback if needed
- Provides version tracking

### 4. Alert on Failures
Optional: Add email/Slack notifications on failure
- GitHub has built-in notifications
- Can integrate with third-party services

---

## 📊 What This Means for Your Portfolio

### Before (Manual Updates)
- ❌ Analysis gets stale after a few days
- ❌ Have to manually re-run scripts
- ❌ GitHub shows "Last updated 1 month ago"
- ❌ Shows lack of DevOps knowledge

### After (Automated)
- ✅ Analysis always current (updated daily)
- ✅ No manual work
- ✅ GitHub shows "Last updated 2 hours ago"
- ✅ **Demonstrates DevOps/CI-CD skills**
- ✅ Impresses employers

---

## 🚀 Future Enhancements

Consider adding:
- **Notifications:** Slack/email on data updates
- **Webhooks:** Trigger downstream analytics
- **Tests:** Automated validation of analysis results
- **Reporting:** Auto-generate PDF reports
- **Visualization:** Update charts automatically

---

## Troubleshooting

### Workflow Not Running
- Check if Actions are enabled (Settings → Actions)
- Verify workflow file syntax (`.yml` format)
- Check cron schedule is correct

### Data Download Fails
- Police data source might be temporarily down
- Try manual download: `curl https://www.polizei-berlin.eu/Fahrraddiebstahl/Fahrraddiebstahl.csv`
- Check network connectivity

### Encoding Errors
- Workflow uses `latin-1` encoding (correct for police data)
- If changes needed, edit `scripts/02_data_cleaning.py`

### Git Push Fails
- GitHub token might be revoked
- Verify `.github/workflows/update-analysis.yml` has correct permissions
- May need to enable "Allow GitHub Actions to create and approve pull requests"

---

## 📚 References

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Workflow Syntax:** https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- **Cron Syntax:** https://crontab.guru/
- **Berlin Police Data:** https://www.polizei-berlin.eu/Fahrraddiebstahl/

---

**Status:** ✅ Ready to Deploy  
**Automation:** ✅ Daily at 6:00 AM UTC  
**Data Freshness:** ✅ < 24 hours old  
**Portfolio Value:** ✅ High (DevOps skills demonstrated)
