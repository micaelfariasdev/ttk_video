import os
from moviepy import *


# --- Parâmetros do Vídeo (você pode alterar aqui) ---
PASTA_IMAGENS = "imagens"
ARQUIVO_SAIDA = "carrossel_video_com_chromakey.mp4"
MUSICA_FUNDO = "audio.wav"
VIDEO_CHROMAKEY = "avatar.mp4" # Nome do seu vídeo com chroma key

audio_clip_final = None
if os.path.exists(MUSICA_FUNDO):
    print("Adicionando música de fundo...")
    audio_clip = AudioFileClip(MUSICA_FUNDO)
else:
    print(f"Arquivo de música '{MUSICA_FUNDO}' não encontrado. O vídeo será gerado sem áudio.")


CHROMA_COLOR = (1, 180, 14) # Exemplo: verde puro. Ajuste para o seu vídeo!
CHROMA_THRESHOLD = 130      # Tolerância para a remoção da cor (0-255). Ajuste!
CHROMA_STIFFNESS = 40      # Tolerância para a remoção da cor (0-255). Ajuste!


# 1. Carrega a lista de imagens da pasta (igual ao anterior)
print("Procurando por imagens na pasta...")
arquivos_imagem = [img for img in os.listdir(PASTA_IMAGENS) if img.endswith(('.png', '.jpg', '.jpeg'))]
arquivos_imagem.sort()

DURACAO_POR_FOTO = audio_clip.duration / len(arquivos_imagem)  
DURACAO_TRANSICAO = 0.3 # segundos da transição (crossfade)
VIDEO_SIZE = (1080, 1920) # Tamanho do vídeo (largura, altura) - Vertical
FPS = 24 # Frames por segundo

if not arquivos_imagem:
    print("Nenhuma imagem encontrada na pasta 'imagens'. Verifique os nomes e a estrutura de pastas.")
    exit()

print(f"Encontradas {len(arquivos_imagem)} imagens. Começando a criação dos clipes base.")

# 2. Cria os clipes de imagem base (igual ao anterior)
clipes_base = []
for imagem in arquivos_imagem:
    caminho_completo = os.path.join(PASTA_IMAGENS, imagem)
    clip = ImageClip(caminho_completo)
    clip = clip.resized(width=VIDEO_SIZE[0]).with_position(('center', 'center')) # Usa set_position para compatibilidade
    clipes_base.append(clip)

# 3. Cria a lista final de clipes com duração, posição e transições (igual ao anterior)
clips_finais_carrossel = [] # Renomeado para clareza
for i, clip in enumerate(clipes_base):
    start_time = i * (DURACAO_POR_FOTO - DURACAO_TRANSICAO)
    clip_com_duracao = clip.with_duration(DURACAO_POR_FOTO) # Usa set_duration
    clip_posicionado = clip_com_duracao.with_start(start_time) # Usa set_start

    if i > 0:
        clip_posicionado = vfx.FadeIn(DURACAO_TRANSICAO).apply(clip_posicionado)
        
    clips_finais_carrossel.append(clip_posicionado)

# 4. Compõe o vídeo base do carrossel
video_carrossel_base = CompositeVideoClip(clips_finais_carrossel, size=VIDEO_SIZE)
duracao_total_video = video_carrossel_base.duration

print(f"Duração total do vídeo base do carrossel: {duracao_total_video:.2f} segundos.")

# --- NOVO: Lógica para o Vídeo de Chroma Key ---
video_chroma_final = None
if os.path.exists(VIDEO_CHROMAKEY):
    print(f"Processando vídeo de chroma key: '{VIDEO_CHROMAKEY}'...")
    clip_chroma = VideoFileClip(VIDEO_CHROMAKEY)
    
    # Redimensiona o vídeo de chroma key para o tamanho do seu vídeo final
    # Você pode querer ajustar isso: talvez apenas redimensionar a altura/largura, ou um crop
    # Exemplo: Redimensiona para metade da largura e centraliza
    clip_chroma = clip_chroma.resized(width=VIDEO_SIZE[0]) # Metade da largura do vídeo final
    clip_chroma = clip_chroma.with_position(("center", "bottom")) # Centralizado na largura, no fundo
    
    # Garante que o vídeo de chroma key tenha a mesma duração do carrossel (loop)
    video_chroma_final = vfx.Loop(duration=duracao_total_video).apply(clip_chroma)

    # Aplica o efeito de chroma key
    video_chroma_final = vfx.MaskColor(color=CHROMA_COLOR, threshold=CHROMA_THRESHOLD, stiffness=CHROMA_STIFFNESS).apply(video_chroma_final)
    
    print("Vídeo de chroma key processado com sucesso.")

else:
    print(f"Arquivo de vídeo '{VIDEO_CHROMAKEY}' não encontrado. O vídeo será gerado sem o efeito de chroma key.")


# 5. Adiciona a música de fundo (igual ao anterior, mas agora no vídeo final após composição)



# 6. Compõe o vídeo final (carrossel + chroma key)
video_chroma_final = video_chroma_final.with_audio(audio_clip)
final_clips_to_compose = []
final_clips_to_compose.append(video_carrossel_base)
if video_chroma_final:
    final_clips_to_compose.append(video_chroma_final)


# 7. Adiciona o áudio ao vídeo final composto

video_final_composto = CompositeVideoClip(final_clips_to_compose, size=VIDEO_SIZE)

video_final_composto =video_final_composto.with_duration(2)

# 8. Escreve o arquivo de vídeo final
print(f"Renderizando o vídeo final em '{ARQUIVO_SAIDA}'...")
video_final_composto.write_videofile(
    ARQUIVO_SAIDA,
    fps=FPS,
    codec='libx264',
    audio_codec='aac'
)

print("Vídeo criado com sucesso!")