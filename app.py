import pickle

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

print("Sistem hazır")