import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# Add FFmpeg path to Python's PATH
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

def get_ffmpeg_version():
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()[0]  # Return the first line of the output
    except FileNotFoundError:
        return "Error: FFmpeg is not installed or not in PATH."
    except subprocess.CalledProcessError as e:
        return f"Error while checking FFmpeg version: {e.stderr.strip()}"

def show_ffmpeg_version():
    version_info = get_ffmpeg_version()
    messagebox.showinfo("FFmpeg Version", version_info)

def analyze_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mkv *.avi")])
    if not file_path:
        return

    try:
        # Run ffmpeg to analyze the video file
        result = subprocess.run(
            ["ffmpeg", "-i", file_path],
            stderr=subprocess.PIPE,  # ffmpeg writes metadata to stderr
            text=True
        )

        # Clear previous metadata output
        title_output.config(state=tk.NORMAL)
        episode_output.config(state=tk.NORMAL)
        duration_output.config(state=tk.NORMAL)
        video_stream_output.config(state=tk.NORMAL)
        audio_stream_output.config(state=tk.NORMAL)

        title_output.delete(1.0, tk.END)
        episode_output.delete(1.0, tk.END)
        duration_output.delete(1.0, tk.END)
        video_stream_output.delete(1.0, tk.END)
        audio_stream_output.delete(1.0, tk.END)

        if result.returncode != 1:  # FFmpeg exits with code 1 on successful metadata display
            messagebox.showerror("Error", "Failed to analyze the file. Please check the file format.")
            return

        # Extract metadata details
        title, episode, duration, video_stream, audio_stream = None, None, None, [], []

        for line in result.stderr.splitlines():
            line = line.strip()
            if "title" in line and not title:
                title = line.split(":")[1].strip()
            elif "episode_id" in line and not episode:
                episode = line.split(":")[1].strip()
            elif "Duration" in line and not duration:
                duration = line.split("Duration:")[1].split(",")[0].strip()
            elif "Stream" in line:
                if "Video:" in line:
                    video_stream.append(line)
                elif "Audio:" in line:
                    audio_stream.append(line)

        # Populate metadata fields
        if title:
            title_output.insert(tk.END, title)
        else:
            title_output.insert(tk.END, "No title information available.")

        if episode:
            episode_output.insert(tk.END, episode)
        else:
            episode_output.insert(tk.END, "No episode information available.")

        if duration:
            duration_output.insert(tk.END, duration)
        else:
            duration_output.insert(tk.END, "No duration information available.")

        if video_stream:
            video_stream_output.insert(tk.END, "\n".join(video_stream))
        else:
            video_stream_output.insert(tk.END, "No video stream information available.")

        if audio_stream:
            audio_stream_output.insert(tk.END, "\n".join(audio_stream))
        else:
            audio_stream_output.insert(tk.END, "No audio stream information available.")

        # Disable editing of text areas
        title_output.config(state=tk.DISABLED)
        episode_output.config(state=tk.DISABLED)
        duration_output.config(state=tk.DISABLED)
        video_stream_output.config(state=tk.DISABLED)
        audio_stream_output.config(state=tk.DISABLED)

    except FileNotFoundError:
        messagebox.showerror("Error", "FFmpeg is not installed or not in PATH.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

# Create main application window
app = tk.Tk()
app.title("Video Metadata Viewer")
app.geometry("600x800")

# Create the menu bar
menu_bar = tk.Menu(app)

# Add Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="FFmpeg Version", command=show_ffmpeg_version)
menu_bar.add_cascade(label="Help", menu=help_menu)

app.config(menu=menu_bar)

# Title
tk.Label(app, text="Video Metadata Viewer", font=("Arial", 16)).pack(pady=10)

# Analyze button
tk.Button(app, text="Analyze Video", command=analyze_video).pack(pady=10)

# Frames for Metadata sections
metadata_frame = tk.Frame(app)
metadata_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Title frame
title_frame = tk.LabelFrame(metadata_frame, text="Title", font=("Arial", 12))
title_frame.pack(fill=tk.X, padx=5, pady=5)

title_output = tk.Text(title_frame, wrap=tk.WORD, height=2, state=tk.DISABLED)
title_output.pack(fill=tk.X, padx=5, pady=5)

# Episode frame
episode_frame = tk.LabelFrame(metadata_frame, text="Episode", font=("Arial", 12))
episode_frame.pack(fill=tk.X, padx=5, pady=5)

episode_output = tk.Text(episode_frame, wrap=tk.WORD, height=2, state=tk.DISABLED)
episode_output.pack(fill=tk.X, padx=5, pady=5)

# Duration frame
duration_frame = tk.LabelFrame(metadata_frame, text="Duration", font=("Arial", 12))
duration_frame.pack(fill=tk.X, padx=5, pady=5)

duration_output = tk.Text(duration_frame, wrap=tk.WORD, height=2, state=tk.DISABLED)
duration_output.pack(fill=tk.X, padx=5, pady=5)

# Video Stream frame
video_stream_frame = tk.LabelFrame(metadata_frame, text="Video Stream Information", font=("Arial", 12))
video_stream_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

video_stream_output = tk.Text(video_stream_frame, wrap=tk.WORD, height=8, state=tk.DISABLED)
video_stream_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Audio Stream frame
audio_stream_frame = tk.LabelFrame(metadata_frame, text="Audio Stream Information", font=("Arial", 12))
audio_stream_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

audio_stream_output = tk.Text(audio_stream_frame, wrap=tk.WORD, height=8, state=tk.DISABLED)
audio_stream_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

app.mainloop()
