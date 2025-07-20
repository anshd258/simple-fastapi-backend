# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
# Install system dependencies if needed
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ ./code/

# Copy application code
COPY . .


# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]