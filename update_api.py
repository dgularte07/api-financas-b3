#!/usr/bin/env python3
import json
import random
import os
import sys

# Garante que o encoding de saída seja UTF-8 para não dar erro com acentos no log
sys.stdout.reconfigure(encoding='utf-8')

def get_variation(base_price):
    """Gera uma variação aleatória de preço para simular mercado real."""
    change = random.uniform(-0.02, 0.02) # Variação de +/- 2%
    return round(base_price * (1 + change), 2)

def main():
    print("Iniciando geração de dados simulados...")

    # Dados Base (Simulando uma coleta de API real)
    data = [
      {
        "id": "1",
        "ticker": "WEGE3",
        "name": "Weg S.A.",
        "type": "ACAO",
        "price": get_variation(40.50),
        "quantity": 100,
        "currency": "BRL",
        "indicators": {
          "pl": 35.5,
          "roe": 25.4,
          "margem_liquida": 14.2,
          "cagr_lucros_5y": 18.5,
          "dy": 1.2
        }
      },
      {
        "id": "2",
        "ticker": "VALE3",
        "name": "Vale S.A.",
        "type": "ACAO",
        "price": get_variation(68.20),
        "quantity": 50,
        "currency": "BRL",
        "indicators": {
          "pl": 5.5,
          "roe": 30.1,
          "margem_liquida": 28.2,
          "cagr_lucros_5y": 12.5,
          "dy": 8.5
        }
      },
      {
        "id": "3",
        "ticker": "KNRI11",
        "name": "Kinea Renda",
        "type": "FII",
        "price": get_variation(160.00),
        "quantity": 20,
        "currency": "BRL",
        "indicators": {
          "p_vp": 1.01,
          "dy_12m": 8.5,
          "vacancia_fisica": 2.5,
          "vacancia_financeira": 0.0,
          "liquidez_diaria": 3500000
        }
      },
      {
        "id": "4",
        "ticker": "HGLG11",
        "name": "CSHG Logística",
        "type": "FII",
        "price": get_variation(165.50),
        "quantity": 15,
        "currency": "BRL",
        "indicators": {
          "p_vp": 1.05,
          "dy_12m": 9.1,
          "vacancia_fisica": 1.5,
          "vacancia_financeira": 0.5,
          "liquidez_diaria": 5500000
        }
      },
      {
        "id": "5",
        "ticker": "AAPL34",
        "name": "Apple Inc.",
        "type": "BDR",
        "price": get_variation(45.20),
        "quantity": 40,
        "currency": "BRL",
        "indicators": {
          "pl": 28.4,
          "roe": 160.0,
          "margem_liquida": 24.5,
          "cagr_lucros_5y": 12.0,
          "dy": 0.6
        }
      },
      {
        "id": "6",
        "ticker": "O",
        "name": "Realty Income",
        "type": "REIT",
        "price": get_variation(52.30),
        "quantity": 10,
        "currency": "USD",
        "indicators": {
          "p_ffo": 14.2,
          "dy_annual": 5.4,
          "vacancia_fisica": 1.1,
          "divida_ebitda": 5.2,
          "payout_ratio": 75.0
        }
      },
      {
        "id": "7",
        "ticker": "IVVB11",
        "name": "iShares S&P 500",
        "type": "ETF_NACIONAL",
        "price": get_variation(280.00),
        "quantity": 10,
        "currency": "BRL",
        "indicators": {
          "taxa_adm": 0.23,
          "sharpe_ratio": 0.85,
          "volatilidade_12m": 15.4,
          "aum_milhoes": 2500.00
        }
      },
      {
        "id": "8",
        "ticker": "VOO",
        "name": "Vanguard S&P 500",
        "type": "ETF_EUA",
        "price": get_variation(410.00),
        "quantity": 5,
        "currency": "USD",
        "indicators": {
          "taxa_adm": 0.03,
          "sharpe_ratio": 0.92,
          "volatilidade_12m": 14.8,
          "aum_bilhoes": 850.00
        }
      },
      {
        "id": "9",
        "ticker": "VWRA",
        "name": "Vanguard All-World",
        "type": "ETF_IRLANDA",
        "price": get_variation(115.00),
        "quantity": 15,
        "currency": "USD",
        "indicators": {
          "taxa_adm": 0.22,
          "sharpe_ratio": 0.78,
          "volatilidade_12m": 16.2,
          "aum_milhoes": 4500.00
        }
      },
      {
        "id": "10",
        "ticker": "BTC",
        "name": "Bitcoin",
        "type": "CRIPTO",
        "price": get_variation(65000.00),
        "quantity": 0.005,
        "currency": "USD",
        "indicators": {
          "market_cap_bilhoes": 1200.00,
          "vol_24h_bilhoes": 35.5,
          "hashrate": "600 EH/s",
          "tvl": None
        }
      },
       {
        "id": "11",
        "ticker": "ETH",
        "name": "Ethereum",
        "type": "CRIPTO",
        "price": get_variation(3500.00),
        "quantity": 0.5,
        "currency": "USD",
        "indicators": {
          "market_cap_bilhoes": 400.00,
          "vol_24h_bilhoes": 15.2,
          "hashrate": None,
          "tvl_bilhoes": 55.4
        }
      }
    ]

    # Salva o arquivo JSON que o App vai ler
    file_path = 'dados_b3_atualizados.json'

    try:
        # Garante que escrevemos no diretório atual
        full_path = os.path.join(os.getcwd(), file_path)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Sucesso! Arquivo gerado em: {full_path}")
        print(f"Total de ativos: {len(data)}")
        
    except Exception as e:
        print(f"Erro fatal ao salvar arquivo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
