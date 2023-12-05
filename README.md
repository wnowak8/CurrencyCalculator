# Exchange Rate Application

This application fetches exchange rate data from the NBP API, stores it in a PostgreSQL database, and provides a Flask web API to retrieve exchange rate information for specific currency codes.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)


## Prerequisites

Before running the application, ensure you have the following installed:

- Docker

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/wnowak8/CurrencyCalculator.git
   ```
2. Run the application:
- To build and start the project use the following command:
   ```bash
   docker-compose up
   ```
- To stop and remove the containers, networks and volumes use command:
   ```bash
   docker-compose down
   ```
3. Access the Application:

Frontend: Open your web browser and navigate to http://localhost:3000.
Backend: Flask application will be accessible at http://localhost:5000.