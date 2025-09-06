import os, sys, threading, subprocess, time, glob, shutil
from PIL import Image
from pydub import AudioSegment
from pydub.playback import play
import yt_dlp

# =========================
# CONFIG
# =========================
BASE_DIR = "/storage/emulated/0/badapple_xdk"
FRAMES_DIR = os.path.join(BASE_DIR, "frames")
ASCII_DIR = os.path.join(BASE_DIR, "ascii_frames")
AUDIO_PATH = os.path.join(BASE_DIR, "audio.wav")
VIDEO_PATH = os.path.join(BASE_DIR, "video.mp4")

ASCII_CHARS = " .:-=+*#%@"
CHAR_ASPECT = 0.5
AUDIO_DELAY = 0.2

# =========================
# FUNÇÕES
# =========================
def ensure_dirs():
    os.makedirs(FRAMES_DIR, exist_ok=True)
    os.makedirs(ASCII_DIR, exist_ok=True)

def map_pixel_to_char(val):
    return ASCII_CHARS[int((val / 255) * (len(ASCII_CHARS) - 1))]

def image_to_ascii(img, term_width, term_height):
    img = img.convert("L")
    w, h = img.size
    new_w = term_width - 4
    new_h = max(1, int((h / w) * new_w * CHAR_ASPECT))
    img = img.resize((new_w, new_h))

    pixels = img.getdata()
    chars = [map_pixel_to_char(p) for p in pixels]
    ascii_lines = ["".join(chars[i:i+new_w]) for i in range(0, len(chars), new_w)]

    # centralizar vertical
    vertical_pad = max(0, (term_height - len(ascii_lines)) // 2)
    ascii_lines = [""] * vertical_pad + ascii_lines

    # centralizar horizontal
    centered_lines = []
    for line in ascii_lines:
        pad = max(0, (term_width - len(line)) // 2)
        centered_lines.append(" " * pad + line)

    return "\n".join(centered_lines)

def list_frame_files(frames_dir):
    return sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))

def download_video(url, outpath):
    if os.path.exists(outpath):
        print("Video already exist, skipping...")
        return outpath
    print("Downloading video...")
    ydl_opts = {"format":"bestvideo+bestaudio/best","outtmpl":outpath,"merge_output_format":"mp4","quiet":True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
    print("Video downloaded successfully!")
    return outpath

def extract_audio(video_path, out_audio_path):
    if os.path.exists(out_audio_path):
        print("Audio already exist, skipping...")
        return
    print("Downloading audio...")
    cmd = ["ffmpeg","-y","-i",video_path,"-vn","-acodec","pcm_s16le","-ar","44100","-ac","2",out_audio_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Audio downloaded successfully!")

def extract_frames(video_path, frames_dir, fps):
    if list_frame_files(frames_dir):
        print("Video frames already exists, skipping...")
        return
    print("Extracting video frames...")
    pattern = os.path.join(frames_dir,"frame_%06d.png")
    cmd = ["ffmpeg","-y","-i",video_path,"-vf",f"fps={fps}",pattern]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Video frames extracted successfully!")

def get_fps_and_duration(video_path, url):
    with yt_dlp.YoutubeDL({"quiet":True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("fps",30), info.get("duration",0)

def save_ascii_frames(frame_files, term_width, term_height):
    ascii_files = sorted(glob.glob(os.path.join(ASCII_DIR,"frame_*.txt")))
    if ascii_files and len(ascii_files) == len(frame_files):
        print("ASCII frames already exists, skipping...")
        return ascii_files
    print("Converting frames to ASCII...")
    for i,fpath in enumerate(frame_files):
        img = Image.open(fpath)
        ascii_frame = image_to_ascii(img, term_width, term_height)
        with open(os.path.join(ASCII_DIR,f"frame_{i:06d}.txt"),"w",encoding="utf-8") as f: f.write(ascii_frame)
        print(f"\r ASCII frames converted: {i+1}/{len(frame_files)}", end="", flush=True)
    print("\n Conversion to ASCII has been completed! ")
    return sorted(glob.glob(os.path.join(ASCII_DIR,"frame_*.txt")))

def play_audio(audio_path):
    audio = AudioSegment.from_wav(audio_path)
    threading.Thread(target=play,args=(audio,),daemon=True).start()

def format_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02}:{s:02}"

def display_ascii(ascii_files, fps_target, duration):
    frame_interval = 1.0/fps_target
    start_time = None
    os.system("clear")
    sys.stdout.write("\x1b[?25l")  # esconde cursor
    total = len(ascii_files)

    prev_frame_time = None
    fps_accum = 0
    fps_count = 0
    last_fps_update = 0
    fps_display = fps_target  # inicial

    try:
        for i,txt_path in enumerate(ascii_files):
            target_time = i*frame_interval
            if start_time is None: start_time = time.perf_counter()
            while time.perf_counter()-start_time < target_time: time.sleep(0.0005)

            with open(txt_path,"r",encoding="utf-8") as f: ascii_frame=f.read()

            now = time.perf_counter()
            elapsed = now - start_time

            # FPS real por frame
            if prev_frame_time is not None:
                delta = now - prev_frame_time
                if delta > 0:
                    fps_accum += 1.0/delta
                    fps_count += 1
            prev_frame_time = now

            # atualizar FPS a cada 1s
            if elapsed - last_fps_update >= 1.0 and fps_count > 0:
                fps_display = fps_accum / fps_count
                fps_accum = 0
                fps_count = 0
                last_fps_update = elapsed

            sys.stdout.write("\x1b[H")
            sys.stdout.write(ascii_frame+"\n\n")
            # log principal
            sys.stdout.write(
                f"Frame {i+1}/{total} | {format_time(elapsed)}/{format_time(duration)}\n"
            )
            # FPS médio atualizado a cada segundo
            sys.stdout.write(f"FPS: {fps_display:.1f}\n")
            sys.stdout.flush()
    finally:
        sys.stdout.write("\x1b[?25h")  # mostra cursor
        sys.stdout.flush()

def main():
    if len(sys.argv)<2:
        print("Uso: python badapple.py <URL>")
        sys.exit(1)
    url=sys.argv[1]
    ensure_dirs()
    VIDEO=download_video(url,VIDEO_PATH)
    fps,duration=get_fps_and_duration(VIDEO,url)
    extract_audio(VIDEO,AUDIO_PATH)
    extract_frames(VIDEO,FRAMES_DIR,fps)
    frame_files=list_frame_files(FRAMES_DIR)
    term_cols, term_rows = shutil.get_terminal_size()
    ascii_files=save_ascii_frames(frame_files,term_cols,term_rows-5)
    time.sleep(AUDIO_DELAY)
    play_audio(AUDIO_PATH)
    display_ascii(ascii_files,fps,duration)

if __name__=="__main__":
    main()