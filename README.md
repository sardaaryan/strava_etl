# Strava ETL Pipeline

This repository contains a **Serverless Strava ETL (Extract, Transform, Load) Pipeline** designed to automate the synchronization of fitness data to a personal portfolio website. It leverages GitHub Actions as a persistent orchestrator to pull, process, and push metrics without requiring a dedicated
backend server.

---

## 🚀 How It Works

The pipeline follows a three-stage automated process:

- [cite_start]**Extract**: The `api_client.py` uses a "Golden Ticket" refresh token to generate a fresh access token for every run[cite: 1]. It then fetches the latest activities from the Strava API and stores them in a local SQLite database (`strava.db`) to prevent duplicates.
- [cite_start]**Transform**: Using `pandas`, the `transform.py` script converts raw SI units (meters, seconds) into athlete-friendly metrics like miles and feet. It calculates weekly totals and formats average paces into "MM:SS" strings.
- **Load**: The `schedule.yml` workflow commits the updated database back to this repository and pushes a lightweight `metrics.json` directly to your portfolio's data folder.

---

## 📂 Project Structure

Based on the repository layout, the core logic is organized as follows:

| Directory/File           | Purpose                                                                                           |
| :----------------------- | :------------------------------------------------------------------------------------------------ |
| **`.github/workflows/`** | Contains `schedule.yml`, which handles the CRON scheduling and cross-repo syncing.                |
| **`src/`**               | Includes `api_client.py` for OAuth, `extract.py` for ingestion, and `transform.py` for analytics. |
| **`data/`**              | The storage hub for the SQLite database and the generated JSON metrics.                           |
| **`init_db.py`**         | [cite_start]Utility script to initialize the SQLite schema for local development.                 |
| **`.env.example`**       | [cite_start]A template for required Strava API credentials and refresh tokens[cite: 1].           |

---

## 🛠️ Setup & Installation

### 1. Local Configuration

[cite_start]Create a `.env` file based on the provided example and fill in your Strava credentials[cite: 1]:

```bash
STRAVA_CLIENT_ID="your_id"
STRAVA_CLIENT_SECRET="your_secret"
STRAVA_REFRESH_TOKEN="your_refresh_token"
```

### 2. Ready to use after!
