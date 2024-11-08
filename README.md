version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
  redis:
    image: redis:alpine
  postgres:
    image: postgres:13
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
