import re
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEY = "119b572848mshd141b98e8696c31p179d35jsnb1b213585552"
API_HOST = "youtube-mp3-audio-video-downloader.p.rapidapi.com"

def extract_video_id(url):
    # ស្រង់យក Video ID 11 ខ្ទង់ចេញពី Link
    match = re.search(r'(?:v=|\/|vi=|\/v\/|shorts\/|youtu\.be\/)([0-9A-Za-z_-]{11})', url)
    return match.group(1) if match else None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.get_json() or {}
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'សូមបញ្ចូល Link YouTube!'}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'Link YouTube មិនត្រឹមត្រូវទេ!'}), 400

    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }

    try:
        api_url = f"https://{API_HOST}/language_list/{video_id}?response_mode=default"
        response = requests.get(api_url, headers=headers, timeout=12)
        
        # ប្រសិនបើ RapidAPI ឆ្លើយតបមកមិនមែន Success (Status Code != 200)
        if response.status_code != 200:
            return jsonify({'error': f'RapidAPI Error ({response.status_code}): {response.text}'}), 500

        res_data = response.json()

        title = res_data.get('title', 'YouTube MP3 Audio')
        thumbnail = res_data.get('thumbnail', f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg")
        
        # ទាញយក Link MP3
        download_url = res_data.get('link') or res_data.get('download_url') or res_data.get('url')

        if not download_url:
            return jsonify({'error': f'RapidAPI មិនមាន Link ទាញយកទេ៖ {res_data}'}), 500

        return jsonify({
            'title': title,
            'thumbnail': thumbnail,
            'download_url': download_url
        })

    except Exception as e:
        # បង្ហាញ Error លម្អិតដើម្បីងាយស្រួលដោះស្រាយ
        return jsonify({'error': f'ការភ្ជាប់មានបញ្ហា៖ {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
