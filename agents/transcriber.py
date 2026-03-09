import os
import tempfile
from faster_whisper import WhisperModel

# load once (important for speed)
model = WhisperModel("base", compute_type="int8")  # low RAM, CPU friendly


def transcribe(audio_file):
    """
    Accepts:
    - Streamlit UploadedFile
    - file path string
    - raw transcript text (for testing)
    """

    # Case 1: already text (unit testing)
    if isinstance(audio_file, str) and not os.path.exists(audio_file):
        return audio_file

    # Case 2: Streamlit upload → save temp file
    if hasattr(audio_file, "read"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            temp_path = tmp.name
    else:
        temp_path = audio_file

    # Transcribe
    segments, _ = model.transcribe(temp_path)

    text = " ".join(seg.text for seg in segments)

    # cleanup
    if hasattr(audio_file, "read"):
        os.remove(temp_path)

    return text
