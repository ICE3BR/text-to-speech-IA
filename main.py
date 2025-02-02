import hashlib
import os
from pathlib import Path

import config  # Importando as configurações
import keyring
from dotenv import load_dotenv
from InquirerPy import prompt
from openai import OpenAI

# 🔍 Obtém o diretório onde `main.py` está localizado
BASE_DIR = Path(__file__).parent.resolve()
download_dir = BASE_DIR / config.DOWNLOAD_FOLDER  # Usando `config.py`
download_dir.mkdir(exist_ok=True)

# 🔐 Tentar carregar a chave da API do keyring
API_KEY_KEYRING = keyring.get_password("openai", "api_key")

# 🔐 Tentar carregar a chave da API do .ENV
load_dotenv()
API_KEY_ENV = os.getenv("OPENAI_API_KEY")

# Escolher a melhor chave disponível
if API_KEY_KEYRING:
    API_KEY = API_KEY_KEYRING
elif API_KEY_ENV:
    API_KEY = API_KEY_ENV
else:
    API_KEY = None

if not API_KEY:
    raise ValueError(
        "❌ A chave da API não foi encontrada no keyring nem no .env. Configure-a primeiro."
    )

client = OpenAI(api_key=API_KEY)


# 🔹 Funções auxiliares
def get_cache_key(text, voice, speed):
    """Gera uma chave única para cada combinação de texto, voz e velocidade."""
    key = f"{text}-{voice}-{speed}"
    return hashlib.md5(key.encode()).hexdigest()


def load_from_cache(cache_key):
    """Verifica se o arquivo de áudio já foi gerado anteriormente."""
    cache_file = download_dir / f"{cache_key}.mp3"
    if cache_file.exists():
        print(f"🎵 Áudio encontrado no cache: {cache_file}")
        return cache_file
    return None


def save_to_cache(response, cache_key):
    """Salva o áudio gerado no cache para reutilização futura."""
    cache_file = download_dir / f"{cache_key}.mp3"
    with open(cache_file, "wb") as f:
        f.write(response.content)
    print(f"✅ Áudio salvo no cache: {cache_file}")
    return cache_file


def generate_speech(client, text, voice="echo", speed=0.96):
    """
    Gera áudio a partir de texto usando a API da OpenAI.

    Args:
        client: Cliente da OpenAI configurado.
        text (str): Texto a ser convertido em áudio.
        voice (str): Voz selecionada.
        speed (float): Velocidade da fala.

    Returns:
        Resposta da API contendo o áudio gerado.
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="mp3",
        speed=speed,
    )
    return response


# 🎤 Função principal
def main():
    # 🎤 Menu para seleção de voz
    menu_voz = [
        {
            "type": "list",
            "name": "voice",
            "message": "Escolha uma voz do menu:",
            "choices": config.VOICES + ["Sair"],  # Usando `config.py`
        },
    ]

    selected_voice = prompt(menu_voz)["voice"]
    if selected_voice == "Sair":
        print("👋 Saindo...")
        return

    # 🛠️ Menu para seleção de modelo
    menu_model = [
        {
            "type": "list",
            "name": "model",
            "message": "Escolha um modelo do menu:",
            "choices": list(config.MODELS.keys()) + ["Sair"],  # Usando `config.py`
        },
    ]

    selected_model = prompt(menu_model)["model"]
    if selected_model == "Sair":
        print("👋 Saindo...")
        return

    print(f"🎙️ Voz escolhida: {selected_voice}")
    print(f"🛠️ Modelo escolhido: {selected_model} ({config.MODELS[selected_model]})")

    # 📝 Solicitar texto ao usuário
    user_input = input("📝 Digite o texto a ser falado: ").strip()
    if not user_input:
        user_input = "Bem-vindo ao Lyra Speech! Como posso ajudar você hoje?"

    # 🕒 Solicitar velocidade da fala ao usuário
    while True:
        speed_input = input(
            f"⚡ Digite a velocidade da fala (Padrão: {config.DEFAULT_SPEED} | 0.25 - 4.0): "
        ).strip()
        if not speed_input:  # Se não digitar nada, usa o padrão
            speed = config.DEFAULT_SPEED
            break
        try:
            speed = float(speed_input)
            if 0.25 <= speed <= 4.0:  # Garante que está dentro do intervalo permitido
                break
            else:
                print("❌ Velocidade inválida! Insira um valor entre 0.25 e 4.0.")
        except ValueError:
            print("❌ Entrada inválida! Digite um número decimal (ex: 1.2).")

    # 🔍 Verificar no cache antes de gerar o áudio
    cache_key = get_cache_key(user_input, selected_voice, speed)
    cached_audio = load_from_cache(cache_key)

    if cached_audio:
        print(f"♻️ Usando áudio em cache: {cached_audio}")
    else:
        try:
            print("🎤 Gerando áudio, aguarde...")
            response = generate_speech(client, user_input, selected_voice, speed)
            save_to_cache(response, cache_key)
        except Exception as e:
            print(f"❌ Ocorreu um erro ao processar a solicitação: {e}")


if __name__ == "__main__":
    main()
