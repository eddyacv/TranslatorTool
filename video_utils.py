import os
import subprocess

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".webm"]
COURSE_EXTENSIONS = [".pdf", ".docx", ".xlsx", ".txt", ".html", ".htm"]


def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True)


def is_video(file):
    return os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS


def is_course_file(file):
    return os.path.splitext(file)[1].lower() in COURSE_EXTENSIONS


def get_duration(file_path):
    cmd = (
        f'ffprobe -v error -show_entries format=duration '
        f'-of default=noprint_wrappers=1:nokey=1 "{file_path}"'
    )

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def extract_audio(video_path, audio_path):
    cmd = f'ffmpeg -y -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}"'
    run_cmd(cmd)


def burn_subtitles(video_path, srt_path, output_path):
    srt_fixed = srt_path.replace("\\", "/").replace(":", "\\:")
    cmd = f'ffmpeg -y -i "{video_path}" -vf "subtitles=\'{srt_fixed}\'" -c:a copy "{output_path}"'
    run_cmd(cmd)


def add_spanish_audio_track(video_path, spanish_audio_path, output_path):
    cmd = (
        f'ffmpeg -y '
        f'-i "{video_path}" '
        f'-i "{spanish_audio_path}" '
        f'-map 0:v '
        f'-map 1:a '
        f'-map 0:a? '
        f'-c:v copy '
        f'-c:a aac '
        f'-metadata:s:a:0 language=spa '
        f'-metadata:s:a:0 title="Español" '
        f'-metadata:s:a:1 language=eng '
        f'-metadata:s:a:1 title="English" '
        f'-disposition:a:0 default '
        f'-disposition:a:1 0 '
        f'"{output_path}"'
    )

    run_cmd(cmd)


def build_atempo_filter(speed):
    filters = []

    while speed > 2.0:
        filters.append("atempo=2.0")
        speed /= 2.0

    while speed < 0.5:
        filters.append("atempo=0.5")
        speed /= 0.5

    filters.append(f"atempo={speed:.4f}")
    return ",".join(filters)


def make_silence(output_path, duration):
    if duration <= 0:
        return

    cmd = (
        f'ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo '
        f'-t {duration:.3f} "{output_path}"'
    )
    run_cmd(cmd)


def fit_segment_audio(input_audio, output_audio, target_duration):
    audio_duration = get_duration(input_audio)

    if audio_duration <= 0:
        return

    if audio_duration > target_duration:
        speed = audio_duration / target_duration
        atempo_filter = build_atempo_filter(speed)

        cmd = (
            f'ffmpeg -y -i "{input_audio}" '
            f'-filter:a "{atempo_filter},atrim=duration={target_duration:.3f}" '
            f'-ar 44100 -ac 2 "{output_audio}"'
        )
    else:
        cmd = (
            f'ffmpeg -y -i "{input_audio}" '
            f'-filter:a "apad,atrim=duration={target_duration:.3f}" '
            f'-ar 44100 -ac 2 "{output_audio}"'
        )

    run_cmd(cmd)


def concat_audio_files(audio_files, output_audio):
    list_path = output_audio + "_list.txt"

    with open(list_path, "w", encoding="utf-8") as f:
        for audio in audio_files:
            safe_audio = audio.replace("\\", "/")
            f.write(f"file '{safe_audio}'\n")

    cmd = f'ffmpeg -y -f concat -safe 0 -i "{list_path}" -c:a pcm_s16le "{output_audio}"'
    run_cmd(cmd)

    os.remove(list_path)