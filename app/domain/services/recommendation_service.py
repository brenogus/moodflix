from app.domain.entities.movie import Movie

def recommend_by_genre(genre: str):
    data = {
        "acao": [
            Movie("Mad Max","acao",8.2), 
            Movie("Jhon Wick","acao",7.9)
                 ],
       
        "ficcao": [
            Movie("Interestelar","ficcao",8.6), 
            Movie("Matrix","ficcao",8.7)
            ],
            
        "comedia": [
            Movie("Superbad", "comedia", 7.5), 
            Movie("Se beber não case", "comedia", 7.8)
            ]
    }

    return data.get(genre.lower(),[])

    