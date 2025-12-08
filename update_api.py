#!/usr/bin/env python3
import json
import random
import os
import sys
from datetime import datetime, timedelta

# Garante encoding UTF-8 para evitar erros de acentuação no log
sys.stdout.reconfigure(encoding='utf-8')

def get_variation(base_price, volatility=0.02):
    """Gera uma variação aleatória no preço para simular o mercado ao vivo."""
    change = random.uniform(-volatility, volatility)
    return round(base_price * (1 + change), 2)

def generate_history(current_price):
    """
    Gera histórico simulado para gráficos de 1D, 7D, 30D, 6M, 1A, 5A.
    """
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

def main():
    print("Iniciando geração completa de dados categorizados...")

    # ---------------------------------------------------------
    # 1. ATIVOS DA CARTEIRA
    # ---------------------------------------------------------
    assets = [
      # --- AÇÕES BRASIL (ACAO) ---
      {
        "id": "br1", "ticker": "WEGE3", "name": "Weg S.A.", "type": "ACAO",
        "price": 40.50, "quantity": 100, "currency": "BRL",
        "indicators": {"pl": 35.5, "roe": 25.4, "dy": 1.2}
      },
      {
        "id": "br2", "ticker": "VALE3", "name": "Vale S.A.", "type": "ACAO",
        "price": 68.20, "quantity": 50, "currency": "BRL",
        "indicators": {"pl": 5.5, "roe": 30.1, "dy": 8.5}
      },
      {
        "id": "br3", "ticker": "PETR4", "name": "Petrobras", "type": "ACAO",
        "price": 36.80, "quantity": 80, "currency": "BRL",
        "indicators": {"pl": 4.2, "roe": 32.5, "dy": 15.0}
      },
      {
        "id": "br4", "ticker": "ITUB4", "name": "Itaú Unibanco", "type": "ACAO",
        "price": 33.50, "quantity": 60, "currency": "BRL",
        "indicators": {"pl": 8.5, "roe": 20.0, "dy": 4.5}
      },

      # --- FUNDOS IMOBILIÁRIOS (FII) ---
      {
        "id": "fii1", "ticker": "KNRI11", "name": "Kinea Renda", "type": "FII",
        "price": 160.00, "quantity": 20, "currency": "BRL",
        "indicators": {"p_vp": 1.01, "dy_12m": 8.5, "vacancia_fisica": 2.5}
      },
      {
        "id": "fii2", "ticker": "HGLG11", "name": "CSHG Logística", "type": "FII",
        "price": 165.50, "quantity": 15, "currency": "BRL",
        "indicators": {"p_vp": 1.05, "dy_12m": 9.1, "vacancia_fisica": 1.5}
      },
      {
        "id": "fii3", "ticker": "MXRF11", "name": "Maxi Renda", "type": "FII",
        "price": 10.55, "quantity": 100, "currency": "BRL",
        "indicators": {"p_vp": 1.02, "dy_12m": 12.5, "vacancia_fisica": 0.0}
      },

      # --- STOCKS AMERICANOS (STOCK) ---
      {
        "id": "us1", "ticker": "AAPL", "name": "Apple Inc.", "type": "STOCK",
        "price": 185.50, "quantity": 5, "currency": "USD",
        "indicators": {"pl": 28.5, "roe": 150.0, "dy": 0.5}
      },
      {
        "id": "us2", "ticker": "MSFT", "name": "Microsoft Corp", "type": "STOCK",
        "price": 415.00, "quantity": 3, "currency": "USD",
        "indicators": {"pl": 35.2, "roe": 40.0, "dy": 0.7}
      },
      {
        "id": "us3", "ticker": "NVDA", "name": "Nvidia Corp", "type": "STOCK",
        "price": 880.00, "quantity": 2, "currency": "USD",
        "indicators": {"pl": 70.5, "roe": 90.0, "dy": 0.02}
      },

      # --- BDRs (BDR) ---
      {
        "id": "bdr1", "ticker": "MELI34", "name": "Mercado Livre", "type": "BDR",
        "price": 85.40, "quantity": 15, "currency": "BRL",
        "indicators": {"pl": 55.0, "roe": 25.0, "dy": 0.0}
      },
      {
        "id": "bdr2", "ticker": "TSLA34", "name": "Tesla Inc.", "type": "BDR",
        "price": 35.20, "quantity": 30, "currency": "BRL",
        "indicators": {"pl": 45.0, "roe": 20.0, "dy": 0.0}
      },

      # --- REITS (REIT) ---
      {
        "id": "reit1", "ticker": "O", "name": "Realty Income", "type": "REIT",
        "price": 52.30, "quantity": 10, "currency": "USD",
        "indicators": {"p_ffo": 14.2, "dy_annual": 5.4}
      },
      {
        "id": "reit2", "ticker": "PLD", "name": "Prologis Inc", "type": "REIT",
        "price": 120.50, "quantity": 5, "currency": "USD",
        "indicators": {"p_ffo": 22.0, "dy_annual": 2.8}
      },

      # --- CRIPTOMOEDAS (CRIPTO) ---
      {
        "id": "cr1", "ticker": "BTC", "name": "Bitcoin", "type": "CRIPTO",
        "price": 65000.00, "quantity": 0.005, "currency": "USD",
        "indicators": {"market_cap_bilhoes": 1200.00, "hashrate": "600 EH/s"}
      },
      {
        "id": "cr2", "ticker": "ETH", "name": "Ethereum", "type": "CRIPTO",
        "price": 3500.00, "quantity": 0.5, "currency": "USD",
        "indicators": {"market_cap_bilhoes": 400.00, "tvl_bilhoes": 55.4}
      },
      {
        "id": "cr3", "ticker": "SOL", "name": "Solana", "type": "CRIPTO",
        "price": 145.00, "quantity": 10, "currency": "USD",
        "indicators": {"market_cap_bilhoes": 65.00}
      },

      # --- ETFs BRASIL (ETF_NACIONAL) ---
      {
        "id": "etf_br1", "ticker": "IVVB11", "name": "iShares S&P 500", "type": "ETF_NACIONAL",
        "price": 280.00, "quantity": 10, "currency": "BRL",
        "indicators": {"taxa_adm": 0.23, "aum_milhoes": 2500.0}
      },
      {
        "id": "etf_br2", "ticker": "SMAL11", "name": "iShares Small Cap", "type": "ETF_NACIONAL",
        "price": 105.00, "quantity": 20, "currency": "BRL",
        "indicators": {"taxa_adm": 0.50, "aum_milhoes": 1200.0}
      },

      # --- ETFs AMERICANOS (ETF_EUA) ---
      {
        "id": "etf_us1", "ticker": "VOO", "name": "Vanguard S&P 500", "type": "ETF_EUA",
        "price": 410.00, "quantity": 5, "currency": "USD",
        "indicators": {"taxa_adm": 0.03, "sharpe_ratio": 0.92}
      },
      {
        "id": "etf_us2", "ticker": "QQQ", "name": "Invesco QQQ", "type": "ETF_EUA",
        "price": 440.00, "quantity": 4, "currency": "USD",
        "indicators": {"taxa_adm": 0.20, "sharpe_ratio": 1.1}
      },

      # --- ETFs IRLANDESES (ETF_IRLANDA) ---
      {
        "id": "etf_ie1", "ticker": "VWRA", "name": "Vanguard All-World", "type": "ETF_IRLANDA",
        "price": 115.00, "quantity": 15, "currency": "USD",
        "indicators": {"taxa_adm": 0.22, "aum_bilhoes": 15.0}
      },
      {
        "id": "etf_ie2", "ticker": "VUAA", "name": "Vanguard S&P 500", "type": "ETF_IRLANDA",
        "price": 85.50, "quantity": 20, "currency": "USD",
        "indicators": {"taxa_adm": 0.07, "aum_bilhoes": 8.5}
      }
    ]

    # Processa ativos: Atualiza preço e gera histórico
    for asset in assets:
        asset['price'] = get_variation(asset['price'])
        asset['history'] = generate_history(asset['price'])

    # ---------------------------------------------------------
    # 2. ÍNDICES DE MERCADO
    # ---------------------------------------------------------
    market_indices = [
        {"id": "idx1", "ticker": "CDI", "name": "Taxa CDI", "type": "INDEX", "price": 12.15, "format": "percent"},
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

    # Processa índices
    for idx in market_indices:
        vol = 0.005 if idx['format'] == 'percent' else 0.015
        idx['price'] = get_variation(idx['price'], vol)
        idx['history'] = generate_history(idx['price'])

    # ---------------------------------------------------------
    # 3. SALVAR ARQUIVO
    # ---------------------------------------------------------
    full_data = assets + market_indices
    file_path = 'dados_b3_atualizados.json'

    try:
        full_path = os.path.join(os.getcwd(), file_path)
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)

        print(f"Sucesso! Arquivo '{file_path}' gerado.")
        print(f"Ativos: {len(assets)} | Índices: {len(market_indices)}")
        
    except Exception as e:
        print(f"Erro fatal ao salvar arquivo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
