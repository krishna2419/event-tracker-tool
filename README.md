# Event Discovery & Tracking Tool

This tool automatically fetches upcoming events from public platforms (BookMyShow/District),
stores them in an Excel sheet, and updates them at regular intervals.

## Features
- Select city (Mumbai, Delhi, Bengaluru, Pune)
- Extracts event name, date, venue, city, category, URL, status
- Stores data in Excel (events.xlsx)
- Deduplicates events on every run
- Marks past events as expired
- Can be scheduled to run automatically

## Tech Stack
- Python
- requests
- beautifulsoup4
- pandas
- openpyxl

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/krishna2419/event-tracker-tool.git
cd event-tracker-tool
