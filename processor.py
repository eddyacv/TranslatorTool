import os
import shutil

from video_utils import (
    is_video,
    is_course_file,
    extract_audio,
    burn_subtitles,
    add_spanish_audio_track,
    make_silence,
    fit_segment_audio,
    concat_audio_files
)

from audio_utils import (
    transcribe_translate_segments,
    generate_tts_sync
)


def copy_course_materials(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if not is_course_file(file):
                continue

            source = os.path.join(root, file)
            relative_path = os.path.relpath(root, input_folder)
            output_dir = os.path.join(output_folder, relative_path)

            os.makedirs(output_dir, exist_ok=True)

            destination = os.path.join(output_dir, file)
            shutil.copy2(source, destination)


def process_single_video(
    input_video,
    input_folder,
    output_folder,
    generate_subs=True,
    burn_subs=False,
    generate_audio=True,
    keep_srt=True,
    model_size="small",
    voice="es-PE-AlexNeural",
    clean_temp=True
):
    relative_path = os.path.relpath(os.path.dirname(input_video), input_folder)
    output_dir = os.path.join(output_folder, relative_path)

    os.makedirs(output_dir, exist_ok=True)

    recursos_dir = os.path.join(output_folder, "recursos")
    temp_dir = os.path.join(recursos_dir, "temporales")

    os.makedirs(temp_dir, exist_ok=True)

    file = os.path.basename(input_video)
    name, ext = os.path.splitext(file)

    temp_audio = os.path.join(temp_dir, f"{name}_original.wav")
    srt_path = os.path.join(output_dir, f"{name}_es.srt")

    final_audio = os.path.join(temp_dir, f"{name}_audio_es_final.wav")
    final_video = os.path.join(output_dir, f"{name}_es.mp4")

    extract_audio(input_video, temp_audio)

    segments = transcribe_translate_segments(
        audio_path=temp_audio,
        srt_path=srt_path,
        model_size=model_size
    )

    current_video = input_video

    if burn_subs and os.path.exists(srt_path):
        subtitled_video = os.path.join(temp_dir, f"{name}_sub_es.mp4")
        burn_subtitles(input_video, srt_path, subtitled_video)
        current_video = subtitled_video

    if generate_audio:
        audio_parts = []
        current_time = 0.0

        for segment in segments:
            start = float(segment["start"])
            end = float(segment["end"])
            text = segment["text"].strip()
            target_duration = max(end - start, 0.4)

            gap = start - current_time

            if gap > 0.05:
                silence_path = os.path.join(
                    temp_dir,
                    f"{name}_silence_{segment['index']}.wav"
                )

                make_silence(silence_path, gap)
                audio_parts.append(silence_path)

            raw_segment_audio = os.path.join(
                temp_dir,
                f"{name}_segment_{segment['index']}.mp3"
            )

            fitted_segment_audio = os.path.join(
                temp_dir,
                f"{name}_segment_{segment['index']}_fit.wav"
            )

            generate_tts_sync(
                text=text,
                voice=voice,
                output_path=raw_segment_audio
            )

            fit_segment_audio(
                input_audio=raw_segment_audio,
                output_audio=fitted_segment_audio,
                target_duration=target_duration
            )

            audio_parts.append(fitted_segment_audio)
            current_time = end

        concat_audio_files(audio_parts, final_audio)

        add_spanish_audio_track(
            video_path=current_video,
            spanish_audio_path=final_audio,
            output_path=final_video
        )
    else:
        if current_video != input_video:
            shutil.copy2(current_video, final_video)
        else:
            shutil.copy2(input_video, final_video)

    if not keep_srt and os.path.exists(srt_path):
        os.remove(srt_path)

    if clean_temp and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)


def process_folder(
    input_folder,
    output_folder,
    generate_subs=True,
    burn_subs=False,
    generate_audio=True,
    keep_srt=True,
    copy_materials=True,
    model_size="small",
    voice="es-PE-AlexNeural",
    clean_temp=True
):
    if copy_materials:
        copy_course_materials(input_folder, output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if not is_video(file):
                continue

            input_video = os.path.join(root, file)

            process_single_video(
                input_video=input_video,
                input_folder=input_folder,
                output_folder=output_folder,
                generate_subs=generate_subs,
                burn_subs=burn_subs,
                generate_audio=generate_audio,
                keep_srt=keep_srt,
                model_size=model_size,
                voice=voice,
                clean_temp=clean_temp
            )