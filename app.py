import re
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEY = "119b572848mshd141b98e8696c31p179d35jsnb1b213585552"
API_HOST = "youtube-mp3-audio-video-downloader.p.rapidapi.com"

def extract_video_id(url):
    # ទាញយក Video ID ចេញពី YouTube Link គ្រប់ទម្រង់
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    return match.group(1) if match else None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.get_json()
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
        # ហៅទៅកាន់ RapidAPI
        api_url = f"https://{API_HOST}/language_list/{video_id}?response_mode=default"
        response = requests.get(api_url, headers=headers)
        res_data = response.json()

        # ទាញយកព័ត៌មានចេញពី API Response
        title = res_data.get('title', 'YouTube MP3 Audio')
        thumbnail = res_data.get('thumbnail', f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg")
        
        # ស្រង់យក Link សម្រាប់ Download
        download_url = res_data.get('link') or res_data.get('download_url') or res_data.get('url')

        if not download_url:
            return jsonify({'error': 'មិនអាចទាញយក Link MP3 បានទេ! សូមពិនិត្យ Endpoint របស់ RapidAPI ឡើងវិញ។'}), 500

        return jsonify({
            'title': title,
            'thumbnail': thumbnail,
            'download_url': download_url
        })

    except Exception as e:
        return jsonify({'error': 'មានបញ្ហាក្នុងការភ្ជាប់ទៅកាន់ RapidAPI!'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                    audio_url = fmt.get('url')
                    break
            if not audio_url:
                audio_url = info.get('url')

            return jsonify({
                'title': title,
                'thumbnail': thumbnail,
                'download_url': audio_url
            })
    except Exception as e:
        return jsonify({'error': 'មិនអាចបំប្លែង Link នេះបានទេ! សូមសាកល្បងម្ដងទៀត។'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
