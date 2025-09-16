# Bad Apple ASCII Video Player

A command prompt implementation that plays Bad Apple (or any black and white video) as ASCII art with synchronized audio.

## Features

- 🎬 Plays any video file as ASCII art in the command prompt
- 🎵 Synchronized audio playback
- ⚡ Optimized for smooth playback
- 🎨 Adjustable terminal size and ASCII character set
- 🖥️ Cross-platform support (Windows, Linux, Mac)

## Requirements

- Python 3.7 or higher
- OpenCV (`opencv-python`)
- NumPy (`numpy`)

## Quick Start

### Windows (Easy Setup)

1. **Download and extract** all files to a folder
2. **Place your video file** (mp4, avi, mov, mkv, webm) in the same folder
3. **Optionally place an audio file** (mp3, wav, ogg, m4a) with the same name as the video
4. **Double-click `run.bat`** to start!

### Manual Setup

1. **Install Python** from [python.org](https://python.org)
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the player:**
   ```bash
   python bad_apple_ascii.py
   ```

## Usage

1. Place your video file in the same directory as the script
2. Optionally place an audio file with the same name as the video
3. Run the script and select your video file
4. Enjoy the ASCII art video with synchronized audio!

## Controls

- **Ctrl+C**: Stop playback
- **Resize terminal**: Not recommended during playback

## Video Requirements

- **Format**: MP4, AVI, MOV, MKV, WebM
- **Type**: Works best with black and white or high contrast videos
- **Resolution**: Any resolution (automatically resized to terminal)

## Audio Requirements

- **Format**: MP3, WAV, OGG, M4A
- **Synchronization**: Audio will start with video automatically

## Customization

You can modify the following in `bad_apple_ascii.py`:

- **Terminal size**: Change `self.width` and `self.height`
- **ASCII characters**: Modify `self.ascii_chars` for different art styles
- **Frame rate**: Adjust `self.fps` for different playback speeds

## Troubleshooting

### Common Issues

1. **"Python is not installed"**
   - Install Python from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **"No module named 'cv2'"**
   - Run: `pip install opencv-python`

3. **Audio not playing**
   - Check if audio file exists and has the same name as video
   - Ensure audio file format is supported

4. **Video too fast/slow**
   - The script automatically detects video FPS
   - For manual adjustment, modify `self.fps` in the code

### Performance Tips

- Use smaller terminal windows for better performance
- Close other applications to free up CPU
- Use high contrast videos for better ASCII art quality

## Technical Details

- Uses OpenCV for video processing
- Converts frames to grayscale and resizes to terminal dimensions
- Maps pixel intensity to ASCII characters
- Synchronizes audio using threading
- Optimized timing for smooth playback

## License

This project is open source and available under the MIT License.

## Credits

- Inspired by the original Bad Apple video
- Built with Python, OpenCV, and NumPy
- Command prompt optimization for Windows
