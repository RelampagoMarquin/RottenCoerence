from scrapingMovieName import call_list
import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

# Buscando a lista de filmes
movie_titles = call_list()

# URL base do rotten tomatoes
base_url = "https://www.rottentomatoes.com/m/"

count = 0

exeptions = {'Percy_Jackson_&_the_Olympians:_Lightning_Thief': '0814255', 'Repo_Men': '10012068-repo_men',
             'Shutter_Island': '1198124-shutter_island', 'Green_Zone': '1202804-green_zone',
             'Kick_Ass': '1217700-kick_ass', 'Océans': 'disneynature_oceans',
             'Get_Him_to_the_Greek': '1212410-get_him_to_the_greek',
             'Lottery_Ticket': '10012039-lottery_ticket', 'Town': 'the_town',
             'Legend_of_the_Guardians:_Owls_of_GaHoole': 'legend_of_the_guardians',
             'Chronicles_of_Narnia:_Voyage_of_the_Dawn_Treader': 'chronicles_of_narnia_the_voyage_of_the_dawn_treader',
             'Life_as_We_Know_It': '10012044-life_as_we_know_it', 'Furry_Vengeance': '1212891-furry_vengeance',
             'The_Last_Song': '10011984-last_song', 'Edge_of_Darkness_2010': 'Edge_of_Darkness',
             'When_in_Rome_2010': 'When_in_Rome', 'Going_the_Distance_2010': 'Going_the_Distance',
             'Cats_&_Dogs:_Revenge_of_Kitty_Galore': 'cats_and_dogs_the_revenge_of_kitty_galore'}

movie_analyses = pd.DataFrame({
    "Movie_Name": [],
    "Author_Review": [],
    "Polarity": [],
    "Text": [],
    "Score": [],
    "Full_Review": [],
})

movie_detail = pd.DataFrame({
    "Title": [],
    "Genre": [],
    "Duration": [],
    "Year": [],
    "Critics_Consensus": [],
    "Consesus_Polarity": [],
    "Director": [],
    "Tomatometer_Score": [],
    "Tomatometer_State": [],
    "Audience_State": [],
    "Audience_Score": [],
    "Image": [],
})

movie_cast = pd.DataFrame({
    "Title": [],
    "image": [],
    "Actor": [],
    "Chrater": []
})

# Busca as analises do filme
def analise_search(movie_name, soup):
    global movie_analyses

    reviews = soup.find_all('review-speech-balloon-deprecated', class_="")

    for review in reviews:
        review_text = review.get('reviewquote')
        author_review = review.findChildren('a', class_='critic-name')
        full_review_trated = ''
        auhtor_review_trated = ''
        polarity = 0
        for ar in author_review:
            auhtor_review_trated = ar.text
            auhtor_review_trated = auhtor_review_trated.replace("\n", "")
            auhtor_review_trated = auhtor_review_trated.replace("                            ", "")
            auhtor_review_trated = auhtor_review_trated.replace("                        ", "")

        score_state = review.get('scorestate')
        score = 0
        if score_state == 'fresh':
            score = 1
        else:
            score = 0

        full_review = review.findChildren('a', class_='')
        for freview in full_review:
            full_review_trated = freview.get('href')

        analysis = TextBlob(review_text)
        polarity = analysis.sentiment.polarity

        line = {"Movie_Name": movie_name, "Text": review_text, "Author_Review": auhtor_review_trated, "Score": score,
                "Full_Review": full_review_trated, "Polarity": polarity}
        movie_analyses = movie_analyses._append(line, ignore_index=True)

    return movie_analyses

# Busca o Elenco do filme
def cast_search(movie, soup):
    global movie_cast
    cards = soup.find_all('div', class_="cast-and-crew-item")
    for card in cards:
        img = ""
        actor = ""
        chrater = ""

        images = card.findChildren('img', class_="")
        for image in images:
            img = image.get("src")
            actor = image.get("alt")

        chraters = card.findChildren('p', class_="p--small")
        for char in chraters:
            chrater = char.text
            chrater = chrater.replace("\n", "")
            chrater = chrater.replace("                                                ", "")
            chrater = chrater.replace("                ", "")

        line = {"Title": movie, "Actor": actor, "Chrater": chrater, "image": img}
        movie_cast = movie_cast._append(line, ignore_index=True)
        return movie_cast

# Buscar informações do filme
def details_movie_search(soup):
    global movie_detail
    global movie_cast
    global movie_analyses

    movies = soup.find_all('score-board-deprecated', class_="")
    for movie in movies:
        audience_score = movie.get('audiencescore')
        audience_state = movie.get('audiencestate')
        tomatometer_state = movie.get('tomatometerstate')
        tomatometer_score = movie.get('tomatometerscore')
        infos = movie.findChildren('p', class_='info')
        genre = ""
        year = ""
        duration = ""
        consensus = ""
        img = ""

        movie_name = movie.findChildren('h1', class_='title')
        for m in movie_name:
            movie_name = m.text

        for info in infos:
            info_to_split = info.text
            splited_info = info_to_split.split(',')
            year = splited_info[0]
            genre = splited_info[1]
            duration = splited_info[2]


        critics_consensus = soup.find_all('div', class_="consensus-wrap")
        for critic in critics_consensus:
            cs = critic.findChildren('span', class_="")
            for c in cs:
                consensus = c.text


        images = soup.find_all('div', class_="movie-thumbnail-wrap")
        for image in images:
            pics = image.findChildren('rt-img', class_="")
            for pic in pics:
                img = pic.get('src')

        analysis = TextBlob(consensus)
        consesus_polarity = analysis.sentiment.polarity

        line = {"Title": movie_name, "Audience_Score": audience_score, "Audience_State": audience_state,
                "Tomatometer_State": tomatometer_state, "Tomatometer_Score": tomatometer_score, "Genre": genre,
                "Duration": duration, "Year": year, "Critics_Consensus": consensus, "Image": img,
                "Consesus_Polarity": consesus_polarity}
        movie_detail = movie_detail._append(line, ignore_index=True)
        return line

def movies_analises():
    global base_url

    for title in movie_titles:

        # Verifica se está na lista de exceção
        if exeptions.__contains__(title):
            id = exeptions[title]
            url = base_url + id
        else:
            url = base_url + title

        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Busca as informações do filme
            movie = details_movie_search(soup)
            movie_name = movie["Title"]

            # Buscar elenco
            cast_search(movie_name, soup)

            # Buscar o review
            analise_search(movie_name, soup)

        else:
            global count
            count += 1
            print(title, count)
            print("Falha, status: {}".format(response.status_code))

    print(len(movie_analyses), len(movie_detail), len(movie_cast))
    return {"movie_analyses": movie_analyses, "movie_detail": movie_detail, "movie_cast": movie_cast}



# movies_analises()
# print(len(movie_analyses), len(movie_detail), len(movie_cast))