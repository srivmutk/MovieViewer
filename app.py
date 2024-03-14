import json
import os
import subprocess
from quart import Quart, render_template, Response
from dotenv import load_dotenv

from update import update_movies

app = Quart(__name__)

load_dotenv(override=True)

@app.route("/")
async def index():
    movie_data_json = json.load(open('movies.json'))
    
    return await render_template("index.html", data=movie_data_json)

@app.route("/update")
def update():
    try:
        update_movies()
    except Exception as e:
        return Response(f"Error in updating library", status=500, mimetype='application/json')

    return Response(f"Update of library sucessful", status=200, mimetype='application/json')


@app.route("/watch/<path:filename>")
async def watch(filename: str):
    try:
        print(filename.replace("/", "\\"))
        subprocess.Popen(
            ["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe", filename.replace("/", "\\")]
        )

    except Exception as e:
        return Response(f"Error in opening {filename}", status=500, mimetype='application/json')


    return Response(f"Watching {os.path.basename(filename).split('/')[-1]}", status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)
