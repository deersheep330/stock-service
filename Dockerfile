FROM deersheep330/python-chrome-crontab

ENV TZ=Asia/Taipei

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

WORKDIR /home/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./stock ./stock

COPY ./symbol_entry.py .
COPY ./ptt_trend_entry.py .
COPY ./reunion_entry.py .
COPY ./institutions_entry.py .
COPY ./quote_entry.py .
COPY ./open_price_entry.py .
COPY ./close_price_entry.py .
COPY ./fastapi_entry.py .
COPY ./trend_chart_cronjob.py .
COPY ./institutions_chart_cronjob.py .

COPY ./cron_entrypoint.sh .
COPY ./wait-for-it.sh .

# Run the command on container startup
# https://stackoverflow.com/questions/37458287/how-to-run-a-cron-job-inside-a-docker-container
CMD /usr/local/bin/python symbol_entry.py && gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --access-logfile /proc/1/fd/1 fastapi_entry:app -D && /bin/bash ./cron_entrypoint.sh > /proc/1/fd/1 2>/proc/1/fd/2
# CMD ["cron", "-f"]

#Quick note about a gotcha:
#If you're adding a script file and telling cron to run it, remember to
#RUN chmod 0744 /the_script
#Cron fails silently if you forget.