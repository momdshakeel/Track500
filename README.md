# MarketPulse 750

A free Streamlit web app that scans the **Nifty Total Market** (Nifty 500 + Nifty Microcap 250, about 750 NSE stocks)
for relative strength, momentum, and classic trend / pattern setups. Educational tool - not investment advice.

## What the app shows

- **RS Rating (1-99):** percentile rank of a weighted 3 / 6 / 9 / 12-month return (40 / 20 / 20 / 20%).
- **Minervini Trend Template:** the 8 conditions, plus RS-line new highs, RS "blue dot" and RSI.
- **Weinstein stages (1-4)**, sideways **bases**, **VCP setups** and **volume breakouts**.
- **Liquidity:** average daily traded value (close x volume) over 20 sessions; liquid = at least Rs 10 crore.
  The left sidebar can limit stock lists to liquid stocks.
- **Market-cap filter:** shares outstanding x latest close, in Rs crore.
- **Breadth and sector strength** (liquid stocks only): advancers / decliners, 52-week highs and lows, share of
  stocks above the 50 / 150 / 200-day averages, Stage 2 and Trend Template shares, and a sector ranking.
- Sortable, responsive tables, font choice, light / dark mode, CSV downloads.
- The classic left sidebar holds **Appearance**, stock filters, the custom screen builder, data status and refresh control.
- **Momentum Candidates:** a staged screen requiring a supportive benchmark (above its 10- and 20-day averages),
  price within 25% of its 52-week high and above its 50-day average, a base no deeper than 20%, a pivot within
  10%, and an RS line within 5% of its 52-week high. First-leg quality, 10/20-day base support, heavy-volume
  rejection, a strong first leg (roughly 40% or more, with stronger up candles and above-average volume),
  and price-action smoothness remain chart-review checks.

## How it works

```
GitHub Actions (weekdays ~5 pm IST)  ->  build_data.py  ->  latest scan + 30-day setup history
                                                                  |
                                      Streamlit app (app.py) reads data/  ->  opens in seconds
```

The heavy work (downloading prices from Yahoo Finance and calculating everything) happens once a day in a free
GitHub job. The app only reads the saved results, so visitors never wait and Yahoo is never called from the web server.
If `data/latest.csv` does not exist yet, the app falls back to calculating live (3-5 minutes).
For the VCP and Breakouts screens, the daily workflow also archives one full scan per market date under
`data/history/` and removes snapshots older than 30 calendar days. Their date selector applies the existing
sidebar filters to the chosen snapshot; the dashboard header and summary cards continue to show the latest scan.

## Repository layout

```
app.py                         the Streamlit app
ui.py                          look and feel (fonts, cards, tables)
nse500_rs_rating.py            all calculations
build_data.py                  the daily job
archive_scan.py                save a dated snapshot and prune history to 30 days
requirements.txt               Python packages for the app
.github/workflows/daily_scan.yml   the schedule (GitHub Actions)
.streamlit/config.toml         optional theme colour
data/                          created by the daily job - do not edit by hand
data/history/                  dated scan snapshots used by VCP / Breakouts history
```

## Setup (first time)

1. Create a **public** GitHub repository and upload the files above.
2. Repository **Settings -> Actions -> General -> Workflow permissions -> Read and write permissions -> Save**.
3. **Actions** tab -> **Daily scan** -> **Run workflow**. After 5-20 minutes a `data/` folder appears.
4. On share.streamlit.io choose **New app**, pick the repository, branch `main`, main file `app.py`, then **Deploy**.

## Running it

- The job runs every weekday at 11:30 UTC (5:00 pm IST). Start it by hand any time from the Actions tab.
- If a run fails, the previous good data stays in place and GitHub emails you.
- The app shows a warning when the data is more than 4 days old.
- GitHub can pause scheduled jobs in a repository with no activity for 60 days; click **Enable** in the Actions tab.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Job fails on "Save the results" with a permission error | Settings -> Actions -> General -> Workflow permissions -> Read and write |
| Job fails: "Yahoo returned too little data" | Yahoo was throttling; run the job again later |
| App says "calculating live" | `data/latest.csv` is missing - run the Daily scan job, then reboot the app |
| App shows an old date | Click **Reload latest data** in the sidebar, or reboot the app from Streamlit's menu |

## Method notes

- Liquid = 20-session average of close x volume of at least Rs 10 crore; RS ranks use every rated stock.
- Stocks with under 12 months of history or no Yahoo data are not rated.
- 52-week highs / lows use closing prices. Stages use the 150-day average (about 30 weeks).
- VCP, bases and breakouts are rule-based approximations - always confirm on a chart.
- The RS line is measured against the Nifty 500 index. Yahoo data can have gaps.
- Momentum Candidates uses the RS benchmark series as its market gate (Nifty 500, with Nifty 50 fallback).
  The gate requires the benchmark close above both its 10-day and 20-day averages; it uses the latest daily close.
