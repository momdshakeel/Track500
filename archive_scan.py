"""Archive the daily full scan for the VCP / breakout history pilot.

Keep one dated snapshot per market session and retain only the last 30 calendar days.
The app uses these full-table snapshots to rebuild its VCP and breakout result views.
"""
import json
import os
from datetime import date, datetime, timedelta, timezone


DATA_DIR = "data"
HISTORY_DIR = os.path.join(DATA_DIR, "history")
KEEP_DAYS = 30
IST = timezone(timedelta(hours=5, minutes=30))


def main():
    with open(os.path.join(DATA_DIR, "meta.json"), encoding="utf-8") as handle:
        meta = json.load(handle)
    scan_date = date.fromisoformat(str(meta["as_of"])[:10])
    os.makedirs(HISTORY_DIR, exist_ok=True)

    filename = f"{scan_date.isoformat()}.csv"
    with open(os.path.join(DATA_DIR, "latest.csv"), "rb") as source:
        with open(os.path.join(HISTORY_DIR, filename), "wb") as target:
            target.write(source.read())

    cutoff = datetime.now(IST).date() - timedelta(days=KEEP_DAYS - 1)
    dates = []
    for name in os.listdir(HISTORY_DIR):
        if not name.endswith(".csv"):
            continue
        try:
            snapshot_date = date.fromisoformat(name[:-4])
        except ValueError:
            continue
        if snapshot_date < cutoff:
            os.remove(os.path.join(HISTORY_DIR, name))
        else:
            dates.append(snapshot_date)

    dates.sort(reverse=True)
    index = {
        "retention_days": KEEP_DAYS,
        "scans": [
            {"date": snapshot.isoformat(), "file": f"{snapshot.isoformat()}.csv"}
            for snapshot in dates
        ],
    }
    with open(os.path.join(HISTORY_DIR, "index.json"), "w", encoding="utf-8") as handle:
        json.dump(index, handle, indent=2)
        handle.write("\n")
    print(f"Archived scan for {scan_date}; keeping {len(dates)} snapshots from {cutoff} onward.")


if __name__ == "__main__":
    main()
