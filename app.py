from flask import Flask, render_template, request, Response
import yt_dlp
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download')
def download():
    video_url = request.args.get('url')
    format_type = request.args.get('format', 'mp4')

    if not video_url:
        return "URL YouTube tidak ditemukan!", 400

    # Konfigurasi yt-dlp untuk mengambil file langsung
    ydl_opts = {
        'format': 'best[ext=mp4]/best' if format_type == 'mp4' else 'bestaudio/best',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            stream_url = info['url']
            title = info.get('title', 'video_youtube').replace('"', '')

        # Alirkan (stream) data langsung dari YouTube ke browser user
        req = requests.get(stream_url, stream=True)
        
        ext = 'mp4' if format_type == 'mp4' else 'mp3'
        headers = {
            'Content-Type': req.headers.get('Content-Type', 'application/octet-stream'),
            'Content-Disposition': f'attachment; filename="{title}.{ext}"'
        }

        return Response(req.iter_content(chunk_size=1024*1024), headers=headers)

    except Exception as e:
        return f"Gagal mengambil video: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
