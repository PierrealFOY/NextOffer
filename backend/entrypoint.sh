#!/bin/bash

# Start Uvicorn
if [ "$ENV" = "prod" ]; then
    uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers &
else
    uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers --reload &
fi

# start cron job
cron -f

# wait for both processes to finish
wait
