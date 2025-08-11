from flask import Flask, request, jsonify
import yt_dlp
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "YT-DLP API is running"})

@app.route("/video", methods=["GET"])
def get_video_info():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        # Create a temporary cookies.txt file from environment variable
        cookies_env = os.environ.get("COOKIES", "")
        cookies_file = None
        if cookies_env.strip():
            temp_dir = tempfile.mkdtemp()
            cookies_file = os.path.join(temp_dir, "cookies.txt")
            with open(cookies_file, "w", encoding="utf-8") as f:
                f.write(cookies_env)

        # yt-dlp options
        ydl_opts = {
            "cookiefile": cookies_file if cookies_file else None,
            "quiet": True,
            "nocheckcertificate": True,
            "ignoreerrors": True,
            "dump_single_json": True,
            "writesubtitles": False,
            "noplaylist": True,
            "format": "bestvideo+bestaudio/best"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        if not info:
            return jsonify({"error": "Could not extract video info"}), 500

        return jsonify(info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
