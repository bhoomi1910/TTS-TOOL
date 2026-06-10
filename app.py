from flask import Flask, render_template, request, jsonify, send_from_directory
import edge_tts
import asyncio
import os
import uuid

app = Flask(__name__)

VOICE_MAP = {

    "Female 1": "en-US-JennyNeural",
    "Female 2": "en-US-AriaNeural",
    "Female 3": "en-GB-SoniaNeural",
    "Female 4": "en-AU-NatashaNeural",
    "Female 5": "en-CA-ClaraNeural",
    "Female 6": "en-IN-NeerjaNeural",
    "Female 7": "en-US-AnaNeural",

    "Male 1": "en-US-GuyNeural",
    "Male 2": "en-GB-RyanNeural",
    "Male 3": "en-AU-WilliamNeural",
    "Male 4": "en-CA-LiamNeural",
    "Male 5": "en-IN-PrabhatNeural",
    "Male 6": "en-US-ChristopherNeural",
    "Male 7": "en-US-BrandonNeural",
    "Male 8": "en-GB-ThomasNeural"
}

@app.route("/")
def home():

    return render_template(
        "index.html",
        voices=VOICE_MAP.keys()
    )

@app.route("/generate", methods=["POST"])
def generate():

    try:

        text = request.form["text"]

        voice = request.form["voice"]

        speed = request.form["speed"]

        pitch = request.form["pitch"]

        voice_id = VOICE_MAP[voice]

        unique_name = f"{uuid.uuid4()}.mp3"

        output_file = os.path.join(
            "static",
            unique_name
        )

        async def save_audio():

            communicate = edge_tts.Communicate(
                text=text,
                voice=voice_id,
                rate=speed,
                pitch=pitch
            )

            await communicate.save(output_file)

        asyncio.run(save_audio())

        return jsonify({
            "success": True,
            "audio_url": f"/audio/{unique_name}"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/audio/<filename>")
def audio(filename):

    return send_from_directory(
        "static",
        filename
    )

app.run(debug=True)