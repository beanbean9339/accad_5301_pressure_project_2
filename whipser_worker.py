
import os
import time
import glob
import whisper
import numpy as np

WORK_DIR = (
    r"C:\Users\beanb\Desktop\TouchDesigner Projects"
    r"\accad 5301\pressure_project2_IL\td_whisper_stream"
)

OUTPUT_FILE = os.path.join(WORK_DIR, "transcript.txt")
TEMP_FILE = os.path.join(WORK_DIR, "transcript.tmp")

MODEL_NAME = "base.en"
MIN_AUDIO_RMS = 0.001

os.makedirs(WORK_DIR, exist_ok=True)

# Clear old audio chunks and captions when starting.
for pattern in ("chunk_*.wav", "transcript.txt", "transcript.tmp"):
    for path in glob.glob(os.path.join(WORK_DIR, pattern)):
        try:
            os.remove(path)
        except OSError as e:
            print(f"Could not remove {path}: {e}", flush=True)

print(f"Loading Whisper {MODEL_NAME} model...", flush=True)
model = whisper.load_model(MODEL_NAME)

print("Whisper ready. Waiting for microphone audio...", flush=True)


def save_transcript(text):
    """Write the latest caption on one line."""
    text = " ".join(text.split())

    with open(TEMP_FILE, "w", encoding="utf-8") as f:
        f.write(text)

    for _ in range(10):
        try:
            os.replace(TEMP_FILE, OUTPUT_FILE)
            return True
        except PermissionError:
            time.sleep(0.1)

    print("Could not update transcript.txt", flush=True)
    return False


# Keep listening until manually stopped.
while True:
    chunks = sorted(
        glob.glob(os.path.join(WORK_DIR, "chunk_*.wav"))
    )

    if not chunks:
        time.sleep(0.1)
        continue

    for audio_path in chunks:
        try:
            if not os.path.exists(audio_path):
                continue

            print(
                "Transcribing:",
                os.path.basename(audio_path),
                flush=True
            )

            audio = whisper.load_audio(audio_path)
            rms = float(np.sqrt(np.mean(audio ** 2)))

            print(f"Audio RMS: {rms:.6f}", flush=True)

            if rms < MIN_AUDIO_RMS:
                print("Skipped quiet audio.", flush=True)
                continue

            result = model.transcribe(
                audio,
                fp16=False,
                language="en",
                task="transcribe",
                temperature=0,
                condition_on_previous_text=False,
                no_speech_threshold=0.6,
                logprob_threshold=-1.0,
                compression_ratio_threshold=2.4,
                verbose=False
            )

            segments = result.get("segments", [])
            text = result.get("text", "").strip()

            # Reject captions when all segments are classified as silence.
            if segments and all(
                seg.get("no_speech_prob", 0) > 0.6
                for seg in segments
            ):
                text = ""

            if text:
                if save_transcript(text):
                    print("Recognized:", text, flush=True)

        except Exception as e:
            print(f"Transcription error: {e}", flush=True)

        finally:
            try:
                os.remove(audio_path)
            except OSError as e:
                print(f"Could not delete WAV: {e}", flush=True)
