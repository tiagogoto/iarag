# -----------------------------
# Dockerfile

FROM python:3.10-sli


# Set workdir
WORKDIR /app

# Copy requirements and source
COPY requirements.txt
COPY . .


# Install Python packages

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

EXPOSE 8282
# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8282", "--reload"]