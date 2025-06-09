from flask import Flask, request, send_file, render_template
from yt_dlp import YoutubeDL
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return "No URL provided", 400

    ydl_opts = {
        'format': 'mp4',
        'quiet': True,
        'outtmpl': '-',
        'noplaylist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']
            response = requests.get(video_url, stream=True)
            if response.status_code != 200:
                return "Failed to download", 400

            return send_file(BytesIO(response.content),
                             as_attachment=True,
                             download_name='tiktok_video.mp4',
                             mimetype='video/mp4')
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))