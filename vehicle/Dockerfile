FROM python:latest
WORKDIR /vehicle
COPY . .
ENV PYTHONPATH="$PYTHONPATH:/vehicle"
RUN python3 -m pip install --user --no-cache-dir -r requirements.txt
CMD ["python", "api/app.py"]