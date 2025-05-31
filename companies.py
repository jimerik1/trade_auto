# companies.py
# Define stock tickers to analyze

# S&P 500 Tech Leaders
TECH_LEADERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'ADBE', 'CRM'
]

# Financial Sector
FINANCIALS = [
    'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'AXP', 'BLK', 'SCHW', 'USB'
]

# Healthcare & Pharma
HEALTHCARE = [
    'JNJ', 'PFE', 'UNH', 'ABBV', 'TMO', 'ABT', 'LLY', 'BMY', 'MRK', 'AMGN'
]

# Consumer Discretionary
CONSUMER_DISC = [
    'AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'SBUX', 'LOW', 'TJX', 'BKNG', 'CMG'
]

# Energy Sector
ENERGY = [
    'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'MPC', 'PSX', 'VLO', 'KMI', 'OKE'
]

# Industrial Sector
INDUSTRIALS = [
    'BA', 'HON', 'UPS', 'CAT', 'MMM', 'GE', 'LMT', 'RTX', 'DE', 'UNP'
]

# Dividend Aristocrats (High Quality Dividend Stocks)
DIVIDEND_ARISTOCRATS = [
    'JNJ', 'PG', 'KO', 'PEP', 'WMT', 'MCD', 'MMM', 'CVX', 'XOM', 'IBM'
]

# Growth Stocks (Higher Beta/Volatility)
GROWTH_STOCKS = [
    'NVDA', 'AMD', 'TSLA', 'NFLX', 'AMZN', 'GOOGL', 'META', 'CRM', 'ADBE', 'PYPL'
]

# Value Stocks (Traditionally Undervalued)
VALUE_STOCKS = [
    'BRK-B', 'JPM', 'BAC', 'XOM', 'CVX', 'WFC', 'IBM', 'VZ', 'T', 'INTC'
]

# Small Cap Growth (Russell 2000 examples)
SMALL_CAP = [
    'ENPH', 'DXCM', 'ETSY', 'PENN', 'ROKU', 'ZM', 'PTON', 'CRWD', 'ZS', 'OKTA'
]

# International ADRs
INTERNATIONAL = [
    'ASML', 'TSM', 'NVO', 'TM', 'BABA', 'JD', 'NIO', 'PDD', 'BIDU', 'TCEHY'
]

# Mixed Portfolio (Recommended for beginners)
BALANCED_PORTFOLIO = [
    # Large Cap Tech
    'AAPL', 'MSFT', 'GOOGL', 'AMZN',
    # Financial
    'JPM', 'BAC',
    # Healthcare
    'JNJ', 'UNH',
    # Consumer
    'PG', 'KO',
    # Industrial
    'HON', 'CAT',
    # Energy
    'XOM', 'CVX',
    # Growth
    'NVDA', 'TSLA',
    # Value
    'BRK-B', 'WMT'
]

# Crypto/Blockchain Exposure
CRYPTO_ADJACENT = [
    'COIN', 'MSTR', 'SQ', 'PYPL', 'RIOT', 'MARA', 'HOOD', 'SOFI'
]

# ESG/Clean Energy
CLEAN_ENERGY = [
    'TSLA', 'ENPH', 'SEDG', 'FSLR', 'PLUG', 'BE', 'ICLN', 'NEE', 'DUK', 'SO'
]

# REITs (Real Estate)
REITS = [
    'SPG', 'PLD', 'AMT', 'CCI', 'EQIX', 'PSA', 'O', 'WELL', 'DLR', 'AVB'
]

# Oslo Stock Exchange (Norway) - Major Companies
OSLO_ENERGY = [
    'EQNR.OL',  # Equinor - Oil & Gas
    'AKRBP.OL',  # Aker BP - Oil & Gas
]

OSLO_SEAFOOD = [
    'MOWI.OL',  # Mowi - Salmon farming
    'SALM.OL',  # SalMar - Salmon farming
]

OSLO_INDUSTRIAL = [
    'YAR.OL',   # Yara International - Fertilizers
    'NHY.OL',   # Norsk Hydro - Aluminum
    'ORK.OL',   # Orkla - Consumer goods
]

OSLO_FINANCIALS = [
    'DNB.OL',   # DNB Bank - Banking
    'GJF.OL',   # Gjensidige Forsikring - Insurance
]

OSLO_TELECOM = [
    'TEL.OL',   # Telenor - Telecommunications
]

OSLO_ALL = OSLO_ENERGY + OSLO_SEAFOOD + OSLO_INDUSTRIAL + OSLO_FINANCIALS + OSLO_TELECOM

# Stockholm Stock Exchange (Sweden) - OMXS30 Companies
STOCKHOLM_INDUSTRIALS = [
    'VOLV-B.ST',    # Volvo - Trucks & buses
    'ABB.ST',       # ABB - Industrial technology
    'SAAB-B.ST',    # Saab - Defense & aerospace
    'GETI-B.ST',    # Getinge - Medical technology
    'ELUX-B.ST',    # Electrolux - Home appliances
    'NIBE-B.ST',    # NIBE - Heating solutions
]

STOCKHOLM_FINANCIALS = [
    'SEB-A.ST',     # SEB - Banking
    'SWED-A.ST',    # Swedbank - Banking
    'SHB-A.ST',     # Handelsbanken - Banking
    'NDA-SE.ST',    # Nordea - Banking
]

STOCKHOLM_HEALTHCARE = [
    'AZN.ST',       # AstraZeneca - Pharmaceuticals
    'ESSITY-B.ST',  # Essity - Hygiene products
]

STOCKHOLM_CONSUMER = [
    'HM-B.ST',      # H&M - Fashion retail
]

STOCKHOLM_TELECOM = [
    'ERIC-B.ST',    # Ericsson - Telecom equipment
    'TEL2-B.ST',    # Tele2 - Telecom services
    'TELIA.ST',     # Telia - Telecom services
    'SINCH.ST',     # Sinch - Communications tech
]

STOCKHOLM_MATERIALS = [
    'BOL.ST',       # Boliden - Mining
    'SCA-B.ST',     # SCA - Forest products
]

STOCKHOLM_GAMING = [
    'EVO.ST',       # Evolution - Online gaming
]

STOCKHOLM_REAL_ESTATE = [
    'CAST.ST',      # Castellum - Real estate
    'SBB-B.ST',     # SBB - Real estate
]

STOCKHOLM_ALL = (STOCKHOLM_INDUSTRIALS + STOCKHOLM_FINANCIALS + 
                 STOCKHOLM_HEALTHCARE + STOCKHOLM_CONSUMER + 
                 STOCKHOLM_TELECOM + STOCKHOLM_MATERIALS + 
                 STOCKHOLM_GAMING + STOCKHOLM_REAL_ESTATE)

# Combined Nordic Portfolio
NORDIC_PORTFOLIO = OSLO_ALL + STOCKHOLM_ALL

# Default ticker list - MODIFY THIS TO CHOOSE YOUR ANALYSIS SET
# Options: TECH_LEADERS, FINANCIALS, HEALTHCARE, CONSUMER_DISC, ENERGY, 
#          INDUSTRIALS, DIVIDEND_ARISTOCRATS, GROWTH_STOCKS, VALUE_STOCKS,
#          SMALL_CAP, INTERNATIONAL, BALANCED_PORTFOLIO, CRYPTO_ADJACENT,
#          CLEAN_ENERGY, REITS, OSLO_ALL, STOCKHOLM_ALL, NORDIC_PORTFOLIO,
#          OSLO_ENERGY, OSLO_SEAFOOD, STOCKHOLM_INDUSTRIALS, STOCKHOLM_FINANCIALS

TICKERS = BALANCED_PORTFOLIO  # Change this to any of the lists above

# Or create your own custom list:
# TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM', 'JNJ', 'XOM', 'BRK-B']

# For testing with a small set:
# TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM']

print(f"Selected {len(TICKERS)} tickers for analysis: {TICKERS}")