from moviepy import *


# 1. Carrega os clipes
# Vídeo com a pessoa e o fundo verde que será removido
clip_foreground = VideoFileClip("avatar.mp4") 

# Imagem ou vídeo que aparecerá no fundo
clip_background = ImageClip("imagens/2.jpg") 

# 2. Define os parâmetros para o efeito
cor_a_remover = (1, 180, 14)  # O tom de verde que encontramos na sua imagem
tolerancia = 130             # Um bom valor inicial para a tolerância
rigidez_borda = 40          # Uma borda um pouco mais definida que o padrão
mask = ColorClip(color=(0, 255, 0), size=(1, 1))
# 3. Aplica o efeito MaskColor
# Usamos .fx() para aplicar o efeito ao nosso clipe
clip_sem_fundo = vfx.MaskColor( 
    color=cor_a_remover, 
    threshold=tolerancia, 
    stiffness=rigidez_borda
).apply(clip_foreground)
clip_sem_fundo = clip_sem_fundo.with_duration(2)
# 4. Compõe o vídeo final
# Coloca o clipe sem fundo em cima do clipe de fundo
video_final = CompositeVideoClip([
    clip_background.with_duration(clip_sem_fundo.duration), # Garante que o fundo tenha a mesma duração
    clip_sem_fundo.with_position(('center', 'center'))      # Centraliza o clipe da pessoa
])

# 5. Salva o resultado
video_final.write_videofile("video_final_com_chromakey.mp4", fps=24)

print("Vídeo com chromakey criado com sucesso!")