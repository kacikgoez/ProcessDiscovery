FROM node:20.9-alpine AS builder

COPY frontend /app/frontend
WORKDIR /app/frontend

# Install vue-cli
#RUN yarn global add @vue/cli

# Building the production-ready application  code
RUN yarn install && yarn build

FROM continuumio/miniconda3

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "Prakitkum", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

WORKDIR /app

# Copy the dist folder from the builder stage
COPY --from=builder app/frontend/dist frontend/dist

# Copy the backend code
COPY backend backend
COPY app.py .

# Why is this necessary?
ENV PYTHONPATH "${PYTHONPATH}:/app/"
# Extract the dataset using the python script
RUN python backend/src/data/extract.py

# Expose the port
EXPOSE 80

# Run the application
CMD ["conda", "run", "--no-capture-output", "-n", "Prakitkum", "python", "app.py"]