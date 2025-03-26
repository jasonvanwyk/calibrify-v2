# ============================================================================
# File Path: frontend/Dockerfile
# Description: Dockerfile for Nginx frontend service
# ============================================================================

FROM debian:12-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Nginx
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /usr/share/nginx/html/static \
    /usr/share/nginx/html/templates

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set permissions
RUN chown -R www-data:www-data /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 