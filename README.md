# CeFi DeFi Arbitrage
A simple Cefi-Defi live arbitrage 
opportunity detection tool

# Installing required packages
Please run the following commands to install the required libraries in the project's requirements.txt file
```
python -m pip install -r requirements.txt
```

# Project Architecture
There are 3 apps in this project. 
- cefi app, where crypto prices are pulled using the Binance public api
- defi app, where crypto prices are pulled from the 1inch data aggregator
- arbitrage app, the prices between the cefi and defi are compared to identify arbitrage opportunities

The cefi and defi apps are APIs with processes running in the background to pull prices. 

The arbitrage app is a Flask web application which displays a dashboard with the prices, expected profit and is 
used to notify the user when there is an arbitrage opportunity.

# Steps to get started
1. Please run app.py found in cefi-defi-arbitrage/cefi/app.py
2. Please run app.py found in cefi-defi-arbitrage/defi/app.py
3. Please run app.py found in cefi-defi-arbitrage/arbitrage/app.py
4. Open your Chrome web browser and go to http://localhost:3002 to view the dashboard
5. Wait for a few seconds for the dashbaord to be updated with live prices, profits and arbitrage opportunities

# Unit Testing
Unit tests were written using the pytest library. There is a tests folder in each app. To run the unit tests, navigate to the project directory in 
the command line and type "pytest" followed by the path to the test file. An example is shown below to run the 
unit test from the cefi app: 

```
pytest cefi/tests/test_fetch_cefi_prices.py
```
