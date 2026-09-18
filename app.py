from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'សូមបញ្ចូល Link YouTube!'}), 400

    # កែប្រែត្រង់នេះដើម្បីកុំឱ្យ YouTube Block IP របស់ Render
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'មិនស្គាល់ចំណងជើង')
            thumbnail = info.get('thumbnail', '')
            
            audio_url = None
            for fmt in info.get('formats', []):
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
        return jsonify({'error': 'មិនអាចបំប្លែង Link នេះបានទេ! សូមសាកល្បងប្រើ Link ពេញ (https://www.youtube.com/watch?v=...)'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                audio_url = info.get('url')

            return jsonify({
                'title': title,
                'thumbnail': thumbnail,
                'download_url': audio_url
            })
    except Exception as e:
        return jsonify({'error': 'មិនអាចបំប្លែង Link នេះបានទេ! សូមពិនិត្យ Link ឡើងវិញ។'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
