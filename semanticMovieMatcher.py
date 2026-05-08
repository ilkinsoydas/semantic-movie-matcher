import pandas as pd
import numpy as np
import pickle
from nltk.stem.porter import PorterStemmer



movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

movies = movies.merge(credits, on = "title")
print("Tablonun boyutu: ", movies.shape)
print(movies.head(1))   

movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.head(1)

import ast

def convert(text):
    if isinstance(text, list):
        return text
        
    if not isinstance(text, str):
        return []
        
    clean_list = []
    real_list = ast.literal_eval(text) #ast, Abstract Syntax Tree
    
    for i in real_list:
        clean_list.append(i["name"])
        
    return clean_list

movies['genres'] = movies['genres'].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)

def convert3(text):
    if isinstance(text, list):
        return text
    if not isinstance(text, str):
        return []

    clean_list = []
    real_list = ast.literal_eval(text)

    for i in real_list:
        clean_list.append(i["name"])
        if len(clean_list) == 3:
            break
    return clean_list

movies["cast"] = movies["cast"].apply(convert3)

def fetch_director(text):
    if isinstance(text, list):
        return text
    if not isinstance(text, str):
        return []
    
    clean_list = []
    real_list = ast.literal_eval(text)
    
    for i in real_list:
        if i["job"] == "Director":
            clean_list.append(i["name"])
            
    return clean_list

movies["crew"] = movies["crew"].apply(fetch_director)

""" 
Şu anki sorunumuz model kelimeleri boşlukları keserek okur. Örneğin elinde Johnny Deep ve Jonny Cash
varsa, model bu iki filmi ikisinde de Johnny geçtiği için benzetme yapar ve hatalı bir bağ kurar.
Bu isimleri JohnnyDeep şeklinde birleştirip yeni benzersiz bir tag haline getirmeliyiz. Bu türler için
de geçerlidir. Bunun için de "replace" fonksiyonunu kullanmalıyız.
"""

def remove_spaces(word_list):
    clean_list = []
    
    for i in word_list:
        clean_list.append(i.replace(" ", ""))
    return clean_list

movies["genres"] = movies["genres"].apply(remove_spaces)
movies["keywords"] = movies["keywords"].apply(remove_spaces)
movies["cast"] = movies["cast"].apply(remove_spaces)
movies["crew"] = movies["crew"].apply(remove_spaces)


movies["overview"] = movies["overview"].apply(lambda x: x.split() if isinstance(x, str) else [])
print(movies.head(2))

movies["tags"] = movies["overview"] + movies["genres"] + movies["keywords"] + movies["cast"] + movies["crew"]

new_df = movies[["movie_id", "title", "tags"]]
print(new_df.head(1))

new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x) if isinstance(x, list) else "")

ps = PorterStemmer()
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())
new_df["tags"] = new_df["tags"].apply(stem) #kelimeleri köklerine ayır

#movie_id ve title bizim referans noktalarımız, model sadece tags üzerinden benzetme yapacak

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words="english") #en fazla tekrar eden 5000 kelime alır, ingilizce stop word'leri çıkarır
vectors = cv.fit_transform(new_df["tags"]).toarray()
print(vectors.shape)


from sklearn.metrics.pairwise import cosine_similarity #iki veri arasındaki benzerliği ölçmek için kullanılan bir matematik formülü
similarity = cosine_similarity(vectors) #benzerlik haritası yarattık
print(similarity.shape)


def recommend(movie):
    movie_index = new_df[new_df["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6] #reverse=true büyükten küçüğe
    #enumarate sayesinde (x,y)-> x. satırdaki film %y benziyor
    
    print(f"\n '{movie}' sevenler bunları da sevdi: \n")
    for i in movie_list:
        print(f"{new_df.iloc[i[0]].title} -> benzerlik puanı: {i[1]:.4f}") #iloc ile satıra gidip .title ismini çekeriz

recommend("Pulp Fiction")
recommend("Avatar")


pickle.dump(new_df, open("movie_dict.pkl", "wb")) #wb->write binary, 0-1ler ile
pickle.dump(similarity, open("similarity.pkl", "wb"))

        







