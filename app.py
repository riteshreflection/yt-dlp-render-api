from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/extract", methods=["POST"])
def extract():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing 'url'"}), 400

    opts = {
        "quiet": True,
        "skip_download": True,
        "format": "best",
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get("title"),
                "url": info.get("url"),
                "ext": info.get("ext"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail")
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
