from moviepy import VideoFileClip, CompositeVideoClip, vfx, ImageClip
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess, shlex

def gerar_texto(dim: list, textos: list, font_path, font_size, cor, output, stroke_width=None, stroke_color=None, background_path=None):
    w, h = dim
    if background_path:
        fundo = Image.open(background_path).convert("RGBA").resize((w, h))
    else:
        fundo = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    draw = ImageDraw.Draw(fundo)
    fonte = ImageFont.truetype(font_path, font_size)

    if len(textos) >= 1:
        bbox1 = draw.textbbox(
            (0, 0), textos[0], font=fonte, stroke_width=stroke_width)
        text_w1, text_h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
        x1 = (w - text_w1) // 2
        y1 = 250
        draw.text((x1, y1), textos[0], font=fonte, fill=cor,
                  stroke_width=stroke_width, stroke_fill=stroke_color)

    if len(textos) >= 2:
        bbox2 = draw.textbbox(
            (0, 0), textos[1], font=fonte, stroke_width=stroke_width)
        text_w2, text_h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        x2 = (w - text_w2) // 2
        y2 = h - text_h2 - 250
        draw.text((x2, y2), textos[1], font=fonte, fill=cor,
                  stroke_width=stroke_width, stroke_fill=stroke_color)

    if output:
        fundo.save(output)

    return fundo

def cortar(arq, inicio, fim):
    cmd = f'ffmpeg -y -hide_banner -loglevel error -i "{arq}"'
    if inicio:
        cmd += f' -ss {inicio}'
    if fim:
        cmd += f' -to {fim}'
    cmd += f' -c copy "TEMP_CROP_PART.mp4"'
    proc = subprocess.run(shlex.split(cmd))
    return "TEMP_CROP_PART.mp4"

def editar(n):
    """
    """
    video_path = n['video']
    init = "00:00:00"
    h, m, s = init.split(':')
    h, m, s = int(h), int(m), int(s)

    m_fim = m + n['corte']
    if m_fim >= 60:
        h += m_fim // 60
        m_fim = m_fim % 60

    h = str(h).zfill(2)
    m_fim = str(m_fim).zfill(2)
    s = str(s).zfill(2)
    final = ':'.join([h, m_fim, s])
    clip = VideoFileClip(video_path)
    for_num = int(clip.duration / n['corte'])
    target_width, target_height = n['dimensao']
    
    for part in range(1, int(for_num) + 1):
        output_path = f"parte-{str(part).zfill(2)}.mp4"
        video_path_crop = cortar(video_path,init,final)
        clip = VideoFileClip(video_path_crop)
        clip_redimensionado = clip.with_effects(
            [vfx.Resize(width=target_width)])
        img_texto = gerar_texto(
            [target_width, target_height],
            [n['text'], f'Parte {part}'],
            n['fonte'],
            90,
            'red',
            output=None,
            stroke_width=4,
            stroke_color='white',
            background_path=n['bg']
        )

        frame = np.array(img_texto)
        back = ImageClip(frame).with_duration(clip.duration)
        video_final = CompositeVideoClip(
            [back, clip_redimensionado.with_position("center")])
        video_final.write_videofile(
            output_path,
            fps=30,
            codec="libx264",
            preset="ultrafast",
            ffmpeg_params=["-tune", "fastdecode", "-crf", "28"]
        )
        init = final
        final = int(final + n['corte'])
    return print(f'{output_path} criado com sucesso')


