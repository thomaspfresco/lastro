'''
/utilities/scheduler/setup.py
-> scheduler setup
'''

from apscheduler.schedulers.background import BackgroundScheduler

from database.fetchData import fetchCSV

# ==================================================
# global vars
# ==================================================

scheduler = BackgroundScheduler()

# ==================================================
# methods
# ==================================================

def jobToAppContext(app,jobFunction):
    with app.app_context():
        try:
            result = jobFunction()
            print(f"Scheduled CSV fetch completed: {result}")
        except Exception as e:
            print(f"Error in scheduled CSV fetch: {e}")

# ==================================================
# init and clean methods
# ==================================================

def initScheduler(app):
    # fetch data from CSV job
    scheduler.add_job(
        func=lambda: jobToAppContext(app, fetchCSV),
        trigger='cron',
        hour=4, minute=0,
        timezone='Europe/Lisbon',
        id='fetchCSV_job',
        name='Fetch CSV Data',
        replace_existing=True
    )

    scheduler.start()

def cleanScheduler():
    if scheduler.running:
        scheduler.shutdown(wait=True)