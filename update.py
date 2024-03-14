import json
import os
from pathlib import Path
import guessit
import httpx
from dotenv import load_dotenv

def update_movies():
    movie_paths = []
    movie_data = []

    load_dotenv(override = True)

    root_paths_json = json.load(open("config.json"))
    ROOT_PATHS = root_paths_json["movie_paths"]
    API_KEY = os.getenv("OMDB_API_KEY")

    for ROOT_PATH in ROOT_PATHS:
        for root, dirs, files in os.walk(ROOT_PATH):
            for name in files:
                file_string = os.path.join(root, name)

                if (((str(ROOT_PATH) == str(Path(file_string).parents[1]) and
                    str(file_string).lower().endswith(('.mp4', '.mkv'))) and
                    str(Path(file_string).stem) != "sample") and str(Path(file_string).stem) != "Sample" and
                        str(Path(file_string).stem) != "trailer"):
                    movie_paths.append(
                        file_string
                    )

    for movie_path in movie_paths:
        movie_results = {}
        info_json_path = str(Path(movie_path).parents[0]) + "\\info.json"

        if os.path.isfile(info_json_path):
            f = open(info_json_path)
            info_json = json.load(f)
            movie_results.update(info_json)
        else:
            movie_guess = guessit.guessit(movie_path, {'type': 'movie'})
            result = httpx.get(
                f"https://www.omdbapi.com/?apikey={API_KEY}&t={movie_guess['title']}&y={movie_guess['year']}&type=movie")

            movie_results.update({"Path": movie_path})

            if "edition" in movie_guess:
                movie_results["Edition"] = movie_guess["edition"]
            elif "alternative_title" in movie_guess:
                movie_results["AlternativeTitle"] = movie_guess["alternative_title"]

            if result.json()['Response'] != "False":
                movie_results.update(result.json())
            else:
                result_alt = httpx.get(
                    f"https://www.omdbapi.com/?apikey={API_KEY}&t={movie_guess['title']}&type=movie")

                if result_alt.json()['Response'] != "False":
                    movie_results.update(result_alt.json())
                else:
                    movie_guess.setdefault("edition", "Unknown")
                    movie_guess.setdefault("alternative_title", "Unknown")

                    movie_results.update(
                        {'Title': movie_guess['title'], 'Year': movie_guess['year'], 'Path': movie_path,
                        'Edition': movie_guess["edition"], 'AlternativeTitle': movie_guess["alternative_title"],
                        "Poster": "/static/default_movie.jpg"})

        movie_data.append(movie_results)

        with open(info_json_path, "w") as outfile:
            outfile.write(json.dumps(movie_results, indent=4))

    with open("movies.json", "w") as outfile:
        outfile.write(json.dumps(sorted(movie_data, key=lambda x: x['Title']), indent=4))
