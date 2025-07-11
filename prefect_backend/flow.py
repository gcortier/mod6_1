import os
from prefect import flow, task
from prefect.logging import get_run_logger



os.environ.setdefault("PYTHONIOENCODING", "utf-8")
# os.environ.setdefault("PREFECT_API_URL", "http://127.0.0.1:4200/api")



@task(retries=2, retry_delay_seconds=1)
def check_random():
    logger = get_run_logger()
    logger.info("Checking random number generation...")
    import random

    random_number = random.random()
    logger.info(f"Generated random number: {random_number}")
    return random_number

@task(retries=2, retry_delay_seconds=1)
def retrain():
    logger = get_run_logger()
    logger.info("Retrain triggered!")
    raise Exception("Retrain failed!")  # Pour tester les retries

@task
def print_ok():
    logger = get_run_logger()
    logger.info("ok")
    
@flow
def periodic_check():
    number = check_random()
    if number < 0.5:
        retrain()
    else:
        print_ok()
        
        
        

if __name__ == "__main__":
    periodic_check.serve(
        name="every-10s",
        interval=10 
    )
