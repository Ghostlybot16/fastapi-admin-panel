# Set Python image
FROM python:3.12.3-slim

# Set working directory 
WORKDIR /app

# Copy dependency list into the container 
COPY requirements.txt .

# Install Python dependencies 
RUN pip install --no-cache-dir -r requirements.txt 

# Copy the rest of the application code into the container 
COPY ./app /app

# Expose port 80 (default port for FastAPI behind proxy) 
EXPOSE 80

# Command to run the app using Uvicorn 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]