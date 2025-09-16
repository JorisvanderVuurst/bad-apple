# Bad Apple ASCII Player - Enhanced Version
# Plays video files as ASCII art in command prompt with audio

import cv2
import numpy as np
import os
import sys
import time
import threading
import subprocess
import platform
import msvcrt
from pathlib import Path
from collections import deque

class BadApplePlayer:
    def __init__(self, video_path, audio_path=None, fullscreen=False):
        self.video_path = video_path
        self.audio_path = audio_path
        self.cap = None
        self.fps = 30
        self.frame_delay = 1.0 / self.fps
        self.ascii_chars = " .:-=+*#%@"
        self.fullscreen = fullscreen
        self.width = 150 if fullscreen else 100
        self.height = 45 if fullscreen else 30
        self.audio_process = None
        self.is_playing = False
        self.frame_buffer = deque(maxlen=10)
        self.last_frame_time = 0
        self.frame_skip = 0
        self.frame_count = 0
        self.start_time = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def get_terminal_size(self):
        try:
            if platform.system() == "Windows":
                from ctypes import windll
                h = windll.kernel32.GetStdHandle(-12)
                csbi = (ctypes.c_ulong * 22)()
                windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
                width = csbi[2] - csbi[0] + 1
                height = csbi[3] - csbi[1] + 1
                self.width = min(width, 120)
                self.height = min(height - 2, 40)
            else:
                import shutil
                size = shutil.get_terminal_size()
                self.width = min(size.columns, 120)
                self.height = min(size.lines - 2, 40)
        except:
            pass
            
    def resize_frame_optimized(self, frame):
        height, width = frame.shape[:2]
        aspect_ratio = width / height
        terminal_aspect = self.width / self.height
        
        if aspect_ratio > terminal_aspect:
            new_width = self.width
            new_height = int(self.width / aspect_ratio)
        else:
            new_height = self.height
            new_width = int(self.height * aspect_ratio)
            
        if new_width < width and new_height < height:
            resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        else:
            resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        
        if new_width < self.width or new_height < self.height:
            pad_width = self.width - new_width
            pad_height = self.height - new_height
            pad_left = pad_width // 2
            pad_right = pad_width - pad_left
            pad_top = pad_height // 2
            pad_bottom = pad_height - pad_top
            
            resized = np.pad(resized, 
                           ((pad_top, pad_bottom), (pad_left, pad_right)), 
                           mode='constant', 
                           constant_values=0)
        
        return resized[:self.height, :self.width]
    
    def frame_to_ascii_enhanced(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.convertScaleAbs(gray, alpha=1.2, beta=10)
        resized = self.resize_frame_optimized(gray)
        normalized = resized.astype(np.float32) / 255.0
        normalized = np.power(normalized, 0.8)
        
        ascii_frame = ""
        for row in normalized:
            for pixel in row:
                char_index = int(pixel * (len(self.ascii_chars) - 1))
                char_index = max(0, min(char_index, len(self.ascii_chars) - 1))
                ascii_frame += self.ascii_chars[char_index]
            ascii_frame += "\n"
            
        return ascii_frame
    
    def play_audio_enhanced(self):
        if not self.audio_path or not os.path.exists(self.audio_path):
            return
            
        try:
            self.audio_process = subprocess.Popen([
                "ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", self.audio_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            try:
                if platform.system() == "Windows":
                    self.audio_process = subprocess.Popen([
                        "powershell", "-c", 
                        f"$player = New-Object Media.SoundPlayer '{self.audio_path}'; $player.PlayLooping()"
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e2:
                print(f"Audio error: {e2}")
    
    def stop_audio(self):
        if self.audio_process:
            self.audio_process.terminate()
            self.audio_process = None
    
    def check_keypress(self):
        if platform.system() == "Windows":
            return msvcrt.kbhit()
        else:
            import select
            import tty
            import termios
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
    
    def get_keypress(self):
        if platform.system() == "Windows":
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8', errors='ignore')
        else:
            import tty
            import termios
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    return sys.stdin.read(1)
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        return None
    
    def play_video_enhanced(self):
        if not os.path.exists(self.video_path):
            print(f"Error: Video file '{self.video_path}' not found!")
            return False
            
        if not self.fullscreen:
            self.get_terminal_size()
        
        if self.fullscreen:
            try:
                if platform.system() == "Windows":
                    os.system("mode con cols=150 lines=45")
            except:
                pass
        
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print(f"Error: Could not open video file '{self.video_path}'!")
            return False
            
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_delay = 1.0 / self.fps if self.fps > 0 else 1.0 / 30.0
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / self.fps if self.fps > 0 else 0
        
        print("Bad Apple ASCII Player")
        print("=" * 30)
        print(f"Video: {os.path.basename(self.video_path)}")
        print(f"FPS: {self.fps:.2f}")
        print(f"Duration: {duration:.1f}s")
        print(f"Mode: {'Fullscreen' if self.fullscreen else 'Windowed'}")
        print(f"Size: {self.width}x{self.height}")
        print("Controls: Space=Pause, Q=Quit, +/-=Speed")
        print("=" * 30)
        time.sleep(2)
        
        if self.audio_path and os.path.exists(self.audio_path):
            audio_thread = threading.Thread(target=self.play_audio_enhanced)
            audio_thread.daemon = True
            audio_thread.start()
        
        self.is_playing = True
        self.start_time = time.time()
        paused = False
        speed_multiplier = 1.0
        
        try:
            while self.is_playing:
                if self.check_keypress():
                    key = self.get_keypress()
                    if key:
                        if key.lower() == 'q':
                            break
                        elif key == ' ':
                            paused = not paused
                        elif key == '+':
                            speed_multiplier = min(speed_multiplier * 1.1, 3.0)
                        elif key == '-':
                            speed_multiplier = max(speed_multiplier * 0.9, 0.1)
                
                if paused:
                    time.sleep(0.1)
                    continue
                
                ret, frame = self.cap.read()
                if not ret:
                    break
                    
                ascii_frame = self.frame_to_ascii_enhanced(frame)
                self.clear_screen()
                print(ascii_frame, end='')
                
                elapsed = time.time() - self.start_time
                progress = (self.frame_count / total_frames) * 100 if total_frames > 0 else 0
                print(f"Time: {elapsed:.1f}s | Progress: {progress:.1f}% | Speed: {speed_multiplier:.1f}x")
                
                self.frame_count += 1
                expected_time = self.frame_count * (self.frame_delay / speed_multiplier)
                elapsed_time = time.time() - self.start_time
                
                sleep_time = expected_time - elapsed_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            print("\n\nStopped.")
            
        finally:
            self.is_playing = False
            self.stop_audio()
            if self.cap:
                self.cap.release()
                
        return True

def main():
    print("Bad Apple ASCII Player")
    print("=" * 25)
    
    fullscreen = False
    try:
        fullscreen_choice = input("Fullscreen? (y/n): ").lower().strip()
        fullscreen = fullscreen_choice in ['y', 'yes', '1', 'true']
    except:
        pass
    
    video_files = [f for f in os.listdir('.') if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm'))]
    
    if not video_files:
        print("No video files found!")
        print("Put a video file in this folder.")
        input("Press Enter to exit...")
        return
    
    if len(video_files) == 1:
        video_path = video_files[0]
        print(f"Using: {video_path}")
    else:
        print("Video files:")
        for i, video in enumerate(video_files, 1):
            print(f"{i}. {video}")
        
        try:
            choice = int(input("Pick one: ")) - 1
            if 0 <= choice < len(video_files):
                video_path = video_files[choice]
            else:
                print("Invalid!")
                return
        except ValueError:
            print("Invalid input!")
            return
    
    audio_path = None
    audio_files = [f for f in os.listdir('.') if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a'))]
    
    if audio_files:
        video_name = os.path.splitext(video_path)[0]
        for audio in audio_files:
            if os.path.splitext(audio)[0].lower() == video_name.lower():
                audio_path = audio
                break
        
        if not audio_path and len(audio_files) == 1:
            audio_path = audio_files[0]
    
    if audio_path:
        print(f"Audio: {audio_path}")
    else:
        print("No audio file - playing without sound")
    
    player = BadApplePlayer(video_path, audio_path, fullscreen)
    success = player.play_video_enhanced()
    
    if not success:
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
