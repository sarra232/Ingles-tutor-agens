import http.server
import socketserver
import json
import io
import os
import time
import base64
import asyncio
import urllib.request
import urllib.error
import urllib.parse
import speech_recognition as sr
try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

PORT = 8090
VOZ_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(VOZ_DIR, "..", ".."))
LIVE_STATE_PATH = os.path.join(VOZ_DIR, "live_state.json")
INBOX_PATH = os.path.join(VOZ_DIR, "student_inbox.json")
HISTORY_PATH = os.path.join(VOZ_DIR, "chat_history.json")
ENV_PATH = os.path.join(ROOT_DIR, ".env")


def load_api_key():
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"].strip()
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def save_api_key(key_str):
    key_str = key_str.strip()
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write(f"GEMINI_API_KEY={key_str}\n")
    os.environ["GEMINI_API_KEY"] = key_str


def read_context_files():
    ctx_parts = []
    for rel in ["context/profile.md", "context/progress.md", "context/weaknesses-and-mistakes.md"]:
        p = os.path.join(ROOT_DIR, rel)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                ctx_parts.append(f"=== {rel} ===\n" + f.read())
    return "\n\n".join(ctx_parts)


def load_chat_history():
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_chat_history(history):
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history[-20:], f, ensure_ascii=False, indent=2)


SYSTEM_PROMPT_TEMPLATE = """You are Alex, a chill, direct, and natural English-speaking teammate and tutor for Wilson (Orus), a 32-year-old Systems Engineer and Java Developer living near Medellín, Colombia.

Here is Wilson's live persistent student context from the repository:
{student_context}

STRICT TONE & PERSONALITY RULES (CRITICAL):
1. Be informal, concise, direct, and human—like a real coworker on a call, NOT a robotic or overly enthusiastic teacher.
2. NEVER over-praise or use exaggerated compliments (NO "That is fantastic!", "Amazing job!", "Spot on!", "Like a true pro!").
3. If Wilson says something right, just say a quick, natural "Good job, let's move on to the next one" or "Nice, that sounded clear. Next up: ..." and immediately continue.
4. If Wilson makes a mistake (grammar, word choice, or pronunciation), point it out directly and briefly without sugarcoating: tell him what he said, how to say it naturally, and make him practice that point in the next turn.
5. Keep your spoken responses (`tutorMessage.en`) short and conversational (1 to 2 sentences max) so the audio flows fast.

YOUR CAPABILITIES IN THE REACT STUDIO:
You control a live React Multimedia Studio with 3 interactive boards:
1. "slides": Visual Slide Deck with custom AI images, English model sentences, IPA pronunciation, Spanish translation, and 3 clickable expression cards.
2. "game": Interactive Sentence Builder & Voice Challenge (sentences scrambled into blocks).
3. "video": Interactive Scene / Dialogue Script (line-by-line roleplay between Alex and Wilson).

INSTRUCTIONS FOR EVERY TURN:
1. If Wilson sent audio, listen to his pronunciation and grammar. Transcribe what he said in `heardText` and rate it 0-100 in `pronunciationScore`.
2. In `feedback`, be direct and brief (`said`, `naturalEnglish`, `explanationEs`). If there was no error, keep `explanationEs` to 4-5 words max (e.g., "Bien dicho, sigamos.").
3. Write your short, casual spoken reply in `tutorMessage` (`en`, `es`, `speaker`: "Alex", `avatar`: "🧑‍💻", `autoSpeak`: true).
4. If Wilson asks for slides, images, a new topic, a game, or a dialogue:
   - Set `activeTab` to `"slides"`, `"game"`, or `"video"` (or `"keep"` if no tab switch is needed).
   - For custom slide images, use: `https://image.pollinations.ai/prompt/<URL_ENCODED_ENGLISH_VISUAL_DESCRIPTION>?width=1000&height=500&nologo=true`
   - Populate `newSlides`, `newGames`, or `newVideoLesson` only when creating new content.

Respond ONLY with a valid JSON object matching this exact structure:
{{
  "heardText": "string (what Wilson said or wrote)",
  "pronunciationScore": 90,
  "feedback": {{
    "hasCorrection": true,
    "said": "what Wilson said",
    "naturalEnglish": "corrected natural version",
    "explanationEs": "explicación directa y corta en español"
  }},
  "tutorMessage": {{
    "speaker": "Alex",
    "avatar": "🧑‍💻",
    "en": "Short, casual, human response in English...",
    "es": "Traducción corta en español...",
    "autoSpeak": true
  }},
  "activeTab": "keep",
  "newSlides": null,
  "newGames": null,
  "newVideoLesson": null
}}
"""


def call_gemini_multimodal(api_key, user_text="", audio_wav_bytes=None):
    student_context = read_context_files()
    sys_instruction = SYSTEM_PROMPT_TEMPLATE.format(student_context=student_context)
    history = load_chat_history()

    parts = []
    if audio_wav_bytes:
        b64_audio = base64.b64encode(audio_wav_bytes).decode("ascii")
        parts.append({
            "inline_data": {
                "mime_type": "audio/wav",
                "data": b64_audio
            }
        })
        parts.append({
            "text": "Listen to Wilson's spoken voice audio above. Transcribe what he said, evaluate his English pronunciation and grammar, respond naturally in English, and update the visual slides/games/video if helpful." + (f" Additional note from Wilson: {user_text}" if user_text else "")
        })
    else:
        parts.append({
            "text": f"Wilson says/requests: {user_text}"
        })

    # Incluir últimos turnos de conversación para memoria continua
    contents = []
    for h in history[-6:]:
        contents.append({
            "role": "user" if h["role"] == "user" else "model",
            "parts": [{"text": h["text"]}]
        })
    contents.append({"role": "user", "parts": parts})

    payload = {
        "system_instruction": {
            "parts": [{"text": sys_instruction}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.6,
            "responseMimeType": "application/json"
        }
    }

    models_to_try = [
        "gemini-flash-lite-latest",
        "gemini-3.8-flash",
        "gemini-flash-latest"
    ]
    raw = None
    last_err = None
    for model_name in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={urllib.parse.quote(api_key)}"
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=35) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
                break
        except Exception as e:
            last_err = e
            continue

    if raw is None:
        raise last_err

    text_resp = raw["candidates"][0]["content"]["parts"][0]["text"]
    ai_data = json.loads(text_resp)

    # Guardar en el historial y actualizar live_state.json
    heard = ai_data.get("heardText") or user_text or "(Audio)"
    history.append({
        "role": "user",
        "text": heard,
        "timestamp": time.strftime("%H:%M")
    })
    history.append({
        "role": "model",
        "text": ai_data.get("tutorMessage", {}).get("en", ""),
        "es": ai_data.get("tutorMessage", {}).get("es", ""),
        "feedback": ai_data.get("feedback"),
        "score": ai_data.get("pronunciationScore"),
        "timestamp": time.strftime("%H:%M")
    })
    save_chat_history(history)

    # Actualizar live_state.json si Gemini generó nuevas diapositivas, juegos o escena
    if os.path.exists(LIVE_STATE_PATH):
        with open(LIVE_STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {"version": 100}

    state["version"] = int(time.time() * 10)
    if ai_data.get("tutorMessage"):
        state["tutorMessage"] = ai_data["tutorMessage"]
    if ai_data.get("feedback"):
        state["lastFeedback"] = ai_data["feedback"]
    if ai_data.get("pronunciationScore") is not None:
        state["lastScore"] = ai_data["pronunciationScore"]
    if ai_data.get("activeTab") in ("slides", "game", "video"):
        state["activeTab"] = ai_data["activeTab"]

    # Normalizar newSlides solo si vienen completas con imagen y en/es
    if isinstance(ai_data.get("newSlides"), list) and len(ai_data["newSlides"]) > 0:
        valid_slides = []
        for idx, s in enumerate(ai_data["newSlides"]):
            if isinstance(s, dict) and s.get("en"):
                valid_slides.append({
                    "id": s.get("id") or f"s-{idx+1}",
                    "badge": s.get("badge") or "Interactive Slide",
                    "title": s.get("title") or "Visual Lesson",
                    "image": s.get("image") or "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=80",
                    "imageCaption": s.get("imageCaption") or "",
                    "en": s.get("en") or "",
                    "ipa": s.get("ipa") or "",
                    "es": s.get("es") or "",
                    "highlights": s.get("highlights") if isinstance(s.get("highlights"), list) else []
                })
        if valid_slides:
            state["slides"] = valid_slides
            state["activeTab"] = "slides"

    # Normalizar newGames para evitar errores en React si Gemini cambia algún nombre de campo
    if isinstance(ai_data.get("newGames"), list) and len(ai_data["newGames"]) > 0:
        valid_games = []
        for idx, g in enumerate(ai_data["newGames"]):
            if isinstance(g, dict):
                target_en = g.get("targetEn") or (" ".join(g["correctOrder"]) if isinstance(g.get("correctOrder"), list) else "")
                scrambled = g.get("scrambled") or g.get("scrambledBlocks") or (target_en.split(" ") if target_en else [])
                if target_en and scrambled:
                    valid_games.append({
                        "id": g.get("id") or f"g-{idx+1}",
                        "promptEs": g.get("promptEs") or g.get("instruction") or "Arma la frase en inglés:",
                        "targetEn": target_en,
                        "scrambled": [str(x) for x in scrambled],
                        "tip": g.get("tip") or "Recuerda el orden: Subject + Verb + Object + Place + Time."
                    })
        if valid_games:
            state["gameChallenges"] = valid_games
            state["activeTab"] = "game"

    if isinstance(ai_data.get("newVideoLesson"), dict) and ai_data["newVideoLesson"].get("script"):
        state["videoLesson"] = ai_data["newVideoLesson"]
        state["activeTab"] = "video"

    with open(LIVE_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    return ai_data, state, history


class VoiceStudioHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)

    def log_message(self, format, *args):
        first_arg = str(args[0]) if args else ""
        if "/live_state" in first_arg or "/api_status" in first_arg:
            return
        super().log_message(format, *args)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/live_state"):
            if os.path.exists(LIVE_STATE_PATH):
                with open(LIVE_STATE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["history"] = load_chat_history()[-10:]
                self._send_json(200, data)
            else:
                self._send_json(200, {"version": 0})
            return

        if self.path.startswith("/api_status"):
            k = load_api_key()
            masked = (k[:6] + "..." + k[-4:]) if len(k) > 10 else ""
            self._send_json(200, {"hasKey": bool(k), "maskedKey": masked})
            return

        if self.path.startswith("/tts"):
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            text = (qs.get("text", [""])[0] or "").strip()
            voice = (qs.get("voice", ["en-US-JennyNeural"])[0] or "en-US-JennyNeural").strip()
            if not text:
                self.send_error(400, "Empty text")
                return

            mp3_bytes = b""
            if HAS_EDGE_TTS:
                try:
                    async def _gen():
                        comm = edge_tts.Communicate(text, voice)
                        buf = io.BytesIO()
                        async for chunk in comm.stream():
                            if chunk["type"] == "audio":
                                buf.write(chunk["data"])
                        return buf.getvalue()
                    mp3_bytes = asyncio.run(_gen())
                except Exception:
                    mp3_bytes = b""

            if not mp3_bytes:
                try:
                    g_url = "https://translate.googleapis.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q=" + urllib.parse.quote(text[:200])
                    req = urllib.request.Request(g_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=10) as r:
                        mp3_bytes = r.read()
                except Exception as e:
                    self.send_error(500, str(e))
                    return

            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Content-Length", str(len(mp3_bytes)))
            self.end_headers()
            self.wfile.write(mp3_bytes)
            return

        super().do_GET()

    def do_POST(self):
        if self.path == "/save_api_key":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            key = body.get("apiKey", "").strip()
            if not key:
                self._send_json(400, {"ok": False, "error": "API Key vacía"})
                return
            save_api_key(key)
            self._send_json(200, {"ok": True, "maskedKey": key[:6] + "..." + key[-4:]})
            return

        if self.path == "/ai_turn":
            api_key = load_api_key()
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            user_text = body.get("text", "").strip()
            audio_b64 = body.get("audioWavBase64", "")
            audio_bytes = base64.b64decode(audio_b64) if audio_b64 else None

            # Si aún no hay API Key de Google AI Studio, usamos el transcriptor local gratuito y avisamos
            if not api_key:
                if audio_bytes:
                    r = sr.Recognizer()
                    try:
                        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                            audio_data = r.record(source)
                        spoken = r.recognize_google(audio_data, language="en-US")
                        self._send_json(200, {
                            "ok": True,
                            "mode": "local_stt_only",
                            "heardText": spoken,
                            "message": "Voz transcrita. Configura tu GEMINI_API_KEY arriba para que Google AI Studio te responda y cree diapositivas/juegos automáticamente."
                        })
                    except Exception as e:
                        self._send_json(200, {"ok": False, "error": str(e)})
                else:
                    self._send_json(200, {"ok": False, "needsKey": True, "error": "Haz clic en '🔑 Conectar Google AI Studio' arriba a la derecha y pega tu API Key gratuita."})
                return

            try:
                ai_data, new_state, history = call_gemini_multimodal(api_key, user_text=user_text, audio_wav_bytes=audio_bytes)
                self._send_json(200, {
                    "ok": True,
                    "mode": "gemini_live",
                    "ai": ai_data,
                    "state": new_state,
                    "history": history[-10:]
                })
            except urllib.error.HTTPError as he:
                err_body = he.read().decode("utf-8", errors="ignore")
                self._send_json(200, {"ok": False, "error": f"Error de Google AI Studio ({he.code}): {err_body[:300]}"})
            except Exception as e:
                self._send_json(200, {"ok": False, "error": str(e)})
            return

        if self.path == "/transcribe":
            length = int(self.headers.get("Content-Length", 0))
            wav_bytes = self.rfile.read(length)
            r = sr.Recognizer()
            try:
                with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
                    audio_data = r.record(source)
                text = r.recognize_google(audio_data, language="en-US")
                self._send_json(200, {"ok": True, "text": text})
            except sr.UnknownValueError:
                self._send_json(200, {"ok": False, "error": "No se detectaron palabras claras en inglés. Habla un poco más cerca del micrófono."})
            except Exception as e:
                self._send_json(200, {"ok": False, "error": str(e)})
            return

        if self.path == "/student_reply":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            body["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(INBOX_PATH, "w", encoding="utf-8") as f:
                json.dump(body, f, ensure_ascii=False, indent=2)
            self._send_json(200, {"ok": True})
            return

        self.send_error(404, "Not Found")

    def _send_json(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), VoiceStudioHandler) as httpd:
        print(f"Orus React Live Studio + Google AI Studio running on http://localhost:{PORT}")
        httpd.serve_forever()
