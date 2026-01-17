import os
from flask import Flask, jsonify, request
import yt_dlp

app = Flask(__name__)

@app.route('/get_stream')
def get_stream():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"success": False, "error": "Missing video id"}), 400

    ydl_opts = {
        'format': 'best', # yt-dlp automatically picks the best manifest for live
        'quiet': True,
        'cookiefile': 'cookies.txt', # Must be Netscape format in your repo
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            url = f"https://www.youtube.com/watch?v={video_id}"
            info = ydl.extract_info(url, download=False)
            
            # Identify if it's a live stream
            is_live = info.get('is_live', False)
            
            return jsonify({
                "success": True,
                "stream_url": info.get('url'),
                "title": info.get('title'),
                "is_live": is_live,
                "thumbnail": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
