FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY src/ src/
COPY .env .env

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "src.web_interface:app", "--host", "0.0.0.0", "--port", "8000"]