# CeFi DeFi Arbitrage
A simple Cefi-Defi live arbitrage 
opportunity detection tool

# Project Architecture
There are 3 apps in this project. 
- cefi app, where crypto prices are pulled using the Binance public api
- defi app, where crypto prices are pulled from the 1inch data aggregator
- arbitrage app, the prices between the cefi and defi are compared to identify arbitrage opportunities

The cefi and defi apps are APIs with processes running in the background to pull prices. 

The arbitrage app is a Flask web application which displays a dashboard with the prices, expected profit and is 
used to notify the user when there is an arbitrage opportunity.

# Getting Started
In the command line navigate to the project folder (cefi-defi-arbitrage) and run:
```
docker-compose up -d
```
Next, to view the dashboard, open your Chrome browser and go to:
```
http://localhost:3002
```

# Unit Testing
Unit tests were written using the pytest library. There is a tests folder in each app. To run the unit tests, navigate to the project directory in 
the command line and type "pytest" followed by the path to the test file. An example is shown below to run the 
unit test from the cefi app: 

```
pytest cefi/tests/test_fetch_cefi_prices.py
```