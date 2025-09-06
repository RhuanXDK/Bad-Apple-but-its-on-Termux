# Bad Apple!! but plays on Termux

This project plays **Bad Apple!!** in the Termux terminal using ASCII art with synchronized audio.  
It supports **1080p@60fps 16:9**, automatic frame extraction, caching, and runs smoothly in **Termux** or Linux terminals.
DISCLAIMER: **THIS CODE ONLY WORKS WITH TERMUX!**
---

## ✨ Features
- Converts video frames into ASCII art (Saves the ASCII frames for faster execution)  
- Supports **360p / 30fps / 4:3** (original Bad Apple video) **1080p / 60fps / 16:9** videos  
- Audio playback perfectly synced with video  
- Automatic download from YouTube via `yt-dlp`
- Saves the video frames in a folder 
- Replays start instantly once frames are cached  

---

## 📷 Screenshots

### 30 FPS 4:3 version example
![Bad Apple ASCII Example 1](assets/example1.png)

### 60 FPS 16:9 version example
![Bad Apple ASCII Example 2](assets/example2.png)


---

## 📦 Requirements
**Termux Android**

Install dependencies:
**Before you put the commands below, use `termux-setup-storage` To allow storage to Termux**

```bash
pkg install python ffmpeg
pip install yt-dlp pillow pydub
```

## How to Install and run the code

To run the file faster, you will create a .sh file directly from terminal

use:
```bash
pkg install nano
```
After installing nano, you will create the .sh file on it, using:

```bash
nano "file_name_here".sh
```
put these commands there:

```bash
cd storage
cd shared
clear
python 30fps.py https://youtu.be/FtutLA63Cp8
```
or

```bash
cd storage
cd shared
clear
python 60fps.py https://youtu.be/W3MkjcHOGH8
```
Ctrl + O to save and Ctrl + X to exit nano

Then you will install Python, FFmpeg (using the `pkg install` command) and the necessary dependencies (commands shown in requirements). The code should work if you have installed correctly 
