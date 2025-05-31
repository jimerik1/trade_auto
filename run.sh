#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run the main factor analysis system
# You can customize with different options:
# python main.py --list TECH_LEADERS
# python main.py --list NORDIC_PORTFOLIO
# python main.py --tickers AAPL MSFT GOOGL
# python main.py --config config.yaml

python3 main.py
#python3 main.py --weekly-signals