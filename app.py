from flask import Flask, request, render_template, send_file, jsonify, url_for
from pytube import YouTube
from pydub import AudioSegment
import os
import uuid
import time

app = Flask(__name__)

# Carpeta de descargas temporales
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    try:
        youtube_url = request.json.get("youtube_url")
        if not youtube_url:
            return jsonify({"error": "Por favor, ingresa un enlace válido."}), 400

        # Descargar el video de YouTube
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        temp_audio_path = audio_stream.download(output_path=DOWNLOAD_FOLDER)

        # Simular progreso (puedes ajustar según el tiempo real)
        for i in range(1, 6):
            time.sleep(0.5)  # Simula el tiempo de procesamiento
            yield f"data: {i * 20}\n\n"

        # Convertir a formato MP3
        mp3_filename = f"{uuid.uuid4()}.mp3"
        mp3_path = os.path.join(DOWNLOAD_FOLDER, mp3_filename)

        audio = AudioSegment.from_file(temp_audio_path)
        audio.export(mp3_path, format="mp3")
        os.remove(temp_audio_path)

        # Devolver la URL de descarga
        return jsonify({"download_url": url_for("download_file", filename=mp3_filename)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
