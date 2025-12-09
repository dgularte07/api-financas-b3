#!/usr/bin/env python3
import json
import random
import os
import sys
from datetime import datetime, timedelta

# Garante encoding UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def get_variation(base_price, volatility=0.02):
    """Gera uma variação aleatória no preço para simular o mercado."""
    change = random.uniform(-volatility, volatility)
    return round(base_price * (1 + change), 2)

def generate_history(current_price):
    """Gera histórico simulado para gráficos de 1D, 7D, 30D, 6M, 1A, 5A."""
    history = {}
    periods = [
        ('1D', 24, 0.005),
        ('7D', 7, 0.015),
        ('30D', 30, 0.03),
        ('6M', 6, 0.08),
        ('1A', 12, 0.12),
        ('5A', 5, 0.25)
    ]
    
    for period_name, points, vol in periods:
        prices = []
        temp_price = current_price
        for _ in range(points):
            prices.insert(0, round(temp_price, 2))
            change = random.uniform(-vol, vol)
            temp_price = temp_price / (1 + change)
        history[period_name] = prices
        
    return history

def generate_indicators(type_):
    """Gera indicadores fundamentalistas realistas baseados no tipo do ativo."""
    indicators = {}
    
    if type_ in ['ACAO', 'STOCK', 'BDR']:
        indicators = {
            "pl": round(random.uniform(4, 40), 1),
            "p_vp": round(random.uniform(0.5, 5.0), 2),
            "dy": round(random.uniform(0, 15), 2),
            "roe": round(random.uniform(5, 35), 1),
            "margem_liquida": round(random.uniform(5, 40), 1),
            "divida_liquida_ebitda": round(random.uniform(-1, 4), 1),
            "cagr_lucros_5y": round(random.uniform(0, 20), 1)
        }
    elif type_ in ['FII', 'REIT']:
        indicators = {
            "p_vp": round(random.uniform(0.8, 1.2), 2) if type_ == 'FII' else None,
            "p_ffo": round(random.uniform(10, 25), 1) if type_ == 'REIT' else None,
            "dy_12m": round(random.uniform(6, 14), 2),
            "dy_annual": round(random.uniform(3, 8), 2) if type_ == 'REIT' else None,
            "vacancia_fisica": round(random.uniform(0, 15), 1),
            "liquidez_diaria": round(random.uniform(100000, 10000000), 0)
        }
    elif type_ in ['CRIPTO']:
        indicators = {
            "market_cap_bilhoes": round(random.uniform(1, 1500), 1),
            "vol_24h_bilhoes": round(random.uniform(0.1, 50), 1),
            "hashrate": "N/A"
        }
    elif 'ETF' in type_:
        indicators = {
            "taxa_adm": round(random.uniform(0.03, 0.75), 2),
            "aum_bilhoes": round(random.uniform(0.5, 500), 1),
            "sharpe_ratio": round(random.uniform(0.5, 2.0), 2)
        }
        
    return {k: v for k, v in indicators.items() if v is not None}

def main():
    print("Iniciando geração MASSIVA de dados (B3 Completa + FIIs)...")

    # ==========================================
    # 1. LISTA MASSIVA DE ATIVOS (Cotação Base Aproximada)
    # ==========================================
    raw_assets = [
        # --- AÇÕES BRASIL (IBOVESPA + IDIV + SMLL) ---
        ("VALE3", "Vale", "ACAO", 68.00, "BRL"), ("PETR4", "Petrobras PN", "ACAO", 36.50, "BRL"),
        ("PETR3", "Petrobras ON", "ACAO", 38.20, "BRL"), ("ITUB4", "Itaú Unibanco", "ACAO", 33.20, "BRL"),
        ("BBDC4", "Bradesco PN", "ACAO", 14.50, "BRL"), ("BBDC3", "Bradesco ON", "ACAO", 12.80, "BRL"),
        ("BBAS3", "Banco do Brasil", "ACAO", 27.80, "BRL"), ("WEGE3", "Weg", "ACAO", 40.50, "BRL"),
        ("ABEV3", "Ambev", "ACAO", 12.80, "BRL"), ("MGLU3", "Magalu", "ACAO", 2.10, "BRL"),
        ("VIIA3", "Casas Bahia", "ACAO", 0.60, "BRL"), ("JBSS3", "JBS", "ACAO", 22.50, "BRL"),
        ("SUZB3", "Suzano", "ACAO", 55.40, "BRL"), ("GGBR4", "Gerdau", "ACAO", 21.30, "BRL"),
        ("RENT3", "Localiza", "ACAO", 52.10, "BRL"), ("LREN3", "Lojas Renner", "ACAO", 16.40, "BRL"),
        ("PRIO3", "Prio", "ACAO", 45.20, "BRL"), ("RDOR3", "Rede D'Or", "ACAO", 28.90, "BRL"),
        ("RAIL3", "Rumo", "ACAO", 22.10, "BRL"), ("CSAN3", "Cosan", "ACAO", 15.80, "BRL"),
        ("B3SA3", "B3", "ACAO", 11.50, "BRL"), ("HAPV3", "Hapvida", "ACAO", 3.90, "BRL"),
        ("ELET3", "Eletrobras ON", "ACAO", 38.20, "BRL"), ("ELET6", "Eletrobras PNB", "ACAO", 42.10, "BRL"),
        ("EMBR3", "Embraer", "ACAO", 28.50, "BRL"), ("CMIG4", "Cemig", "ACAO", 10.20, "BRL"),
        ("CPLE6", "Copel", "ACAO", 9.80, "BRL"), ("SBSP3", "Sabesp", "ACAO", 78.50, "BRL"),
        ("TIMS3", "TIM", "ACAO", 17.20, "BRL"), ("VIVT3", "Vivo", "ACAO", 50.10, "BRL"),
        ("UGPA3", "Ultrapar", "ACAO", 26.40, "BRL"), ("EQTL3", "Equatorial", "ACAO", 32.10, "BRL"),
        ("RADL3", "Raia Drogasil", "ACAO", 26.50, "BRL"), ("TOTS3", "Totvs", "ACAO", 29.80, "BRL"),
        ("CSNA3", "CSN Siderurgia", "ACAO", 14.20, "BRL"), ("USIM5", "Usiminas", "ACAO", 7.50, "BRL"),
        ("GOAU4", "Metalúrgica Gerdau", "ACAO", 10.50, "BRL"), ("BRFS3", "BRF", "ACAO", 16.20, "BRL"),
        ("MRFG3", "Marfrig", "ACAO", 9.80, "BRL"), ("BEEF3", "Minerva", "ACAO", 6.50, "BRL"),
        ("KLBN11", "Klabin", "ACAO", 21.50, "BRL"), ("ALOS3", "Allos", "ACAO", 23.40, "BRL"),
        ("MULT3", "Multiplan", "ACAO", 25.10, "BRL"), ("IGTI11", "Iguatemi", "ACAO", 22.80, "BRL"),
        ("CYRE3", "Cyrela", "ACAO", 21.50, "BRL"), ("EZTC3", "EZTEC", "ACAO", 15.20, "BRL"),
        ("MRVE3", "MRV", "ACAO", 7.80, "BRL"), ("CVCB3", "CVC", "ACAO", 2.50, "BRL"),
        ("GOLL4", "Gol", "ACAO", 1.80, "BRL"), ("AZUL4", "Azul", "ACAO", 10.50, "BRL"),
        ("PETZ3", "Petz", "ACAO", 4.20, "BRL"), ("SOMA3", "Grupo Soma", "ACAO", 7.10, "BRL"),
        ("ARZZ3", "Arezzo", "ACAO", 60.50, "BRL"), ("ASAI3", "Assaí", "ACAO", 13.50, "BRL"),
        ("CRFB3", "Carrefour", "ACAO", 10.80, "BRL"), ("SLCE3", "SLC Agrícola", "ACAO", 18.50, "BRL"),
        ("STBP3", "Santos Brasil", "ACAO", 13.20, "BRL"), ("RRRP3", "3R Petroleum", "ACAO", 30.50, "BRL"),
        ("RECV3", "PetroReconcavo", "ACAO", 21.00, "BRL"), ("VBBR3", "Vibra", "ACAO", 24.50, "BRL"),
        ("CPFE3", "CPFL Energia", "ACAO", 34.00, "BRL"), ("EGIE3", "Engie Brasil", "ACAO", 42.50, "BRL"),
        ("TRPL4", "ISA CTEEP", "ACAO", 25.80, "BRL"), ("TAEE11", "Taesa", "ACAO", 36.50, "BRL"),
        ("ALUP11", "Alupar", "ACAO", 30.20, "BRL"), ("SAPR11", "Sanepar", "ACAO", 28.50, "BRL"),
        ("CSMG3", "Copasa", "ACAO", 19.80, "BRL"), ("BRAP4", "Bradespar", "ACAO", 20.50, "BRL"),
        ("POMO4", "Marcopolo", "ACAO", 7.80, "BRL"), ("RANI3", "Irani", "ACAO", 10.20, "BRL"),
        ("TASA4", "Taurus", "ACAO", 14.50, "BRL"), ("POSI3", "Positivo", "ACAO", 8.20, "BRL"),
        ("INTB3", "Intelbras", "ACAO", 22.00, "BRL"), ("LWSA3", "Locaweb", "ACAO", 5.50, "BRL"),
        ("CASH3", "Méliuz", "ACAO", 7.80, "BRL"), ("HYPE3", "Hypera", "ACAO", 32.50, "BRL"),
        ("FLRY3", "Fleury", "ACAO", 16.80, "BRL"), ("ODPV3", "Odontoprev", "ACAO", 12.50, "BRL"),
        ("PSSA3", "Porto Seguro", "ACAO", 28.50, "BRL"), ("BBSE3", "BB Seguridade", "ACAO", 33.50, "BRL"),
        ("CXSE3", "Caixa Seguridade", "ACAO", 14.20, "BRL"), ("IRBR3", "IRB Brasil", "ACAO", 40.50, "BRL"),
        
        # --- FUNDOS IMOBILIÁRIOS (IFIX Completo e Populares) ---
        ("KNRI11", "Kinea Renda", "FII", 160.00, "BRL"), ("HGLG11", "CSHG Logística", "FII", 165.50, "BRL"),
        ("MXRF11", "Maxi Renda", "FII", 10.55, "BRL"), ("XPLG11", "XP Logística", "FII", 108.20, "BRL"),
        ("VISC11", "Vinci Shoppings", "FII", 120.50, "BRL"), ("HGRU11", "CSHG Renda Urbana", "FII", 130.20, "BRL"),
        ("BCFF11", "BTG Fundo de Fundos", "FII", 9.20, "BRL"), ("IRDM11", "Iridium Recebíveis", "FII", 75.50, "BRL"),
        ("KNIP11", "Kinea Índices", "FII", 95.20, "BRL"), ("KNCR11", "Kinea Rendimentos", "FII", 102.50, "BRL"),
        ("CPTS11", "Capitânia Securities", "FII", 8.50, "BRL"), ("RECR11", "Rec Recebíveis", "FII", 85.20, "BRL"),
        ("HFOF11", "Hedge Top FOF", "FII", 78.50, "BRL"), ("JSRE11", "JS Real Estate", "FII", 70.10, "BRL"),
        ("VILG11", "Vinci Logística", "FII", 98.50, "BRL"), ("MALL11", "Malls Brasil", "FII", 115.00, "BRL"),
        ("XPML11", "XP Malls", "FII", 118.50, "BRL"), ("BTLG11", "BTG Logística", "FII", 102.80, "BRL"),
        ("PVBI11", "VBI Prime Properties", "FII", 105.50, "BRL"), ("LVBI11", "VBI Logística", "FII", 116.00, "BRL"),
        ("BRCO11", "Bresco Logística", "FII", 122.50, "BRL"), ("HCTR11", "Hectare CE", "FII", 35.50, "BRL"),
        ("DEVA11", "Devant Recebíveis", "FII", 42.80, "BRL"), ("TORD11", "Tordesilhas", "FII", 2.50, "BRL"),
        ("VGHF11", "Valora Hedge", "FII", 9.10, "BRL"), ("VGIP11", "Valora Cri", "FII", 88.50, "BRL"),
        ("RBRR11", "RBR Rendimento", "FII", 89.20, "BRL"), ("RBRF11", "RBR Alpha", "FII", 75.50, "BRL"),
        ("ALZR11", "Alianza Trust", "FII", 112.50, "BRL"), ("TRXF11", "TRX Real Estate", "FII", 110.00, "BRL"),
        ("RECT11", "Rec Renda Imob", "FII", 38.00, "BRL"), ("SARE11", "Santander Renda", "FII", 45.20, "BRL"),
        ("RBRP11", "RBR Properties", "FII", 55.00, "BRL"), ("RBRY11", "RBR Crédito", "FII", 98.00, "BRL"),
        ("TGAR11", "TG Ativo Real", "FII", 120.00, "BRL"), ("KNSC11", "Kinea Securities", "FII", 89.00, "BRL"),
        ("HGBS11", "Hedge Brasil Shop", "FII", 220.00, "BRL"), ("HGRE11", "CSHG Real Estate", "FII", 130.00, "BRL"),
        ("KNHY11", "Kinea High Yield", "FII", 98.00, "BRL"), ("VSLH11", "Versalhes", "FII", 3.50, "BRL"),
        ("HSLG11", "HSI Logística", "FII", 95.00, "BRL"), ("GTWR11", "Green Towers", "FII", 85.00, "BRL"),
        ("GGRC11", "GGR Covepi", "FII", 112.00, "BRL"), ("VRTA11", "Fator Verita", "FII", 88.00, "BRL"),
        ("CVBI11", "VBI CRI", "FII", 92.00, "BRL"), ("BTRA11", "BTG Terras", "FII", 65.00, "BRL"),
        ("RBRL11", "RBR Log", "FII", 82.00, "BRL"), ("XPIN11", "XP Industrial", "FII", 78.00, "BRL"),
        ("VINO11", "Vinci Offices", "FII", 8.50, "BRL"), ("SAAG11", "Santander Agências", "FII", 88.00, "BRL"),
        ("OUJP11", "Ourinvest JPP", "FII", 95.00, "BRL"), ("MCCI11", "Mauá Capital", "FII", 92.00, "BRL"),
        ("FIIB11", "Industrial Brasil", "FII", 450.00, "BRL"), ("RBVA11", "Rio Bravo Varejo", "FII", 110.00, "BRL"),
        ("BARI11", "Barigui Rendimentos", "FII", 90.00, "BRL"), ("HGCR11", "CSHG Recebíveis", "FII", 102.00, "BRL"),

        # --- STOCKS AMERICANOS (S&P 500 / NASDAQ) ---
        ("AAPL", "Apple Inc.", "STOCK", 185.50, "USD"), ("MSFT", "Microsoft Corp", "STOCK", 415.00, "USD"),
        ("NVDA", "Nvidia Corp", "STOCK", 880.00, "USD"), ("GOOGL", "Alphabet Inc.", "STOCK", 175.50, "USD"),
        ("AMZN", "Amazon.com", "STOCK", 180.20, "USD"), ("META", "Meta Platforms", "STOCK", 490.50, "USD"),
        ("TSLA", "Tesla Inc.", "STOCK", 170.20, "USD"), ("BRK.B", "Berkshire Hathaway", "STOCK", 410.00, "USD"),
        ("LLY", "Eli Lilly", "STOCK", 780.00, "USD"), ("V", "Visa Inc.", "STOCK", 280.50, "USD"),
        ("JPM", "JPMorgan Chase", "STOCK", 195.00, "USD"), ("WMT", "Walmart", "STOCK", 60.50, "USD"),
        ("XOM", "Exxon Mobil", "STOCK", 115.00, "USD"), ("UNH", "UnitedHealth", "STOCK", 480.00, "USD"),
        ("MA", "Mastercard", "STOCK", 470.00, "USD"), ("PG", "Procter & Gamble", "STOCK", 160.00, "USD"),
        ("JNJ", "Johnson & Johnson", "STOCK", 155.00, "USD"), ("HD", "Home Depot", "STOCK", 370.00, "USD"),
        ("MRK", "Merck & Co", "STOCK", 125.00, "USD"), ("COST", "Costco Wholesale", "STOCK", 750.00, "USD"),
        ("KO", "Coca-Cola", "STOCK", 60.00, "USD"), ("PEP", "PepsiCo", "STOCK", 168.00, "USD"),
        ("BAC", "Bank of America", "STOCK", 36.00, "USD"), ("NFLX", "Netflix", "STOCK", 610.00, "USD"),
        ("AMD", "Advanced Micro Devices", "STOCK", 170.00, "USD"), ("DIS", "Walt Disney", "STOCK", 110.00, "USD"),
        ("NKE", "Nike", "STOCK", 95.00, "USD"), ("MCD", "McDonald's", "STOCK", 280.00, "USD"),
        ("INTC", "Intel Corp", "STOCK", 40.00, "USD"), ("PFE", "Pfizer", "STOCK", 27.00, "USD"),

        # --- BDRs ---
        ("MELI34", "Mercado Livre", "BDR", 85.40, "BRL"), ("TSLA34", "Tesla Inc.", "BDR", 35.20, "BRL"),
        ("NVDC34", "Nvidia Corp", "BDR", 115.20, "BRL"), ("AAPL34", "Apple Inc.", "BDR", 48.50, "BRL"),
        ("MSFT34", "Microsoft", "BDR", 55.20, "BRL"), ("GOGL34", "Alphabet", "BDR", 45.80, "BRL"),
        ("AMZO34", "Amazon", "BDR", 38.90, "BRL"), ("M1TA34", "Meta", "BDR", 65.40, "BRL"),
        ("BABA34", "Alibaba", "BDR", 18.50, "BRL"), ("NFLX34", "Netflix", "BDR", 42.10, "BRL"),
        ("COCA34", "Coca-Cola", "BDR", 52.00, "BRL"), ("DISB34", "Disney", "BDR", 32.50, "BRL"),
        ("VISA34", "Visa", "BDR", 60.20, "BRL"), ("MCDB34", "McDonalds", "BDR", 72.00, "BRL"),
        ("PGCO34", "P&G", "BDR", 58.50, "BRL"), ("WALM34", "Walmart", "BDR", 45.00, "BRL"),
        ("JNJB34", "Johnson & Johnson", "BDR", 62.00, "BRL"), ("PFIZ34", "Pfizer", "BDR", 28.00, "BRL"),
        ("NIKE34", "Nike", "BDR", 35.00, "BRL"), ("SBUB34", "Starbucks", "BDR", 48.00, "BRL"),

        # --- REITS (Real Estate Investment Trusts) ---
        ("O", "Realty Income", "REIT", 52.30, "USD"), ("PLD", "Prologis Inc", "REIT", 120.50, "USD"),
        ("AMT", "American Tower", "REIT", 190.00, "USD"), ("EQIX", "Equinix", "REIT", 820.00, "USD"),
        ("PSA", "Public Storage", "REIT", 280.00, "USD"), ("DLR", "Digital Realty", "REIT", 145.00, "USD"),
        ("SPG", "Simon Property", "REIT", 150.00, "USD"), ("VICI", "VICI Properties", "REIT", 29.00, "USD"),
        ("CCI", "Crown Castle", "REIT", 105.00, "USD"), ("WELL", "Welltower", "REIT", 95.00, "USD"),
        ("AVB", "AvalonBay", "REIT", 185.00, "USD"), ("EQR", "Equity Residential", "REIT", 65.00, "USD"),
        ("MAA", "Mid-America", "REIT", 130.00, "USD"), ("ESS", "Essex Property", "REIT", 240.00, "USD"),
        ("ARE", "Alexandria RE", "REIT", 120.00, "USD"), ("BXP", "Boston Properties", "REIT", 65.00, "USD"),

        # --- CRIPTOMOEDAS ---
        ("BTC", "Bitcoin", "CRIPTO", 65000.00, "USD"), ("ETH", "Ethereum", "CRIPTO", 3500.00, "USD"),
        ("SOL", "Solana", "CRIPTO", 145.00, "USD"), ("BNB", "Binance Coin", "CRIPTO", 600.00, "USD"),
        ("XRP", "Ripple", "CRIPTO", 0.62, "USD"), ("ADA", "Cardano", "CRIPTO", 0.58, "USD"),
        ("AVAX", "Avalanche", "CRIPTO", 45.00, "USD"), ("DOGE", "Dogecoin", "CRIPTO", 0.15, "USD"),
        ("DOT", "Polkadot", "CRIPTO", 8.50, "USD"), ("LINK", "Chainlink", "CRIPTO", 18.00, "USD"),
        ("MATIC", "Polygon", "CRIPTO", 0.90, "USD"), ("SHIB", "Shiba Inu", "CRIPTO", 0.000025, "USD"),
        ("LTC", "Litecoin", "CRIPTO", 85.00, "USD"), ("BCH", "Bitcoin Cash", "CRIPTO", 450.00, "USD"),
        ("UNI", "Uniswap", "CRIPTO", 12.00, "USD"), ("ATOM", "Cosmos", "CRIPTO", 11.00, "USD"),

        # --- ETFs BRASIL ---
        ("IVVB11", "iShares S&P 500", "ETF_NACIONAL", 280.00, "BRL"), ("BOVA11", "iShares Ibovespa", "ETF_NACIONAL", 125.00, "BRL"),
        ("SMAL11", "iShares Small Cap", "ETF_NACIONAL", 105.00, "BRL"), ("HASH11", "Hashdex Crypto", "ETF_NACIONAL", 35.00, "BRL"),
        ("NASD11", "Trend Nasdaq", "ETF_NACIONAL", 12.50, "BRL"), ("XINA11", "Trend China", "ETF_NACIONAL", 8.50, "BRL"),
        ("GOLD11", "Trend Ouro", "ETF_NACIONAL", 11.20, "BRL"), ("DIVO11", "Itau Dividendos", "ETF_NACIONAL", 95.00, "BRL"),
        ("MATB11", "Itau Materiais", "ETF_NACIONAL", 35.00, "BRL"), ("BRAX11", "iShares BrX-100", "ETF_NACIONAL", 90.00, "BRL"),

        # --- ETFs AMERICANOS ---
        ("VOO", "Vanguard S&P 500", "ETF_EUA", 410.00, "USD"), ("SPY", "SPDR S&P 500", "ETF_EUA", 510.00, "USD"),
        ("QQQ", "Invesco QQQ", "ETF_EUA", 440.00, "USD"), ("VTI", "Vanguard Total Stock", "ETF_EUA", 255.00, "USD"),
        ("SCHD", "Schwab US Dividend", "ETF_EUA", 78.00, "USD"), ("JEPI", "JPMorgan Equity", "ETF_EUA", 56.00, "USD"),
        ("VT", "Vanguard Total World", "ETF_EUA", 105.00, "USD"), ("TLT", "iShares 20+ Year", "ETF_EUA", 92.00, "USD"),
        ("VNQ", "Vanguard Real Estate", "ETF_EUA", 85.00, "USD"), ("GLD", "SPDR Gold Shares", "ETF_EUA", 205.00, "USD"),

        # --- ETFs IRLANDESES ---
        ("VWRA", "Vanguard All-World", "ETF_IRLANDA", 115.00, "USD"), ("VUAA", "Vanguard S&P 500", "ETF_IRLANDA", 85.50, "USD"),
        ("CSPX", "iShares Core S&P 500", "ETF_IRLANDA", 490.00, "USD"), ("EIMI", "iShares EM IMI", "ETF_IRLANDA", 30.00, "USD"),
        ("IWDA", "iShares Core MSCI World", "ETF_IRLANDA", 88.00, "USD"), ("SXR8", "iShares S&P 500 EUR", "ETF_IRLANDA", 450.00, "USD"),
        ("AGGU", "iShares Global Bond", "ETF_IRLANDA", 5.20, "USD"), ("IB01", "iShares Treasury 0-1yr", "ETF_IRLANDA", 105.00, "USD")
    ]

    processed_assets = []
    
    # Processamento em loop
    for ticker, name, type_, price, currency in raw_assets:
        
        final_price = get_variation(price)
        indicators = generate_indicators(type_)
        
        processed_assets.append({
            "id": f"{type_.lower()}_{ticker.lower()}",
            "ticker": ticker,
            "name": name,
            "type": type_,
            "price": final_price,
            "quantity": 0,
            "currency": currency,
            "indicators": indicators,
            "history": generate_history(final_price)
        })

    # ==========================================
    # 2. ÍNDICES DE MERCADO E MOEDAS
    # ==========================================
    market_indices = [
        {"id": "idx_selic", "ticker": "SELIC", "name": "Taxa Selic", "type": "INDEX", "price": 11.25, "format": "percent"},
        {"id": "idx_infla", "ticker": "INFLACAO", "name": "Inflação (IPCA)", "type": "INDEX", "price": 4.50, "format": "percent"},
        {"id": "idx1", "ticker": "CDI", "name": "Taxa CDI", "type": "INDEX", "price": 11.15, "format": "percent"},
        {"id": "idx2", "ticker": "IPCA", "name": "IPCA 12m", "type": "INDEX", "price": 4.62, "format": "percent"},
        {"id": "idx3", "ticker": "IBOV", "name": "Ibovespa", "type": "INDEX", "price": 128500, "format": "points"},
        {"id": "idx4", "ticker": "SMLL", "name": "Small Caps", "type": "INDEX", "price": 2150, "format": "points"},
        {"id": "idx5", "ticker": "IFIX", "name": "Índice FIIs", "type": "INDEX", "price": 3350, "format": "points"},
        {"id": "idx6", "ticker": "IDIV", "name": "Índice Dividendos", "type": "INDEX", "price": 7800, "format": "points"},
        {"id": "curr1", "ticker": "DOLAR", "name": "Dólar Americano", "type": "CURRENCY", "price": 6.05, "format": "currency"},
        {"id": "curr2", "ticker": "EURO", "name": "Euro", "type": "CURRENCY", "price": 6.45, "format": "currency"},
        {"id": "curr3", "ticker": "LIBRA", "name": "Libra Esterlina", "type": "CURRENCY", "price": 7.62, "format": "currency"},
        {"id": "curr4", "ticker": "BITCOIN", "name": "Bitcoin (BRL)", "type": "CURRENCY", "price": 395000, "format": "currency"},
        {"id": "curr5", "ticker": "YUAN", "name": "Yuan Chinês", "type": "CURRENCY", "price": 0.83, "format": "currency"},
    ]

    for idx in market_indices:
        vol = 0.005 if idx['format'] == 'percent' else 0.015
        idx['price'] = get_variation(idx['price'], vol)
        idx['history'] = generate_history(idx['price'])

    # ==========================================
    # 3. SALVAR
    # ==========================================
    full_data = processed_assets + market_indices
    file_path = 'dados_b3_atualizados.json'

    try:
        full_path = os.path.join(os.getcwd(), file_path)
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
        print(f"Sucesso! {len(full_data)} itens gerados (Ativos: {len(processed_assets)} | Índices: {len(market_indices)})")
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
