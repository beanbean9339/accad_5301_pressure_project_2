# Echo Void
### ACCAD 5301: Pressure Project 2, A Mystery Is Revealed

**Echo Void** is an interactive audiovisual project created in TouchDesigner. It combines live microphone input, speech-to-text transcription, webcam input, and hand tracking to transform spoken words into glowing particles that users can manipulate in real time.

As users speak, their words are transcribed and represented visually as particles. Using hand gestures, users can interact with these particles by gathering or dispersing them. As more speech is introduced, words can overlap, become difficult to read, and shift around the screen.

The project explores the relationship between speech, perception, and interaction. The computer reflects the user's speech, but transcription delays and recognition errors can make the result feel unfamiliar or unpredictable.

The project is called *Echo Void* because the computer echoes the user's speech back to them, sometimes with a delay or unexpected interpretation.

## Project Information

- **Project:** Pressure Project 2: A Mystery Is Revealed
- **Course:** ACCAD 5301
- **Institution:** The Ohio State University
- **Creator:** Isabella Lo
- **Software:** TouchDesigner
- **Speech Recognition:** OpenAI Whisper
- **Hand Tracking:** MediaPipe
- **Programming Language:** Python

## Files and Folder Structure

The repository contains the following files and folders:

```text
accad_5301_pressure_project_2/
├── README.md
├── pressure_project_2_IL.toe
├── whipser_worker.py
├── run script function.txt
└── td_whisper_stream/
    └── transcript.txt
```

*Note: Update the filenames in this diagram if your actual repository uses different names.*

### `README.md`

Documentation for the project, including its purpose, setup requirements, file structure, and instructions for running it.

### `Pressure_Project_2.toe`

The main TouchDesigner project file. It contains the node network used to create the visual experience and connect the different components, including the particle visuals, audio input, and hand-tracking interaction.

### `whisper_worker.py`

The Python script responsible for speech recognition using OpenAI Whisper.

The worker monitors the `td_whisper_stream/` directory for audio chunks named `chunk_*.wav`. When audio chunks are found, it processes them using Whisper and writes recognized speech to `transcript.txt`.

The script also:

- Loads the English `base.en` Whisper model.
- Checks audio volume using RMS (root mean square) to skip audio that is too quiet.
- Uses transcription settings intended to reduce silence-related and unreliable results.
- Writes updated transcripts through a temporary file, `transcript.tmp`, before replacing `transcript.txt`.
- Deletes processed audio chunks after attempting transcription.
- Continues running and checking for new audio chunks until manually stopped.

When the worker starts, it clears existing audio chunks and transcript files from the working directory. **Any unprocessed audio chunks or previous transcript files in that directory will therefore be removed at startup.**

### `run script function.txt`

A text file containing the command-line instruction used to start the Whisper worker in a separate Python process.

The current command is:

```bat
py -3.11 "C:\Users\beanb\Desktop\TouchDesigner Projects\accad 5301\pressure_project2_IL\whipser_worker.py"
```

This command uses the Python 3.11 launcher on Windows to execute the worker script.

The paths in this command are specific to the original development computer and must be updated before running the project on another device. The script filename in the command must also match the actual filename exactly.

### `td_whisper_stream/`

The working directory used to exchange audio and transcription files between TouchDesigner and the Python worker.

The worker expects to find audio chunks named `chunk_*.wav` in this directory. It writes the latest recognized text to `transcript.txt` and temporarily uses `transcript.tmp` when updating the transcript.

The directory is currently empty in the repository. This is expected if the project has not generated any audio chunks or transcript files. The Python script automatically creates the directory if it does not exist.

The project relies on this directory being correctly configured in both the TouchDesigner project and the Python worker.

## How the Project Works

### 1. Live Audio Input

The computer's microphone captures the user's speech through the project's audio-input setup in TouchDesigner.

Audio is processed into WAV chunks that the Python worker can read. These chunks are placed in the `td_whisper_stream/` directory for transcription.

No prerecorded audio files are included in the repository because the project is designed around live audio input.

### 2. Speech-to-Text with OpenAI Whisper

The `whisper_worker.py` script uses OpenAI Whisper to convert audio into text.

When the worker starts, it loads the `base.en` model. It then continuously checks the working directory for new `chunk_*.wav` files.

For each audio chunk, the script:

1. Loads the audio using Whisper's audio utilities.
2. Calculates the audio's RMS level.
3. Skips audio below the configured threshold of `0.001`.
4. Transcribes the audio in English with `fp16=False`.
5. Checks the transcription segments for results classified as silence.
6. Saves nonempty recognized text to `transcript.txt`.
7. Attempts to delete the processed WAV file.

The transcription settings include a temperature of `0`, disabled conditioning on previous text, and thresholds intended to filter silence and unreliable output.

The worker prints status messages to the terminal, including when the model loads, when audio is processed, the RMS level, recognized text, and any errors.

### 3. File-Based Communication

TouchDesigner and the Python worker exchange information through files in `td_whisper_stream/`.

The intended workflow is:

```text
Microphone
    ↓
TouchDesigner audio processing
    ↓
Audio chunks: chunk_*.wav
    ↓
whisper_worker.py
    ↓
OpenAI Whisper transcription
    ↓
transcript.txt
    ↓
TouchDesigner visual system
    ↓
Glowing particle text
```

TouchDesigner provides the audio chunks, while the worker processes them and writes the recognized text to a file. The TouchDesigner project can then use the transcript for its visual output.

The Python worker does not directly control the particle visuals. Instead, it handles speech recognition and updates the transcript file.

### 4. Particle-Based Text

The recognized words are represented as glowing particles in TouchDesigner. Rather than presenting speech only as ordinary text, the project transforms language into a visual form that users can manipulate.

As more words appear, the particles may overlap and shift, making the text less immediately readable.

### 5. Webcam and Hand Tracking

The project uses webcam input and MediaPipe hand tracking to detect hand movement.

The tracked index finger allows users to interact with the particles. Pinching the thumb and index finger together gathers particles, while spreading the fingers disperses them.

### 6. Interactive Experience

The different components combine speech recognition, particle visuals, and physical interaction.

The resulting experience is not simply a transcription of what someone says. Spoken language becomes part of a changing visual environment that responds to speech and hand movement.

## How to Use

### Requirements

Before running the project, make sure you have:

- TouchDesigner installed.
- A webcam.
- A working microphone.
- Python 3.11 installed and accessible through the Windows Python launcher, or an appropriately configured alternative.
- OpenAI Whisper installed in the Python environment used to run `whisper_worker.py`.
- NumPy installed in that environment.
- FFmpeg installed and available if required by your Whisper setup.
- The MediaPipe TouchDesigner plugin installed if the project requires it.
- Any additional dependencies required by the TouchDesigner project.

### Step 1: Download the Repository

Clone or download the repository to your computer.

Keep the project files together in the same directory where possible. The TouchDesigner project, Python worker, and launch instructions may refer to one another through local paths.

### Step 2: Install OpenAI Whisper

Follow the official installation instructions:

https://github.com/openai/whisper

Make sure Whisper and NumPy are installed in the same Python environment used to execute `whisper_worker.py`.

Whisper may download model weights the first time the `base.en` model is loaded. An internet connection may be required for this initial download.

### Step 3: Install FFmpeg

Whisper may require FFmpeg for audio processing. Follow the installation instructions for your operating system and ensure FFmpeg is available to the Python environment.

### Step 4: Install the MediaPipe TouchDesigner Plugin

If the project uses the MediaPipe TouchDesigner plugin, follow its installation instructions:

https://github.com/torinmb/mediapipe-touchdesigner

Confirm that the plugin is available in your TouchDesigner installation.

### Step 5: Update All Local File Paths

**Important: Update all hardcoded paths to match your own computer.**

The current scripts contain paths specific to the original development device. These paths will not work automatically on another computer.

Check the following:

- **`run script function.txt`:** Update the Python launcher or executable and the path to `whisper_worker.py`.
- **`whisper_worker.py`:** Update `WORK_DIR` so it points to your own `td_whisper_stream/` directory.
- **`Pressure_Project_2.toe`:** Check TouchDesigner nodes, parameters, and scripts for references to the original Python executable, worker script, working directory, plugins, and other local resources.

The worker's `WORK_DIR` currently points to:

```python
WORK_DIR = (
    r"C:\Users\beanb\Desktop\TouchDesigner Projects"
    r"\accad 5301\pressure_project2_IL\td_whisper_stream"
)
```

Replace this with the correct location on your computer. Python combines the two adjacent raw strings into one path.

Also, verify that the worker filename matches the filename used by the launch command. For example, the provided command uses `whipser_worker.py`, while the script has been referred to as `whisper_worker.py`. Correct any spelling mismatch.

If you change the directory structure, update every corresponding reference in both TouchDesigner and Python.

### Step 6: Start the Whisper Worker

Open `run script function.txt` and update the command for your device.

Run the command in Windows Command Prompt or another suitable terminal. For example, if the worker file is named `whisper_worker.py` and is located at the path shown below, the command would look like this:

```bat
py -3.11 "C:\path\to\your\project\whisper_worker.py"
```

Replace the example path with the actual location of your script.

Keep the worker running while using TouchDesigner. The terminal should display a message indicating that Whisper is loading, followed by a message that it is ready and waiting for microphone audio.

### Step 7: Open the TouchDesigner Project

Open `Pressure_Project_2.toe` in TouchDesigner.

Resolve any missing dependencies, plugin errors, or external file references. Confirm that the microphone and webcam are accessible and that the project points to the correct working directory.

### Step 8: Interact with Echo Void

1. **Speak into the microphone.** The audio is processed and transcribed by Whisper.
2. **Watch the particles.** Recognized words are represented as glowing particles.
3. **Use your index finger.** Move your hand in front of the webcam to interact with the particles.
4. **Pinch your thumb and index finger together.** Use this gesture to gather particles.
5. **Spread your fingers apart.** Use this gesture to disperse particles.
6. **Continue speaking and experimenting.** New words can overlap with existing particles and change the composition.

Speech-recognition speed and hand-tracking responsiveness depend on your hardware, configuration, and the performance of the running processes.

## Troubleshooting

### Whisper Does Not Start

- Confirm that Python 3.11 is installed and accessible.
- Verify that the launch command points to the correct Python environment and script.
- Make sure the script filename is spelled correctly.
- Confirm that Whisper and NumPy are installed in the environment used by the command.
- Check the terminal output for missing packages or other errors.

### Speech Is Not Being Transcribed

- Confirm that the microphone is connected and working.
- Check that the Whisper worker is running.
- Verify that TouchDesigner is generating audio chunks in `td_whisper_stream/`.
- Confirm that `WORK_DIR` points to the same directory used by TouchDesigner.
- Check the terminal for audio RMS values, transcription errors, or messages indicating that quiet audio was skipped.

The script ignores audio chunks whose RMS level is below `0.001`. If the input is too quiet, the worker may skip it.

### Words Do Not Appear in TouchDesigner

- Confirm that the worker is successfully updating `transcript.txt`.
- Check that TouchDesigner is reading the transcript from the correct directory.
- Verify that the project and Python script use the same working directory.
- Check the TouchDesigner network for missing file references or errors.

### Hand Tracking Does Not Work

- Confirm that the webcam is connected and available.
- Check that TouchDesigner has permission to access the webcam.
- Verify that the required MediaPipe plugin is installed.
- Make sure your hand is visible to the camera.

### The Project Works on One Computer but Not Another

This may be caused by hardcoded paths, different Python environments, missing dependencies, unavailable plugins, or differences in hardware.

Review the setup steps and update all relevant paths before running the project again.

## Tutorials and References

- [OpenAI Whisper](https://github.com/openai/whisper)  
  Open-source speech-recognition model used to transcribe spoken language into text.

- [MediaPipe TouchDesigner](https://github.com/torinmb/mediapipe-touchdesigner)  
  TouchDesigner integration for MediaPipe-based tracking and interaction.

- [TouchDesigner Documentation](https://docs.derivative.ca/)  
  Documentation for TouchDesigner operators, scripting, and project development.

## Credits

**Creator:** Isabella Lo  
**Institution:** The Ohio State University  
**Course:** ACCAD 5301  
**Project:** Pressure Project 2: A Mystery Is Revealed

This project combines TouchDesigner, Python, OpenAI Whisper, and MediaPipe to explore real-time speech recognition and gesture-based visual interaction.

Thanks to the creators and maintainers of the open-source tools and resources referenced above.

## Disclaimer

This project was developed as an educational and experimental creative-technology project. Setup may require additional configuration depending on your operating system, Python environment, TouchDesigner version, installed dependencies, and hardware.

The repository does not currently include prerecorded audio or image assets. The project is designed to use live microphone and webcam input.

The `td_whisper_stream/` directory is currently empty in the repository. During execution, it is used to store temporary audio chunks and transcript files. The worker also clears existing audio chunks and transcript files from this directory when it starts.

Before running the project, review the code, install the required dependencies, and update all local paths to match your own computer.
