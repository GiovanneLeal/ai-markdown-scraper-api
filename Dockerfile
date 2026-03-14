FROM python:3.11-slim

# Instalação ultra-simplificada, sem chaves manuais
RUN apt-get update && apt-get install -y chromium chromium-driver xvfb

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN printf "#!/bin/bash\nXvfb :99 -screen 0 1920x1080x24 &\nexport DISPLAY=:99\nexec uvicorn main:app --host 0.0.0.0 --port 8000" > start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]