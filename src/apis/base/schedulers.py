from apscheduler.schedulers.background import BackgroundScheduler

def schedule():
    """
    register all scheduled job
    """
    try:
        scheduler = BackgroundScheduler(job_defaults={'max_instances': 3})
        # scheduler.add_job(changeTenantStatus, 'interval', minutes=3)
        scheduler.start()
    except Exception:  # noqa
        pass
