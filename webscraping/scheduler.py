from apscheduler.schedulers.blocking import BlockingScheduler
from scraper import scrape_jobs

scheduler = BlockingScheduler()

# Schedule the scrape_jobs function to run every day at 08:00 AM
scheduler.add_job(scrape_jobs, 'interval', days=1)

print("Scheduler started...")
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass
