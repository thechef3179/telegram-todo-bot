FROM python:3.14-alpine3.24
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY app/main.py main.py
COPY app/db_controller.py db_controller.py
RUN mkdir logs assets

# # Setup an app user so the container doesn't run as the root user
# RUN useradd app
# USER app

CMD [ "python3", "-u", "main.py" ]
