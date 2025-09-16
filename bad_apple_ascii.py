# Bad Apple ASCII Player
# Plays video as ASCII art in command prompt

import cv2
import numpy as np
import os
import sys
import time
import threading
import subprocess
import platform
from pathlib import Path

class BadAppleASCII:
    def __init__(self, video_path, audio_path=None, fullscreen=False):
        self.video_path = video_path
        self.audio_path = audio_path
        self.cap = None
        self.fps = 30
        self.frame_delay = 1.0 / self.fps
        self.ascii_chars = " .:-=+*#%@"
        self.fullscreen = fullscreen
        self.width = 120 if fullscreen else 80
        self.height = 40 if fullscreen else 24
        self.audio_process = None
        self.is_playing = False
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def resize_frame(self, frame):
        height, width = frame.shape[:2]
        aspect_ratio = width / height
        terminal_aspect = self.width / self.height
        
        if aspect_ratio > terminal_aspect:
            new_width = self.width
            new_height = int(self.width / aspect_ratio)
        else:
            new_height = self.height
            new_width = int(self.height * aspect_ratio)
            
        resized = cv2.resize(frame, (new_width, new_height))
        
        if new_width < self.width or new_height < self.height:
            pad_width = self.width - new_width
            pad_height = self.height - new_height
            resized = np.pad(resized, 
                           ((0, pad_height), (0, pad_width)), 
                           mode='constant', 
                           constant_values=0)
        
        return resized[:self.height, :self.width]
    
    def frame_to_ascii(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = self.resize_frame(gray)
        normalized = resized.astype(np.float32) / 255.0
        
        ascii_frame = ""
        for row in normalized:
            for pixel in row:
                char_index = int(pixel * (len(self.ascii_chars) - 1))
                ascii_frame += self.ascii_chars[char_index]
            ascii_frame += "\n"
            
        return ascii_frame
    
    def play_audio(self):
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
    
    def play_video(self):
        if not os.path.exists(self.video_path):
            print(f"Error: Video file '{self.video_path}' not found!")
            return False
            
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print(f"Error: Could not open video file '{self.video_path}'!")
            return False
            
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_delay = 1.0 / self.fps if self.fps > 0 else 1.0 / 30.0
        
        if self.fullscreen:
            try:
                if platform.system() == "Windows":
                    os.system("mode con cols=120 lines=40")
            except:
                pass
        
        print("Bad Apple ASCII Player")
        print("=" * 25)
        print(f"Video: {os.path.basename(self.video_path)}")
        print(f"FPS: {self.fps:.2f}")
        print(f"Mode: {'Fullscreen' if self.fullscreen else 'Windowed'}")
        print(f"Size: {self.width}x{self.height}")
        print("Press Ctrl+C to stop")
        print("=" * 25)
        time.sleep(2)
        
        if self.audio_path and os.path.exists(self.audio_path):
            audio_thread = threading.Thread(target=self.play_audio)
            audio_thread.daemon = True
            audio_thread.start()
        
        self.is_playing = True
        frame_count = 0
        start_time = time.time()
        
        try:
            while self.is_playing:
                ret, frame = self.cap.read()
                if not ret:
                    break
                    
                ascii_frame = self.frame_to_ascii(frame)
                self.clear_screen()
                print(ascii_frame, end='')
                
                frame_count += 1
                elapsed_time = time.time() - start_time
                expected_time = frame_count * self.frame_delay
                
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
    
    player = BadAppleASCII(video_path, audio_path, fullscreen)
    success = player.play_video()
    
    if not success:
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
