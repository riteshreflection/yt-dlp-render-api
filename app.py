from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/video_info", methods=["POST"])
def video_info():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # yt-dlp options to get full streaming data
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False,  # we want full formats
        "nocheckcertificate": True,
        "geo_bypass": True,
        "format": "bestaudio*+bestvideo*",  # Get both
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)

            # Extract only needed fields + formats
            result = {
                "id": info.get("id"),
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "channel_id": info.get("channel_id"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "upload_date": info.get("upload_date"),
                "view_count": info.get("view_count"),
                "like_count": info.get("like_count"),
                "formats": []
            }

            for f in info.get("formats", []):
                # Keep only fields useful for playback
                result["formats"].append({
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "resolution": f.get("resolution") or f"{f.get('width')}x{f.get('height')}",
                    "fps": f.get("fps"),
                    "filesize": f.get("filesize"),
                    "tbr": f.get("tbr"),  # bitrate
                    "vcodec": f.get("vcodec"),
                    "acodec": f.get("acodec"),
                    "url": f.get("url"),  # Direct playable URL
                    "protocol": f.get("protocol"),
                })

            return jsonify(result)

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "YT-DLP API is running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
