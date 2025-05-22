# Use official NGINX image as the base
FROM nginx:stable-alpine

# Copy custom nginx config file to replace the default
COPY nginx.conf /etc/nginx/nginx.conf

# Optional: If you serve static files from NGINX
# COPY ./static /usr/share/nginx/html

# Expose port 80
EXPOSE 80
