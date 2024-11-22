# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the DNS server script
COPY dns_proxy.py /app/dns_proxy.py
COPY requirements.txt /app/requirements.txt

# Install required Python libraries
RUN pip install -r requirements.txt

# Expose the port the DNS server will run on
EXPOSE 5354

# Run the DNS proxy server as the entrypoint
ENTRYPOINT ["python", "/app/dns_proxy.py"]
