from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from pytube import YouTube
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(DOWNLOAD_FOLDER)
        filename = video.default_filename
        return redirect(url_for('download_file', filename=filename))
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

