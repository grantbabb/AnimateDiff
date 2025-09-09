FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["python", "infer.py", "--task", "flood", "--features", "{\"rainfall_mm\": 5, \"river_level_m\": 1.2, \"soil_saturation\": 0.8}"]
