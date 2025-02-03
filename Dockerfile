# Use the official Selenium Chrome image
FROM selenium/standalone-chrome:latest

# Install Python and pip
RUN sudo apt-get update && sudo apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Command to run the application
CMD ["python3", "Adidas.py"]
