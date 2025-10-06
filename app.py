import base64
import io
import wave
# MUDANÇA AQUI: Trocamos jsonify por send_file
from flask import Flask, send_file, request, jsonify 
from piper import PiperVoice

# --- Inicialização ---
# 1. Crie a aplicação Flask
app = Flask(__name__)

# 2. Carregue o modelo da voz UMA VEZ ao iniciar o servidor.
print("Carregando modelo de voz...")
try:
    voice = PiperVoice.load("pt_BR-faber-medium.onnx", "pt_BR-faber-medium.onnx.json")
    print("Modelo de voz carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    voice = None

# --- Rota da API ---
@app.route('/synthesize', methods=['GET'])
def synthesize():
    """
    Gera áudio a partir de um texto e retorna o arquivo de áudio diretamente.
    Use: /synthesize?text=seu+texto+aqui
    """
    if not voice:
        return jsonify({"error": "Modelo de voz não foi carregado."}), 500

    # 1. Pega o texto do parâmetro 'text' na URL.
    text_to_synthesize = request.args.get('text')
    if not text_to_synthesize:
        return jsonify({"error": "Parâmetro 'text' é obrigatório."}), 400

    try:
        
        with wave.open('audio.wav', "wb") as wav_file:
            # Definindo parâmetros padrão para o WAV
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(22050) # Taxa de amostragem do modelo
            voice.synthesize_wav(text_to_synthesize, wav_file)
        
        # --- MUDANÇA PRINCIPAL AQUI ---
        
        # 4. "Rebobina" o buffer para o início.
        #    Isso é crucial para que o send_file possa ler o conteúdo desde o começo.
        

        # 5. Retorna o buffer como um arquivo de áudio.
        return send_file(
            'audio.wav',
            mimetype='audio/wav',        # Informa ao navegador que é um arquivo de áudio WAV
            as_attachment=False,         # 'False' tenta tocar no navegador, 'True' força o download
            download_name='audio.wav'    # Nome padrão do arquivo se o usuário decidir salvar
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Execução ---
if __name__ == '__main__':
    # Roda o servidor na porta 5003, acessível na sua rede local.
    app.run(host='0.0.0.0', port=5003, debug=True)