import requests
from bs4 import BeautifulSoup

url = "https://pt.wikipedia.org/wiki/2010_no_cinema"
def remove_space_and_parenteses(text):
    title = text.replace(" ", "_")
    title = title.replace("(", "")
    title = title.replace(")", "")
    title = title.replace("_filme", "")
    # title = title.replace("_2010", "")
    title = title.replace("The_", "")
    title = title.replace("-", "_")
    title = title.replace("'", "")
    title = title.replace(",", "")
    return title

def call_list(url="https://pt.wikipedia.org/wiki/2010_no_cinema"):
    movie_titles = []
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Buscando todas as tabelas
        tables = soup.find_all('table', class_="wikitable")

        # Removendo a tabela das maiores bileterias
        tables.remove(tables[0])
        for table in tables:
            links = table.findChildren('i', class_='')
            for link in links:
                names = link.findChildren('a', class_='')
                for name in names:
                    title = name.get('title')
                    title = remove_space_and_parenteses(title)
                    movie_titles.append(title)
        return movie_titles

    else:
        print("Falha, status: {}".format(response.status_code))
