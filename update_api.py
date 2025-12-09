#!/usr/bin/env python3
import json
import random
import os
import sys
from datetime import datetime, timedelta

# Garante encoding UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def get_variation(base_price, volatility=0.02):
    """Simula variação de mercado."""
    change = random.uniform(-volatility, volatility)
    return round(base_price * (1 + change), 2)

def generate_history(current_price):
    """Gera histórico simulado para gráficos."""
    history = {}
    periods = [('1D', 24, 0.005), ('7D', 7, 0.015), ('30D', 30, 0.03), ('6M', 6, 0.08), ('1A', 12, 0.12), ('5A', 5, 0.25)]
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
    """Gera indicadores fundamentalistas baseados no tipo."""
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
    print("Iniciando geração COMPLETA da B3 + Mercado Global...")

    raw_assets = []

    # ==========================================
    # 1. TODOS OS ATIVOS BRASILEIROS (Ações)
    # ==========================================
    # Lista abrangente cobrindo IBOV, IBRX100 e Small Caps
    acoes_b3 = [
        "RRRP3", "ALOS3", "ALPA4", "ABEV3", "AMER3", "ARZZ3", "ASAI3", "AZUL4", "B3SA3", "BBSE3", 
        "BBDC3", "BBDC4", "BRAP4", "BBAS3", "BRKM5", "BRFS3", "BPAC11", "CRFB3", "CCRO3", "CMIG4", 
        "CIEL3", "COGN3", "CPLE6", "CSAN3", "CPFE3", "CMIN3", "CVCB3", "CYRE3", "DXCO3", "ELET3", 
        "ELET6", "EMBR3", "ENGI11", "ENEV3", "EGIE3", "EQTL3", "EZTC3", "FLRY3", "GGBR4", "GOAU4", 
        "GOLL4", "NTCO3", "HAPV3", "HYPE3", "IGTI11", "IRBR3", "ITSA4", "ITUB4", "JBSS3", "KLBN11", 
        "RENT3", "LWSA3", "LREN3", "MGLU3", "MRFG3", "CASH3", "BEEF3", "MRVE3", "MULT3", "PCAR3", 
        "PETR3", "PETR4", "PRIO3", "PETZ3", "POSI3", "QUAL3", "RADL3", "RAIZ4", "RDOR3", "RAIL3", 
        "SBSP3", "SANB11", "SMTO3", "SOMA3", "SLCE3", "SUZB3", "TAEE11", "VIVT3", "TIMS3", "TOTS3", 
        "UGPA3", "USIM5", "VALE3", "VIIA3", "VBBR3", "WEGE3", "YDUQ3", "AERI3", "AESB3", "AGRO3", 
        "ALLD3", "AMBP3", "ANIM3", "APER3", "ARML3", "AURE3", "B3SA3", "BKBR3", "BLAU3", "BMOB3", 
        "BOAS3", "BRBI11", "BRIT3", "BRPR3", "CAML3", "CBAV3", "CEAB3", "CLSA3", "COGN3", "CSMG3", 
        "CURY3", "CXSE3", "DASA3", "DESK3", "DIRR3", "ECOR3", "ENAT3", "ENJU3", "ESPA3", "EVEN3", 
        "FESA4", "FHER3", "FIQE3", "GMAT3", "GGPS3", "GRND3", "GUAR3", "HBOR3", "HBRE3", "HBSA3", 
        "IFCM3", "INTB3", "JALL3", "JHSF3", "JSLG3", "KEPL3", "LAVV3", "LJQQ3", "LOGG3", "LOGN3", 
        "MATD3", "MDIA3", "MEAL3", "MILS3", "MLAS3", "MOVI3", "MYPK3", "NEOE3", "NGRD3", "ODPV3", 
        "ONCO3", "OPCT3", "ORVR3", "PARD3", "PGMN3", "PLPL3", "PMAM3", "PNVL3", "POMO4", "PORT3", 
        "PRNR3", "PTBL3", "RANI3", "RAPT4", "RCSL3", "RDOR3", "RECV3", "ROMI3", "SBFG3", "SEQL3", 
        "SHOW3", "SIMH3", "SMFT3", "SOJA3", "SQIA3", "STBP3", "SYNE3", "TASA4", "TEND3", "TFCO4", 
        "TGMA3", "TRIS3", "TTEN3", "TUPY3", "UNIP6", "VAMO3", "VIVA3", "VLID3", "VULC3", "WIZS3",
        "ZAMP3"
    ]
    
    for t in acoes_b3:
        price = random.uniform(2, 100) # Preço base aleatório mas realista
        raw_assets.append((t, f"{t} S.A.", "ACAO", price, "BRL"))

    # ==========================================
    # 2. TODOS OS FUNDOS IMOBILIÁRIOS (IFIX e +)
    # ==========================================
    fiis_b3 = [
        "ABCP11", "AFHI11", "AIEC11", "ALZR11", "ARCT11", "ARRI11", "BARI11", "BBFI11B", "BBPO11", 
        "BCFF11", "BCIA11", "BCRI11", "BICE11", "BLMG11", "BPFF11", "BRCO11", "BRCR11", "BTAL11", 
        "BTRA11", "BTLG11", "CACR11", "CARE11", "CBOP11", "CEOC11", "CNES11", "CPFF11", "CPTS11", 
        "CVBI11", "DEVA11", "DRIT11", "ELDO11", "EQIR11", "ERCR11", "ESLP11", "EURO11", "EVBI11", 
        "FAED11", "FAMB11", "FATN11", "FCFL11", "FEXC11", "FIGS11", "FIIB11", "FIIP11B", "FISC11", 
        "FIVN11", "FLMA11", "FVPQ11", "GALG11", "GAME11", "GCFF11", "GCRI11", "GGRC11", "GSFI11", 
        "GTWR11", "HABT11", "HBCR11", "HBRH11", "HBTT11", "HCHG11", "HCTR11", "HFOF11", "HGBS11", 
        "HGCR11", "HGFF11", "HGIC11", "HGLG11", "HGPO11", "HGRE11", "HGRS11", "HGRU11", "HLOG11", 
        "HOSI11", "HRDF11", "HSAF11", "HSLG11", "HSML11", "HSRE11", "HTMX11", "HUSC11", "IDFI11", 
        "IRDM11", "JFLL11", "JSAF11", "JSRE11", "KFOF11", "KINP11", "KISU11", "KNCR11", "KNHY11", 
        "KNIP11", "KNRI11", "KNSC11", "LASC11", "LOFT11B", "LUGG11", "LVBI11", "MALL11", "MAXR11", 
        "MBRF11", "MCCI11", "MFII11", "MGFF11", "MORE11", "MXRF11", "NCHB11", "NEWL11", "NSLU11", 
        "ONEF11", "OUJP11", "PATL11", "PLCR11", "PORD11", "PQDP11", "PVBI11", "QAGR11", "RBDS11", 
        "RBED11", "RBFF11", "RBHG11", "RBHY11", "RBIR11", "RBLG11", "RBRF11", "RBRL11", "RBRP11", 
        "RBRR11", "RBRS11", "RBRY11", "RBTS11", "RBVA11", "RCFA11", "RCRB11", "RECR11", "RECT11", 
        "REIT11", "RELG11", "RFOF11", "RZAG11", "RZAK11", "RZTR11", "SADI11", "SARE11", "SDIL11", 
        "SNCI11", "SNFF11", "SPTW11", "SPXS11", "TEPP11", "TGAR11", "TORD11", "TRNT11", "TRXF11", 
        "URPR11", "VCJR11", "VGHF11", "VGIA11", "VGIP11", "VGIR11", "VIFI11", "VILG11", "VINO11", 
        "VISC11", "VIUR11", "VJFD11", "VOTS11", "VPSI11", "VRTA11", "VSHO11", "VSLH11", "VTLT11", 
        "XPCI11", "XPCM11", "XPHT11", "XPIN11", "XPLG11", "XPML11", "XPPR11", "XPSF11", "YCHY11"
    ]

    for t in fiis_b3:
        # Preços de FIIs variam muito, alguns base 10, outros base 100
        price = random.uniform(8, 12) if random.random() > 0.6 else random.uniform(80, 150)
        raw_assets.append((t, f"Fundo {t}", "FII", price, "BRL"))

    # ==========================================
    # 3. MERCADO INTERNACIONAL (100 de cada categoria principal)
    # ==========================================
    
    # Stocks (Top 100)
    stock_tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B", "UNH", "JNJ", "XOM", "JPM", 
        "PG", "V", "LLY", "MA", "HD", "CVX", "MRK", "ABBV", "PEP", "KO", "AVGO", "COST", "TMO", "MCD", 
        "CSCO", "ACN", "ABT", "DHR", "WMT", "LIN", "CRM", "BAC", "ADBE", "DIS", "TXN", "PM", "VZ", "CMCSA", 
        "UPS", "NEE", "NKE", "BMY", "PFE", "NFLX", "QCOM", "INTC", "AMD", "RTX", "HON", "T", "AMGN", "IBM", 
        "UNP", "SPGI", "LOW", "ORCL", "MS", "CAT", "GS", "DE", "LMT", "SBUX", "PLD", "INTU", "AXP", "GE", 
        "BA", "MMM", "ISRG", "BLK", "MDLZ", "CVS", "BKNG", "GILD", "TGT", "TJX", "ADP", "SYK", "AMT", "CI", 
        "C", "MO", "SCHW", "TMUS", "CB", "MMC", "VRTX", "LRCX", "ADI", "ZTS", "PYPL", "DUK", "SO", "BSX", 
        "REGN", "EQIX", "BDX", "NOW"
    ]
    for t in stock_tickers:
        raw_assets.append((t, f"{t} Inc.", "STOCK", random.uniform(30, 800), "USD"))

    # REITs (Principais)
    reit_tickers = [
        "PLD", "AMT", "EQIX", "CCI", "PSA", "O", "SPG", "VICI", "WELL", "DLR", "AVB", "EQR", "CSGP", 
        "EXR", "INVH", "MAA", "SUN", "ESS", "BXP", "ARE", "VTR", "HST", "UDR", "KIM", "REG", "CPT", 
        "IRM", "FRT", "GLPI", "NNN", "STAG", "ADC", "EPR", "LXP", "HIW", "DOC", "OHI", "MPW", "WPC"
    ]
    for t in reit_tickers:
        raw_assets.append((t, f"{t} Reit", "REIT", random.uniform(20, 250), "USD"))

    # Criptos (Principais)
    crypto_list = [
        ("BTC", 65000), ("ETH", 3500), ("USDT", 1), ("BNB", 600), ("SOL", 145), ("XRP", 0.60), 
        ("USDC", 1), ("ADA", 0.58), ("AVAX", 45), ("DOGE", 0.15), ("DOT", 8.5), ("TRX", 0.12), 
        ("LINK", 18), ("MATIC", 0.90), ("WBTC", 65000), ("SHIB", 0.000025), ("LTC", 85), 
        ("DAI", 1), ("BCH", 450), ("UNI", 12), ("LEO", 5.8), ("ATOM", 11), ("ICP", 13), 
        ("IMX", 2.8), ("ETC", 30), ("FIL", 9), ("HBAR", 0.10), ("LDO", 2.5), ("APT", 13), 
        ("ARB", 1.5), ("CRO", 0.14), ("NEAR", 7), ("VET", 0.04), ("QNT", 115), ("MKR", 3200)
    ]
    for t, p in crypto_list:
        raw_assets.append((t, f"{t} Token", "CRIPTO", p, "USD"))

    # BDRs (Gerados baseados nas Stocks)
    for t in stock_tickers[:80]: # Pega as 80 maiores stocks
        raw_assets.append((f"{t}34", f"{t} BDR", "BDR", random.uniform(20, 100), "BRL"))

    # ETFs
    etfs = [
        ("IVVB11", "iShares S&P500", "ETF_NACIONAL", 280, "BRL"), ("BOVA11", "iShares Ibovespa", "ETF_NACIONAL", 125, "BRL"), 
        ("SMAL11", "iShares SmallCap", "ETF_NACIONAL", 105, "BRL"), ("HASH11", "Hashdex Crypto", "ETF_NACIONAL", 35, "BRL"),
        ("NASD11", "Trend Nasdaq", "ETF_NACIONAL", 12.50, "BRL"), ("XINA11", "Trend China", "ETF_NACIONAL", 8.50, "BRL"),
        ("GOLD11", "Trend Ouro", "ETF_NACIONAL", 11.20, "BRL"), ("DIVO11", "Itau Dividendos", "ETF_NACIONAL", 95, "BRL"),
        ("MATB11", "Itau Materiais", "ETF_NACIONAL", 35, "BRL"), ("BRAX11", "iShares BrX-100", "ETF_NACIONAL", 90, "BRL"),
        ("VOO", "Vanguard S&P500", "ETF_EUA", 410, "USD"), ("QQQ", "Invesco Nasdaq", "ETF_EUA", 440, "USD"), 
        ("VTI", "Vanguard Total", "ETF_EUA", 255, "USD"), ("SCHD", "Schwab Dividend", "ETF_EUA", 78, "USD"),
        ("VWRA", "Vanguard All-World", "ETF_IRLANDA", 115, "USD"), ("VUAA", "Vanguard S&P500", "ETF_IRLANDA", 85, "USD"), 
        ("CSPX", "iShares Core S&P", "ETF_IRLANDA", 490, "USD"), ("EIMI", "iShares EM", "ETF_IRLANDA", 30, "USD")
    ]
    for t, n, tp, p, c in etfs:
        raw_assets.append((t, n, tp, p, c))

    # ==========================================
    # PROCESSAMENTO E GERAÇÃO
    # ==========================================
    processed_assets = []
    
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
    # ÍNDICES DE MERCADO
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
    # SALVAR
    # ==========================================
    full_data = processed_assets + market_indices
    file_path = 'dados_b3_atualizados.json'

    try:
        full_path = os.path.join(os.getcwd(), file_path)
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
        print(f"Sucesso! {len(full_data)} itens gerados.")
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
