import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json
import random
import time
import math
import logging
from datetime import datetime
import os
import re

# Configuração de Logs (Isso garante que você veja o que está acontecendo no GitHub)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==============================================================================
# 1. CATÁLOGO COMPLETO DE ATIVOS
# ==============================================================================
# ... (Logo abaixo vêm as listas BRAZIL_STOCKS, FIIS, etc.)
