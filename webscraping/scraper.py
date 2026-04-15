import requests
from database import insert_job

def scrape_jobs():
    print("🔍 Fetching jobs from Himalayas API...")
    url = "https://himalayas.app/jobs/api?q=python&limit=20"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        jobs = data.get("jobs", [])

        if not jobs:
            print("⚠️ No jobs returned from API.")
            return

        print(f"✅ Found {len(jobs)} jobs!")

        for job in jobs:
            try:
                title    = job.get("title", "").strip()
                company  = job.get("companyName", "").strip()
                location = job.get("locationRestrictions", ["Remote"])
                location = ", ".join(location) if isinstance(location, list) else location

                # Build salary string from min/max
                min_sal  = job.get("minSalary")
                max_sal  = job.get("maxSalary")
                currency = job.get("currency", "USD")
                if min_sal and max_sal:
                    salary = f"{currency} {min_sal:,} - {max_sal:,}"
                else:
                    salary = "Not listed"

                job_url  = job.get("applicationLink", "").strip()

                # Skip job if critical fields are missing
                if not title or not company or not job_url:
                    print(f"⚠️ Skipped incomplete job entry.")
                    continue

                insert_job(
                    title=title,
                    company=company,
                    location=location,
                    salary=salary,
                    job_url=job_url,
                    source="Himalayas"
                )

            except Exception as e:
                print(f"⚠️ Skipped a job due to error: {e}")
                continue

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch jobs: {e}")

if __name__ == "__main__":
    scrape_jobs()