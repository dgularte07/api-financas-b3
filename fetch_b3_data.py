import yfinance as yf
import json
from datetime import datetime

# Lista de ativos que queremos monitorar
# Note o ".SA" no final, que indica que são da Bolsa de São Paulo (B3)
tickers = [
    "VALE3.SA", "PETR4.SA", "ITUB4.SA", "BBDC4.SA", "WEGE3.SA", 
    "BBAS3.SA", "TAEE11.SA", "KLBN11.SA", "MXRF11.SA", "HGLG11.SA", 
    "IVVB11.SA", "BOVA11.SA", "SMAL11.SA"
]

def fetch_data():
    print(f"--- Iniciando Coleta de Dados: {datetime.now()} ---")
    
    data_list = []
    
    # Baixa dados de todos os tickers de uma vez (mais eficiente)
    # period="5d" pega os últimos 5 dias para termos histórico recente
    tickers_data = yf.download(tickers, period="5d", interval="1d")
    
    for ticker in tickers:
        try:
            # Tratamento para pegar o preço mais recente
            # O Yahoo Finance retorna um DataFrame pandas complexo, simplificamos aqui:
            hist = tickers_data['Close'][ticker].dropna()
            
            if hist.empty:
                print(f"Sem dados para {ticker}")
                continue
                
            current_price = float(hist.iloc[-1])
            prev_close = float(hist.iloc[-2]) if len(hist) > 1 else current_price
            
            # Calcular variação
            change_percent = ((current_price - prev_close) / prev_close) * 100
            
            # Classificar o tipo baseado no código (Lógica simples para demonstração)
            asset_type = "Ação"
            if "11" in ticker:
                # Simplificação: 11 geralmente é Unit, ETF ou FII. 
                # Num sistema real, teríamos uma lista de cadastro.
                asset_type = "FII/ETF" 

            # Formata o objeto final
            asset_obj = {
                "code": ticker.replace(".SA", ""), # Remove o .SA para ficar bonito no App
                "name": ticker, # Em um app real, buscaríamos o nome completo numa tabela auxiliar
                "type": asset_type,
                "value": round(current_price, 2),
                "change": round(change_percent, 2),
                "segment": "Geral", # Precisaria de uma base externa para saber o setor exato
                "dividendYield": 0.0, # O yfinance as vezes traz isso em 'info', mas é lento para buscar em lote
                "extra": "Atualizado"
            }
            
            data_list.append(asset_obj)
            print(f"Coletado: {ticker} - R$ {current_price:.2f}")
            
        except Exception as e:
            print(f"Erro ao processar {ticker}: {e}")

    # Salva em um arquivo JSON que o nosso site poderia ler
    with open("dados_b3_atualizados.json", "w", encoding='utf-8') as f:
        json.dump(data_list, f, indent=2, ensure_ascii=False)
        
    print("--- Base de dados atualizada com sucesso! ---")
    print("Copie o conteúdo de 'dados_b3_atualizados.json' para o seu código React.")

if __name__ == "__main__":
    fetch_data()