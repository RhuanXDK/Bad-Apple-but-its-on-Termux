# Bad Apple!! but it plays on Termux

This project plays **Bad Apple!!** in the Termux terminal using ASCII art with synchronized audio.  
It supports **360p@30fps and 1080p@60fps 16:9**, automatic frame extraction, caching, and runs smoothly in **Termux** or Linux terminals

DISCLAIMER: **THIS CODE DOESNT WORK WITH WINDOWS**
---

## ✨ Features
- Converts video frames into ASCII art (Saves the ASCII frames for faster execution)  
- Supports **360p@30 4:3** (original Bad Apple video) and **1080p@60 16:9** 
- Audio playback perfectly synced with video  
- Automatic download from YouTube via `yt-dlp`
- Saves the video frames in a folder 
- Replays start instantly once frames are cached  

---

## 📷 Screenshots

### 30 FPS 4:3 version example
![30 FPS](https://cdn.discordapp.com/attachments/1059282510577668130/1413903018671476936/example.jpg?ex=68bd9f4c&is=68bc4dcc&hm=6f19b5729238ce207fe3cbddadd1c8b39cd342aa15ff8c0b359e24fb0743bb31&)

### 60 FPS 16:9 version example
![60 FPS](https://cdn.discordapp.com/attachments/1059282510577668130/1413903011893481593/example2.jpg?ex=68bd9f4b&is=68bc4dcb&hm=5f3e12797a39a6a412e0a024afc393a27aaf43a69889d489ffa3835093bee591&)


---

## 📦 Requirements
**Termux Android**

Required dependencies `Python, FFmpeg, Pillow, yt-dlp, pydub`


**Before you put the commands below, use `termux-setup-storage` To allow storage to Termux**


## How to install and run the code

1- Install Python and FFmpeg first:
```bash
pkg install python ffmpeg
```
2 - Install the `pip` dependencies
```bash
pip install yt-dlp pillow pydub
```

3 - To run the file faster, you will create a .sh file directly from terminal

use:
```bash
pkg install nano
```

4 - After installing nano, you will create the .sh file on it, using:

```bash
nano 30fps.sh
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


5 - To run the code, use `sh 30fps.sh` and wait until the code create everything, (there will be a log for you to watch)
