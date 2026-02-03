import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

EXCEL_FILE = "events.xlsx"

def fetch_events(city="mumbai"):
    url = "https://www.district.in/events"  # robust explore page
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, timeout=20)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    events = []

    links = soup.find_all("a", href=True)

    for a in links:
        try:
            title = a.get_text(strip=True)
            link = a["href"]

            if not title or "/events/" not in link:
                continue

            if not link.startswith("http"):
                link = "https://www.district.in" + link

            events.append({
                "Event Name": title,
                "Date": "N/A",     # dynamic on site
                "Venue": "N/A",    # dynamic on site
                "City": city.title(),  # selected city tagged
                "Category": "Event",
                "URL": link,
                "Status": "Upcoming",
                "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception:
            continue

    return pd.DataFrame(events)

def update_excel(new_df):
    today = datetime.now().date()

    try:
        old_df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        new_df.to_excel(EXCEL_FILE, index=False)
        print("Excel file created with new events.")
        return

    combined = pd.concat([old_df, new_df], ignore_index=True)

    # Deduplicate by URL
    combined = combined.drop_duplicates(subset=["URL"], keep="last")

    # Expiry handling (future-ready)
    if "Date" in combined.columns:
        def update_status(row):
            try:
                event_date = pd.to_datetime(row["Date"], errors="coerce")
                if pd.notna(event_date) and event_date.date() < today:
                    return "Expired"
            except:
                pass
            return row["Status"]

        combined["Status"] = combined.apply(update_status, axis=1)

    combined.to_excel(EXCEL_FILE, index=False)
    print("Excel updated successfully.")

if __name__ == "__main__":
    city = input("Enter city (mumbai/delhi/bengaluru/pune/jaipur): ").strip().lower()
    df_new = fetch_events(city)

    if df_new.empty:
        print("No events found right now. Try again later.")
    else:
        update_excel(df_new)
        print(f"Done! {len(df_new)} events fetched (tagged for {city.title()}).")
