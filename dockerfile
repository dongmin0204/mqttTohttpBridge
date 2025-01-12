FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 로컬의 aasxs 디렉토리를 이미지 내 /usr/share/aasxs 로 복사
COPY aasxs /usr/share/aasxs

COPY mqtt_to_rest.py .


COPY . .

CMD ["python", "mqtt_to_rest.py"]
