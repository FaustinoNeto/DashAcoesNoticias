import requests
from bs4 import BeautifulSoup
import time

def get_stock_news(selected_acao):
    acao_mapping = [
        ('CEAB3.SA', 'CEAB3'),
        ('WEGE3.SA', 'WEGE3'),
        ('PETR4.SA', 'PETR4'),
        
    ]

    selected_acao = next((mapped_acao for input_acao, mapped_acao in acao_mapping if input_acao == selected_acao), selected_acao)

    url = f"https://valorinveste.globo.com/busca/?q={selected_acao}&page=1&order=recent"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Erro durante a solicitação HTTP: {e}")
        return None
    except Exception as e:
        print(f"Erro durante a análise HTML: {e}")
        return None

    articles = soup.find_all('div', class_='widget--info__text-container')
    news_list = []

    for i, article in enumerate(articles[:3]):
        link_element = article.find('a', href=True)
        title_element = article.find('div', class_='widget--info__title product-color')

        link = f"https:{link_element['href']}" if link_element and 'href' in link_element.attrs else None
        title = title_element.text.strip() if title_element else None

        news = {'title': title, 'link': link}
        news_list.append(news)
        time.sleep(1)

    return news_list

