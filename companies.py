# companies.py
# Define stock tickers to analyze - Updated with 100+ Scandinavian companies

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

# =============================================================================
# SCANDINAVIAN STOCK EXCHANGES - COMPREHENSIVE LISTS (100+ COMPANIES)
# =============================================================================

# NORWAY - Oslo Stock Exchange (Euronext Oslo)
# =============================================================================

# OBX Index (Top 25 Norwegian Companies)
OSLO_OBX_INDEX = [
    'EQNR.OL',    # Equinor - Oil & Gas giant
    'DNB.OL',     # DNB Bank - Largest bank
    'MOWI.OL',    # Mowi - Salmon farming leader
    'TEL.OL',     # Telenor - Telecommunications
    'YAR.OL',     # Yara International - Fertilizers
    'NHY.OL',     # Norsk Hydro - Aluminum & renewable energy
    'AKRBP.OL',   # Aker BP - Oil & Gas
    'STB.OL',     # Storebrand - Insurance & asset management
    'SALM.OL',    # SalMar - Salmon farming
    'ORKLA.OL',   # Orkla - Consumer goods
    'GJF.OL',     # Gjensidige - Insurance
    'KOG.OL',     # Kongsberg Gruppen - Defense & maritime tech
    'REC.OL',     # REC Silicon - Solar grade silicon
    'MPCC.OL',    # MPC Container Ships - Shipping
    'BAKKA.OL',   # Bakkafrost - Salmon farming
    'SUBC.OL',    # Subsea 7 - Offshore engineering
    'LSG.OL',     # Leroy Seafood Group - Seafood
    'AEGA.OL',    # Aegon ASA - Insurance
    'ADEA.OL',    # Atlantic Sapphire - Land-based salmon farming
    'SCATC.OL',   # Scatec - Solar power
    'NEL.OL',     # Nel ASA - Hydrogen technology
    'PCIB.OL',    # PCI Biotech - Cancer treatment
    'KAHOT.OL',   # Kahoot - Educational technology
    'OTEC.OL',    # Otec - Technology
    'BOUVET.OL'   # Bouvet - IT consulting
]

# Norwegian Energy & Maritime
OSLO_ENERGY_MARITIME = [
    'EQNR.OL',    # Equinor
    'AKRBP.OL',   # Aker BP
    'OKEA.OL',    # OKEA ASA - Oil & gas
    'PGS.OL',     # Petroleum Geo-Services
    'SDRL.OL',    # Seadrill - Offshore drilling
    'BORR.OL',    # Borr Drilling
    'ARCHER.OL',  # Archer - Oilfield services
    'DNO.OL',     # DNO ASA - Oil & gas
    'NOSP.OL',    # North Sea Shipping
    'FLNG.OL',    # Flex LNG - LNG shipping
    'GOGL.OL',    # Golden Ocean Group - Dry bulk shipping
    'FRONTLINE.OL', # Frontline - Oil tankers
    'HAFNIA.OL',  # Hafnia - Product tankers
    'HAVI.OL',    # Havila Shipping - Offshore vessels
    'SOFF.OL',    # Scana Offshore - Maritime equipment
    'SUBSEA7.OL', # Subsea 7 - Offshore engineering
    'AKOFS.OL',   # Aker Offshore Wind
    'SCATEC.OL',  # Scatec - Solar power
    'NEL.OL',     # Nel ASA - Hydrogen
    'HEX.OL'      # Hexagon Composites - Pressure vessels
]

# Norwegian Seafood (World's largest seafood exporters)
OSLO_SEAFOOD_AQUACULTURE = [
    'MOWI.OL',    # Mowi - World's largest salmon farmer
    'SALM.OL',    # SalMar - Salmon farming
    'LSG.OL',     # Leroy Seafood Group
    'BAKKA.OL',   # Bakkafrost - Faroe Islands salmon
    'GRIEG.OL',   # Grieg Seafood - Salmon farming
    'NRS.OL',     # Norway Royal Salmon
    'AUSS.OL',    # Austevoll Seafood - Pelagic fishing
    'ADEA.OL',    # Atlantic Sapphire - Land-based farming
    'ICE.OL',     # ICE Fish Farm - Land-based salmon
    'NOVO.OL',    # Nova Sea - Salmon farming
    'SMLA.OL',    # Salmones Multiexport - Chilean operations
    'SSC.OL',     # Salmon Seafood Company
    'BEWI.OL',    # Bewi - EPS packaging for seafood
    'AKVA.OL',    # AKVA Group - Aquaculture technology
    'MASSON.OL'   # Masson - Aquaculture equipment
]

# Norwegian Tech & Industrials
OSLO_TECH_INDUSTRIALS = [
    'YAR.OL',     # Yara International - Fertilizers
    'NHY.OL',     # Norsk Hydro - Aluminum
    'KOG.OL',     # Kongsberg Gruppen - Defense tech
    'ORKLA.OL',   # Orkla - Consumer goods
    'TEL.OL',     # Telenor - Telecom
    'TGS.OL',     # TGS - Seismic data
    'KAHOT.OL',   # Kahoot - EdTech
    'OTEC.OL',    # Otec - Technology
    'BOUVET.OL',  # Bouvet - IT consulting
    'CRAYON.OL',  # Crayon Group - Software & cloud services
    'THIN.OL',    # Thin Film Electronics - Printed electronics
    'NAPA.OL',    # Napatech - Network analytics
    'OPERA.OL',   # Opera Software - Web browser
    'Q30.OL',     # Q30 - Software solutions
    'NEXT.OL',    # Next Biometrics - Fingerprint sensors
    'ZWIPE.OL',   # Zwipe - Biometric payment cards
    'IDEX.OL',    # IDEX Biometrics - Fingerprint sensors
    'AKER.OL',    # Aker ASA - Industrial investment
    'AMSC.OL',    # American Superconductor Norge
    'PROT.OL'     # Protector Forsikring - Insurance tech
]

# Norwegian Financial Services
OSLO_FINANCIALS = [
    'DNB.OL',     # DNB Bank - Largest bank
    'STB.OL',     # Storebrand - Insurance
    'GJF.OL',     # Gjensidige - Insurance
    'SPOG.OL',    # SpareBank 1 Østlandet - Regional bank
    'HELG.OL',    # Helgeland Sparebank
    'TOTG.OL',    # Totens Sparebank
    'MING.OL',    # SpareBank 1 Ringerike Hadeland
    'PARB.OL',    # Pareto Bank
    'SADG.OL',    # Sbanken - Digital bank
    'PROT.OL',    # Protector Forsikring
    'GOODING.OL', # Goodtech - Financial tech
    'AEGA.OL'     # Aegon Asset Management
]

# All Oslo Stock Exchange companies
OSLO_ALL = (OSLO_OBX_INDEX + OSLO_ENERGY_MARITIME + OSLO_SEAFOOD_AQUACULTURE + 
           OSLO_TECH_INDUSTRIALS + OSLO_FINANCIALS)

# Remove duplicates while preserving order
OSLO_ALL = list(dict.fromkeys(OSLO_ALL))

# SWEDEN - Stockholm Stock Exchange (Nasdaq Stockholm)
# =============================================================================

# OMXS30 Index (Top 30 Swedish Companies) - Updated 2025
STOCKHOLM_OMXS30 = [
    'AZN.ST',     # AstraZeneca - Pharmaceuticals (largest by market cap)
    'ABB.ST',     # ABB - Industrial technology
    'INVE_B.ST',  # Investor AB - Investment company
    'ATCO_B.ST',  # Atlas Copco B - Industrial equipment
    'ATCO_A.ST',  # Atlas Copco A - Industrial equipment
    'VOLV_B.ST',  # Volvo B - Commercial vehicles
    'NDA_SE.ST',  # Nordea Bank - Banking
    'SEB_A.ST',   # SEB - Banking
    'ASSA_B.ST',  # Assa Abloy B - Lock systems
    'SWED_A.ST',  # Swedbank A - Banking
    'ERIC_B.ST',  # Ericsson B - Telecom equipment
    'SAND.ST',    # Sandvik - Mining & construction
    'HEXA_B.ST',  # Hexagon B - Measurement technology
    'SAAB_B.ST',  # Saab B - Defense & aerospace
    'SHB_A.ST',   # Handelsbanken A - Banking
    'HM_B.ST',    # H&M B - Fashion retail
    'ESSITY_B.ST', # Essity B - Hygiene products
    'ALFA.ST',    # Alfa Laval - Heat transfer equipment
    'TELIA.ST',   # Telia Company - Telecommunications
    'EVO.ST',     # Evolution - Online gaming
    'TEL2_B.ST',  # Tele2 B - Telecommunications
    'SKF_B.ST',   # SKF B - Bearings & seals
    'SCA_B.ST',   # SCA B - Forest products
    'BOL.ST',     # Boliden - Mining
    'NIBE_B.ST',  # NIBE B - Climate solutions
    'GETI_B.ST',  # Getinge B - Medical technology
    'KINV_B.ST',  # Kinnevik B - Investment company
    'SINCH.ST',   # Sinch - Communications platform
    'ELUX_B.ST',  # Electrolux B - Home appliances
    'SBB_B.ST'    # SBB B - Real estate
]

# Swedish Industrials & Manufacturing (Global Leaders)
STOCKHOLM_INDUSTRIALS_EXTENDED = [
    'ABB.ST',     # ABB - Industrial automation
    'ATCO_A.ST',  # Atlas Copco A
    'ATCO_B.ST',  # Atlas Copco B
    'VOLV_B.ST',  # Volvo trucks & buses
    'VOLV_A.ST',  # Volvo A shares
    'SAND.ST',    # Sandvik - Mining equipment
    'SKF_A.ST',   # SKF A - Bearings
    'SKF_B.ST',   # SKF B - Bearings
    'SAAB_B.ST',  # Saab - Defense
    'ALFA.ST',    # Alfa Laval - Heat exchangers
    'GETI_B.ST',  # Getinge - Medical equipment
    'HUSQ_B.ST',  # Husqvarna B - Outdoor power products
    'HUSQ_A.ST',  # Husqvarna A
    'ELUX_B.ST',  # Electrolux B - Home appliances
    'ELUX_A.ST',  # Electrolux A
    'ASSA_B.ST',  # Assa Abloy B - Access solutions
    'NIBE_B.ST',  # NIBE B - Heat pumps
    'FAGC.ST',    # Fagerhult - Lighting solutions
    'SWED_A.ST',  # Swedbank
    'KONE.ST',    # KONE - Elevators (Finnish but listed)
    'SECU_B.ST',  # Securitas B - Security services
    'TREL_B.ST',  # Trelleborg B - Polymer solutions
    'WALL_B.ST',  # Wallenstam B - Real estate
    'PEAB_B.ST',  # PEAB B - Construction
    'SKANSKA_B.ST', # Skanska B - Construction
    'NCC_B.ST'    # NCC B - Construction
]

# Swedish Tech & Communications
STOCKHOLM_TECH_TELECOM = [
    'ERIC_B.ST',  # Ericsson B - 5G leader
    'ERIC_A.ST',  # Ericsson A
    'TELIA.ST',   # Telia - Telecom operator
    'TEL2_B.ST',  # Tele2 B - Mobile operator
    'TEL2_A.ST',  # Tele2 A
    'SINCH.ST',   # Sinch - Cloud communications
    'HEXA_B.ST',  # Hexagon B - Digital solutions
    'HEXA_A.ST',  # Hexagon A
    'ADDTECH_B.ST', # Addtech B - Industrial technology
    'ICA.ST',     # ICA Gruppen - Retail tech
    'TOBII.ST',   # Tobii - Eye tracking technology
    'NEXAM.ST',   # Nexam Chemical - Advanced materials
    'MYCRONIC.ST', # Mycronic - Electronics production
    'BURE.ST',    # Bure Equity - Tech investments
    'ENEA.ST',    # Enea - Software solutions
    'NETU_B.ST',  # NetInsight - Media networks
    'MICRO.ST',   # Micronic Mydata - PCB production
    'NOTE.ST',    # Note - Electronics manufacturing
    'CLAVISTER.ST', # Clavister - Cybersecurity
    'ONECALL.ST'  # Onecall Group - Telecom services
]

# Swedish Gaming & Entertainment
STOCKHOLM_GAMING = [
    'EVO.ST',     # Evolution - Live casino gaming
    'KINV_B.ST',  # Kinnevik B - Investments in gaming/media
    'MTG_B.ST',   # MTG B - Gaming & esports
    'NENT_B.ST',  # NENT Group B - Entertainment
    'BETSSON_B.ST', # Betsson B - Online gaming
    'LGR.ST',     # Lundin Gold - Gaming investments
    'CHERRY.ST',  # Cherry - Gaming entertainment
    'GGBET.ST',   # Gaming innovation Group
    'STILLFRONT.ST', # Stillfront Group - Mobile gaming
    'G5EN.ST'     # G5 Entertainment - Mobile games
]

# Swedish Healthcare & Life Sciences
STOCKHOLM_HEALTHCARE = [
    'AZN.ST',     # AstraZeneca - Global pharma leader
    'ESSITY_B.ST', # Essity B - Hygiene & health
    'ESSITY_A.ST', # Essity A
    'GETI_B.ST',  # Getinge B - Medical technology
    'GETI_A.ST',  # Getinge A
    'ELEKTA_B.ST', # Elekta B - Cancer care solutions
    'SWMA.ST',    # Swedish Match - Tobacco/nicotine
    'CAMB.ST',    # Cambrex - Pharmaceutical services
    'MEKO.ST',    # Mekonomen Group - Healthcare retail
    'OATLY.ST',   # Oatly Group - Plant-based foods
    'CELLINK.ST', # CELLINK - Bioprinting
    'XVIVO.ST',   # XVIVO Perfusion - Organ preservation
    'GENO.ST',    # Genovis - Glycan analysis tools
    'CALLIDITAS.ST', # Calliditas Therapeutics
    'SPRINT.ST'   # Sprint Bioscience - Drug discovery
]

# Swedish Financial Services
STOCKHOLM_FINANCIALS = [
    'SEB_A.ST',   # SEB A - Skandinaviska Enskilda Banken
    'SEB_C.ST',   # SEB C
    'SWED_A.ST',  # Swedbank A
    'SHB_A.ST',   # Handelsbanken A
    'SHB_B.ST',   # Handelsbanken B
    'NDA_SE.ST',  # Nordea Bank
    'INVE_B.ST',  # Investor AB B - Investment company
    'INVE_A.ST',  # Investor AB A
    'KINV_B.ST',  # Kinnevik B - Investment company
    'KINV_A.ST',  # Kinnevik A
    'BURE.ST',    # Bure Equity AB
    'CRED_A.ST',  # Creditsafe - Credit information
    'LATO_B.ST',  # Latour B - Investment company
    'LUNDBERGB.ST', # L E Lundbergföretagen B
    'RROS.ST',    # Rörvik Timber - Forest investments
    'ORES.ST'     # Öresund - Investment company
]

# Swedish Consumer & Retail
STOCKHOLM_CONSUMER = [
    'HM_B.ST',    # H&M B - Fashion retail giant
    'HM_A.ST',    # H&M A
    'ICA.ST',     # ICA Gruppen - Retail & real estate
    'AXFO.ST',    # Axfood - Food retail
    'CLAS_B.ST',  # Clas Ohlson B - Hardware retail
    'JM.ST',      # JM AB - Residential development
    'HUSQ_B.ST',  # Husqvarna B - Outdoor products
    'OATLY.ST',   # Oatly - Plant-based drinks
    'AAK.ST',     # AAK AB - Specialty oils & fats
    'ARJO_B.ST',  # Arjo B - Medical devices
    'DUNI.ST',    # Duni Group - Table-top products
    'BEIJER_B.ST', # Beijer Ref B - Climate solutions
    'ELUX_B.ST',  # Electrolux B - Home appliances
    'MEKO.ST',    # Mekonomen - Automotive aftermarket
    'INWI.ST'     # Inwido - Windows & doors
]

# All Stockholm Stock Exchange companies
STOCKHOLM_ALL = (STOCKHOLM_OMXS30 + STOCKHOLM_INDUSTRIALS_EXTENDED + 
                STOCKHOLM_TECH_TELECOM + STOCKHOLM_GAMING + 
                STOCKHOLM_HEALTHCARE + STOCKHOLM_FINANCIALS + 
                STOCKHOLM_CONSUMER)

# Remove duplicates while preserving order
STOCKHOLM_ALL = list(dict.fromkeys(STOCKHOLM_ALL))

# DENMARK - Copenhagen Stock Exchange (Nasdaq Copenhagen)
# =============================================================================

# OMXC25 Index (Top 25 Danish Companies) - Updated 2025
COPENHAGEN_OMXC25 = [
    'NOVO-B.CO',  # Novo Nordisk B - Diabetes care leader
    'ASML.AS',    # ASML (Dutch but major Nordic holding)
    'MAERSK-B.CO', # A.P. Møller-Mærsk B - Shipping & logistics
    'MAERSK-A.CO', # A.P. Møller-Mærsk A
    'ORSTED.CO',  # Ørsted - Offshore wind leader
    'DSV.CO',     # DSV - Transport & logistics
    'CARLB.CO',   # Carlsberg B - Brewing
    'DANSKE.CO',  # Danske Bank - Banking
    'PNDORA.CO',  # Pandora - Jewelry
    'NZYM-B.CO',  # Novozymes B - Industrial enzymes
    'COLB.CO',    # Coloplast B - Medical devices
    'COLO-B.CO',  # Coloplast B (alternative ticker)
    'VWS.CO',     # Vestas Wind Systems - Wind turbines
    'TRYG.CO',    # Tryg - Insurance
    'GMAB.CO',    # Genmab - Biotechnology
    'AMBU-B.CO',  # Ambu B - Medical devices
    'ROCK-B.CO',  # Rockwool B - Insulation
    'FLS.CO',     # FLSmidth - Engineering
    'JYSK.CO',    # Jyske Bank - Banking
    'RLIB.CO',    # Ringkjøbing Landbobank
    'PAAL-B.CO',  # Per Aarsleff B - Construction
    'BACTI.CO',   # Bavarian Nordic - Vaccines
    'SIM.CO',     # SimCorp - Investment management software
    'NETC.CO',    # Netcompany Group - IT services
    'ZEAL.CO'     # Zealand Pharma - Biotechnology
]

# Danish Healthcare & Biotech (World leaders)
COPENHAGEN_HEALTHCARE = [
    'NOVO-B.CO',  # Novo Nordisk B - Global diabetes leader
    'NOVO-A.CO',  # Novo Nordisk A
    'NZYM-B.CO',  # Novozymes B - Enzymes & biosolutions
    'NZYM-A.CO',  # Novozymes A
    'COLB.CO',    # Coloplast B - Ostomy & wound care
    'COLO-A.CO',  # Coloplast A
    'GMAB.CO',    # Genmab - Cancer immunotherapy
    'AMBU-B.CO',  # Ambu B - Medical devices
    'AMBU-A.CO',  # Ambu A
    'BACTI.CO',   # Bavarian Nordic - Vaccines
    'ZEAL.CO',    # Zealand Pharma - Peptide drugs
    'PHAR.CO',    # Pharma Equity Group
    'SUBC.CO',    # Subcuvia - Immunotherapy
    'ALMB.CO',    # ALM Brand - Health insurance
    'ORPHAN.CO',  # Orphan Reach - Rare diseases
    'BAVA.CO',    # Bavarian Nordic
    'LUNDBECK.CO', # H. Lundbeck - CNS pharmaceuticals
    'LEO-B.CO',   # LEO Pharma - Dermatology
    'WILLIAM.CO', # William Demant - Hearing aids
    'ZEALAND.CO'  # Zealand Pharma
]

# Danish Energy & Industrials
COPENHAGEN_ENERGY_INDUSTRIALS = [
    'ORSTED.CO',  # Ørsted - Global offshore wind leader
    'VWS.CO',     # Vestas Wind Systems - Wind turbines
    'MAERSK-A.CO', # A.P. Møller-Mærsk A - Shipping
    'MAERSK-B.CO', # A.P. Møller-Mærsk B
    'DSV.CO',     # DSV - Logistics
    'FLS.CO',     # FLSmidth - Cement & mining
    'ROCK-A.CO',  # Rockwool A - Insulation
    'ROCK-B.CO',  # Rockwool B
    'DFDS.CO',    # DFDS - Ferry & logistics services
    'DKSH.CO',    # DKSH - Market expansion services
    'PAAL-B.CO',  # Per Aarsleff B - Construction
    'MONT-B.CO',  # Monberg & Thorsen - Project development
    'NKT.CO',     # NKT - Power cables
    'KGHM.CO',    # Copper mining operations
    'COOL.CO',    # Copenhagen Infrastructure Partners
    'GREEN.CO',   # Green Investment Group
    'EUROPE.CO',  # European Energy
    'BETTER.CO',  # Better Energy - Solar development
    'SOLAR-B.CO', # Solar A/S - Installation services
    'DANFOSS.CO'  # Danfoss - Engineering solutions
]

# Danish Financial Services
COPENHAGEN_FINANCIALS = [
    'DANSKE.CO',  # Danske Bank - Largest bank
    'JYSK.CO',    # Jyske Bank
    'RLIB.CO',    # Ringkjøbing Landbobank
    'TRYG.CO',    # Tryg - Insurance
    'TOPDANMARK.CO', # Topdanmark - Insurance
    'SPAR.CO',    # Spar Nord Bank
    'ALMB.CO',    # ALM Brand - Insurance
    'PNDINV.CO',  # Pandion Investment Management
    'HARBOES.CO', # Harboes Brewery - Regional investment
    'CPHCAP.CO',  # Copenhagen Capital
    'RLIF.CO',    # Realkredit Danmark
    'BRF.CO',     # BRFkredit - Mortgage credit
    'NORDF.CO',   # Nordea Finance
    'INVEST.CO',  # Investment banking services
    'LOAN.CO'     # Alternative lending
]

# Danish Consumer & Retail
COPENHAGEN_CONSUMER = [
    'CARLB.CO',   # Carlsberg B - Global brewing
    'CARLA.CO',   # Carlsberg A
    'PNDORA.CO',  # Pandora - Jewelry & accessories
    'BESTSELLER.CO', # Bestseller - Fashion retail
    'ONLY.CO',    # Only - Fashion brand
    'JACK.CO',    # Jack & Jones - Fashion
    'LEGO.CO',    # LEGO Group (private but major Danish brand)
    'ECCO.CO',    # ECCO - Footwear
    'BANG.CO',    # Bang & Olufsen - Audio equipment
    'ROYAL.CO',   # Royal Copenhagen - Porcelain
    'GEORG.CO',   # Georg Jensen - Silver & jewelry
    'ARLA.CO',    # Arla Foods - Dairy
    'DANISH.CO',  # Danish Crown - Meat processing
    'HARBOES.CO', # Harboes Brewery
    'TIVOLI.CO',  # Tivoli - Entertainment
    'ISS.CO',     # ISS - Facility services
    'CPHAIR.CO',  # Copenhagen Airports
    'TDC.CO',     # TDC NET - Telecommunications
    'NORDIC.CO',  # Nordic Entertainment Group
    'SALLING.CO'  # Salling Group - Retail
]

# Danish Technology
COPENHAGEN_TECHNOLOGY = [
    'SIM.CO',     # SimCorp - Investment software
    'NETC.CO',    # Netcompany Group - IT consulting
    'SCAPE.CO',   # Scape Technologies
    'UNITY.CO',   # Unity Technologies (gaming engine)
    'SHAPE.CO',   # Shape Robotics - Educational robotics
    'TRACK.CO',   # Track Hospitality Software
    'IMPACT.CO',  # Impact - Partnership automation
    'TEMPLAFY.CO', # Templafy - Document automation
    'BLACKWOOD.CO', # Blackwood Seven - Digital transformation
    'ZIGG.CO',    # Zigg Capital - Fintech investments
    'TDC.CO',     # TDC NET - Telecom infrastructure
    'ADFORM.CO',  # Adform - AdTech platform
    'SITECORE.CO', # Sitecore - Digital experience platform
    'FALCON.CO',  # Falcon.io - Social media management
    'ZENDESK.CO'  # Zendesk (has major Copenhagen operations)
]

# All Copenhagen Stock Exchange companies
COPENHAGEN_ALL = (COPENHAGEN_OMXC25 + COPENHAGEN_HEALTHCARE + 
                 COPENHAGEN_ENERGY_INDUSTRIALS + COPENHAGEN_FINANCIALS + 
                 COPENHAGEN_CONSUMER + COPENHAGEN_TECHNOLOGY)

# Remove duplicates while preserving order
COPENHAGEN_ALL = list(dict.fromkeys(COPENHAGEN_ALL))

# FINLAND - Helsinki Stock Exchange (Nasdaq Helsinki)
# =============================================================================

# Finnish Technology & Telecom
HELSINKI_TECH = [
    'NOKIA.HE',   # Nokia - 5G & network infrastructure
    'NORDEA.HE',  # Nordea Bank
    'FORTUM.HE',  # Fortum - Clean energy
    'NESTE.HE',   # Neste - Renewable diesel
    'UPM.HE',     # UPM-Kymmene - Forest industry
    'STORA.HE',   # Stora Enso - Sustainable materials
    'WARTSILA.HE', # Wärtsilä - Marine & energy
    'METSO.HE',   # Metso Outotec - Minerals processing
    'KONE.HE',    # KONE - Elevators & escalators
    'TVO.HE',     # Teollisuuden Voima - Nuclear power
    'ELISA.HE',   # Elisa - Telecommunications
    'TELIA.HE',   # Telia (operates in Finland)
    'QT.HE',      # Qt Group - Software development platform
    'SSH.HE',     # SSH Communications Security
    'TECN.HE',    # Tecnotree - Telecom software
    'ETTEPLAN.HE', # Etteplan - Engineering services
    'DIGIA.HE',   # Digia - Software services
    'BASWARE.HE', # Basware - Purchase-to-pay solutions
    'ROVIO.HE',   # Rovio Entertainment - Mobile games
    'REMEDY.HE'   # Remedy Entertainment - Video games
]

# Finnish Industrials
HELSINKI_INDUSTRIALS = [
    'WARTSILA.HE', # Wärtsilä - Marine power
    'METSO.HE',   # Metso Outotec - Mining equipment
    'KONE.HE',    # KONE - Elevators
    'RAUTE.HE',   # Raute - Wood processing machinery
    'CARGOTEC.HE', # Cargotec - Cargo handling
    'PONSSE.HE',  # Ponsse - Forest machines
    'VALMET.HE',  # Valmet - Pulp & paper machinery
    'ORION.HE',   # Orion Corporation - Pharmaceuticals
    'HUHTAMAKI.HE', # Huhtamäki - Packaging solutions
    'FISKARS.HE', # Fiskars Group - Consumer goods
    'RAPALA.HE',  # Rapala VMC - Fishing tackle
    'SCANFIL.HE', # Scanfil - Electronics manufacturing
    'PKC.HE',     # PKC Group - Wiring systems
    'GLASTON.HE', # Glaston - Glass processing
    'ATRIA.HE',   # Atria - Food processing
    'RAISIO.HE',  # Raisio - Food & nutrition
    'KEMIRA.HE',  # Kemira - Water treatment chemicals
    'OUTOKUMPU.HE', # Outokumpu - Stainless steel
    'SSAB.HE',    # SSAB - Steel
    'RUUKKI.HE'   # Ruukki Construction - Building solutions
]

# All Helsinki companies
HELSINKI_ALL = HELSINKI_TECH + HELSINKI_INDUSTRIALS

# Remove duplicates
HELSINKI_ALL = list(dict.fromkeys(HELSINKI_ALL))

# =============================================================================
# COMPREHENSIVE SCANDINAVIAN PORTFOLIOS
# =============================================================================

# Top 50 Scandinavian Blue Chips (Market Leaders)
SCANDINAVIAN_BLUE_CHIPS = [
    # Norwegian Leaders
    'EQNR.OL', 'DNB.OL', 'MOWI.OL', 'TEL.OL', 'YAR.OL',
    # Swedish Leaders  
    'AZN.ST', 'ABB.ST', 'VOLV_B.ST', 'ERIC_B.ST', 'HEXA_B.ST',
    # Danish Leaders
    'NOVO-B.CO', 'MAERSK-B.CO', 'ORSTED.CO', 'DSV.CO', 'CARLB.CO',
    # Finnish Leaders
    'NOKIA.HE', 'NESTE.HE', 'UPM.HE', 'KONE.HE', 'FORTUM.HE',
    # Additional Nordic Champions
    'NHY.OL', 'SALM.OL', 'INVE_B.ST', 'SEB_A.ST', 'VWS.CO',
    'GMAB.CO', 'COLB.CO', 'TELIA.ST', 'SAND.ST', 'ASSA_B.ST',
    'HM_B.ST', 'EVO.ST', 'DANSKE.CO', 'TRYG.CO', 'WARTSILA.HE',
    'KOG.OL', 'SAAB_B.ST', 'ESSITY_B.ST', 'PNDORA.CO', 'METSO.HE',
    'AKRBP.OL', 'SKF_B.ST', 'NZYM-B.CO', 'ELISA.HE', 'STB.OL',
    'BOL.ST', 'NIBE_B.ST', 'FLS.CO', 'HUHTAMAKI.HE', 'ORKLA.OL'
]

# ESG & Clean Energy Leaders (Scandinavian Green Champions)
SCANDINAVIAN_ESG_LEADERS = [
    'ORSTED.CO',   # World's largest offshore wind developer
    'VWS.CO',      # Global wind turbine leader
    'NESTE.HE',    # Renewable diesel pioneer
    'EQNR.OL',     # Transitioning oil major with renewables
    'SCATEC.OL',   # Solar power developer
    'NEL.OL',      # Hydrogen technology
    'FORTUM.HE',   # Clean energy & nuclear
    'UPM.HE',      # Sustainable forest products
    'STORA.HE',    # Sustainable materials
    'ESSITY_B.ST', # Hygiene & health solutions
    'NIBE_B.ST',   # Heat pumps & climate solutions
    'ROCK-B.CO',   # Sustainable insulation
    'NOVO-B.CO',   # Healthcare innovation
    'MOWI.OL',     # Sustainable seafood
    'YARA.OL',     # Green ammonia & fertilizers
    'ALFA.ST',     # Energy-efficient heat exchangers
    'ABB.ST',      # Electrification & automation
    'HEXA_B.ST',   # Smart manufacturing solutions
    'GETI_B.ST',   # Healthcare technology
    'AKVA.OL'      # Sustainable aquaculture technology
]

# Technology & Innovation Portfolio
SCANDINAVIAN_TECH_INNOVATION = [
    'NOKIA.HE',    # 5G & network technology
    'ERIC_B.ST',   # Telecom equipment leader
    'SINCH.ST',    # Cloud communications
    'KAHOT.OL',    # Educational technology
    'EVO.ST',      # Live casino technology
    'HEXA_B.ST',   # Measurement & digital solutions
    'QT.HE',       # Software development platform
    'NETC.CO',     # IT consulting
    'SIM.CO',      # Investment management software
    'BOUVET.OL',   # IT consulting
    'OPERA.OL',    # Web browser technology
    'TOBII.ST',    # Eye tracking technology
    'UNITY.CO',    # Game development platform
    'ROVIO.HE',    # Mobile gaming
    'STILLFRONT.ST', # Mobile gaming
    'CLAVISTER.ST', # Cybersecurity
    'SSH.HE',      # Security software
    'THIN.OL',     # Printed electronics
    'NEXT.OL',     # Biometric sensors
    'SHAPE.CO'     # Educational robotics
]

# Defensive Income Portfolio (High dividend yields & stability)
SCANDINAVIAN_DIVIDEND_STOCKS = [
    'TEL.OL',      # Telenor - Stable telecom dividends
    'TELIA.ST',    # Telia - Nordic telecom operator
    'HM_B.ST',     # H&M - Retail dividends
    'SEB_A.ST',    # SEB - Banking dividends
    'DNB.OL',      # DNB - Norwegian banking
    'DANSKE.CO',   # Danske Bank - Danish banking
    'VOLV_B.ST',   # Volvo - Industrial dividends
    'ABB.ST',      # ABB - Technology dividends
    'SAND.ST',     # Sandvik - Mining equipment
    'SKF_B.ST',    # SKF - Industrial dividends
    'CARLB.CO',    # Carlsberg - Brewery dividends
    'MOWI.OL',     # Mowi - Seafood dividends
    'ORKLA.OL',    # Orkla - Consumer goods
    'ESSITY_B.ST', # Essity - Hygiene products
    'COLB.CO',     # Coloplast - Medical devices
    'UPM.HE',      # UPM - Forest industry
    'FORTUM.HE',   # Fortum - Energy utilities
    'TRYG.CO',     # Tryg - Insurance
    'GJF.OL',      # Gjensidige - Insurance
    'INVE_B.ST'    # Investor AB - Investment company
]

# Growth & Small Cap Portfolio
SCANDINAVIAN_GROWTH_STOCKS = [
    'NOVO-B.CO',   # Novo Nordisk - Diabetes care growth
    'GMAB.CO',     # Genmab - Biotech growth
    'ORSTED.CO',   # Ørsted - Green energy growth
    'NESTE.HE',    # Neste - Renewable fuels
    'EVO.ST',      # Evolution - Gaming growth
    'SINCH.ST',    # Sinch - Communications growth
    'KAHOT.OL',    # Kahoot - EdTech growth
    'NEL.OL',      # Nel - Hydrogen growth
    'SCATEC.OL',   # Scatec - Solar growth
    'ZEAL.CO',     # Zealand Pharma - Biotech
    'CELLINK.ST',  # CELLINK - Bioprinting
    'XVIVO.ST',    # XVIVO - Organ preservation
    'STILLFRONT.ST', # Stillfront - Mobile gaming
    'QT.HE',       # Qt Group - Software platform
    'NETC.CO',     # Netcompany - IT services
    'ADEA.OL',     # Atlantic Sapphire - Land-based aquaculture
    'OPERA.OL',    # Opera Software - Browser tech
    'TOBII.ST',    # Tobii - Eye tracking
    'BACTI.CO',    # Bavarian Nordic - Vaccines
    'REMEDY.HE'    # Remedy Entertainment - Gaming
]

# Combined All Scandinavian Companies (100+ unique companies)
SCANDINAVIAN_ALL = (OSLO_ALL + STOCKHOLM_ALL + COPENHAGEN_ALL + HELSINKI_ALL)

# Remove duplicates while preserving order
SCANDINAVIAN_ALL = list(dict.fromkeys(SCANDINAVIAN_ALL))

# =============================================================================
# PORTFOLIO SELECTIONS
# =============================================================================

# Default ticker list - MODIFY THIS TO CHOOSE YOUR ANALYSIS SET
TICKERS = SCANDINAVIAN_BLUE_CHIPS  # Change this to any of the lists above

# Alternative portfolio options:
# TICKERS = SCANDINAVIAN_ALL              # All 100+ companies
# TICKERS = SCANDINAVIAN_ESG_LEADERS      # Green/sustainable focus
# TICKERS = SCANDINAVIAN_TECH_INNOVATION  # Technology focus
# TICKERS = SCANDINAVIAN_DIVIDEND_STOCKS  # Income focus
# TICKERS = SCANDINAVIAN_GROWTH_STOCKS    # Growth focus
# TICKERS = OSLO_ALL                      # Norway only
# TICKERS = STOCKHOLM_ALL                 # Sweden only  
# TICKERS = COPENHAGEN_ALL                # Denmark only
# TICKERS = HELSINKI_ALL                  # Finland only
# TICKERS = BALANCED_PORTFOLIO            # Original US portfolio

# Print selected portfolio info
print(f"Selected portfolio: {len(TICKERS)} companies")
print(f"Tickers: {TICKERS[:10]}..." if len(TICKERS) > 10 else f"Tickers: {TICKERS}")

# Portfolio statistics
if TICKERS == SCANDINAVIAN_ALL:
    norway_count = len([t for t in TICKERS if t.endswith('.OL')])
    sweden_count = len([t for t in TICKERS if t.endswith('.ST')])
    denmark_count = len([t for t in TICKERS if t.endswith('.CO')])
    finland_count = len([t for t in TICKERS if t.endswith('.HE')])
    
    print(f"\nPortfolio breakdown:")
    print(f"Norway (Oslo): {norway_count} companies")
    print(f"Sweden (Stockholm): {sweden_count} companies") 
    print(f"Denmark (Copenhagen): {denmark_count} companies")
    print(f"Finland (Helsinki): {finland_count} companies")
    print(f"Total: {len(TICKERS)} companies")
    
print(f"\nTo change portfolio, modify the TICKERS variable in companies.py")
print(f"Available options: SCANDINAVIAN_ALL, SCANDINAVIAN_BLUE_CHIPS, SCANDINAVIAN_ESG_LEADERS, etc.")