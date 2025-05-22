# Set Python image
FROM python:3.12.3-slim

# Set working directory 
WORKDIR /project

# Copy dependency list into the container 
COPY requirements.txt .

# Install Python dependencies 
RUN pip install --no-cache-dir -r requirements.txt 

# Copy .env config file
COPY .env .env

# Copy Alembic config file 
COPY alembic.ini /project/alembic.ini

# Copy Alembic migrations directory 
COPY alembic /project/alembic

# Copy the rest of the application code into the container 
COPY ./app /project/app

# Set PYTHONPATH to allow 'app.' imports
ENV PYTHONPATH=/project

# Expose port 80 (default port for FastAPI behind proxy) 
EXPOSE 80

# Command to run the app using Uvicorn 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]