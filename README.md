# Price Watcher API

A simple educational FastAPI project for managing products (name + url) with protection against duplicate URLs.  
The purpose of this project is to practice FastAPI, async SQLAlchemy, and basic CRUD operations without over-engineering.


## Features

- Healthcheck endpoint: `GET /health`
- Products API:
  - `POST /products` — create a product
  - `GET /products` — list products (pagination and sorting)
  - `GET /products/{id}` — get product by id
  - `PUT /products/{id}` — update product (name and/or url)
  - `DELETE /products/{id}` — delete product
- URL uniqueness validation:
  - returns **409 Conflict** if a product with the same URL already exists
- Clear and consistent validation error responses


## Tech Stack

- Python 3.12+
- FastAPI
- Async SQLAlchemy
- SQLite

## Project Structure

app/
├── api/ # HTTP routes and error handlers
├── db/ # database setup, models, sessions
├── schemas/ # Pydantic schemas (request / response)
├── services/ # business logic layer
└── main.py # application entry point

## Installation and Run

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload


