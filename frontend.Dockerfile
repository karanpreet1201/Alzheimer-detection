# Build Stage
FROM node:18-alpine AS builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Serve Stage
FROM nginx:alpine
# Copy built static files to NGINX html directory
COPY --from=builder /app/dist /usr/share/nginx/html
# Note: we need to redirect all traffic to index.html for React Router, providing an nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
