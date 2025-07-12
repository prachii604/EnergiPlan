import schedule
import time
import os

def update_data_and_model():
    print(" Updating dataset and retraining model...")
    os.system("python get_weather_and_generate_data.py")
    os.system("python train_model.py")
    print(" Updated and retrained successfully.")

#Now we will schedule the task
schedule.every(10).hours.do(update_data_and_model)

print("Scheduler started. Will run every 10 hours.")
while True:
    schedule.run_pending()
    time.sleep(60)
