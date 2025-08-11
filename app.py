from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "YT-DLP API is running"})

@app.route("/video", methods=["GET"])
def video_get():
    yt_url = request.args.get("url")
    if not yt_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "format": "bestaudio*+bestvideo*",
        "extract_flat": False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=False)
        # Send **full raw JSON** from yt-dlp
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
