FROM node:20.9-alpine AS builder

COPY frontend /app/frontend
WORKDIR /app/frontend

# Install vue-cli
#RUN yarn global add @vue/cli

# Building the production-ready application  code
RUN yarn install && yarn build

FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy the dist folder from the builder stage
COPY --from=builder app/frontend/dist frontend/dist

# Install poetry
RUN pip install poetry

# Copy the poetry files
COPY pyproject.toml poetry.lock ./

# Install the dependencies
RUN poetry config virtualenvs.create false 

RUN poetry install

# Copy the backend code
COPY backend backend
COPY definitions.py .
COPY app.py .

ENV PYTHONPATH="/app"

# Extract the dataset using the python script
RUN python backend/src/data/extract.py

# Expose the port
EXPOSE 80

# Run the application
CMD ["python", "app.py"]