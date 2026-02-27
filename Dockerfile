# Multi-stage build: build React app, then serve with Flask

# 1. frontend build stage
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
COPY frontend/vite.config.js ./
COPY frontend/tsconfig.json* ./  # if exists
COPY frontend/.eslintrc* ./
# copy rest of frontend sources
COPY frontend/src ./src
COPY frontend/public ./public
RUN npm install
RUN npm run build

# 2. backend stage
FROM python:3.11-slim
WORKDIR /app
# set environment
ENV PYTHONUNBUFFERED=1

# copy backend code
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
# copy backend sources
COPY backend ./backend
# copy built frontend output into backend static folder
COPY --from=frontend-builder /app/frontend/dist ./backend/frontend/dist

EXPOSE 5000
WORKDIR /app/backend
CMD ["python", "app.py"]
