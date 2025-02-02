import hashlib
import os
from pathlib import Path

from dotenv import load_dotenv
from InquirerPy import prompt
from openai import OpenAI

# Carregar variáveis do .env
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("A chave da API não está configurada no arquivo .env.")

client = OpenAI(api_key=API_KEY)

# Configurações de modelos e vozes
MODELS = {
    "tts-1": "Menor qualidade | barato",
    "tts-1-hd": "Maior qualidade | 2x mais caro",
}
VOICES = ["echo", "alloy", "fable", "onyx"]

# Diretório para salvar os áudios
download_dir = Path("downloads_ia")
download_dir.mkdir(exist_ok=True)


# Funções Auxiliares
def get_cache_key(text, voice, speed):
    """Gera uma chave única para cada combinação de texto, voz e velocidade."""
    key = f"{text}-{voice}-{speed}"
    return hashlib.md5(key.encode()).hexdigest()


def load_from_cache(cache_key, download_dir):
    """Verifica se o arquivo de áudio já foi gerado anteriormente."""
    cache_file = download_dir / f"{cache_key}.mp3"
    if cache_file.exists():
        print(f"Áudio encontrado no cache: {cache_file}")
        return cache_file
    return None


def save_to_cache(response, cache_key, download_dir):
    """Salva o áudio gerado no cache para reutilização futura."""
    cache_file = download_dir / f"{cache_key}.mp3"
    with open(cache_file, "wb") as f:
        f.write(response.content)
    print(f"Áudio salvo no cache: {cache_file}")
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


def escolher_opcao(menu):
    """Exibe um menu interativo para o usuário selecionar uma opção."""
    result = prompt(menu)
    return result[menu[0]["name"]]  # Correção aplicada


def main():
    # Menu para seleção de voz
    menu_voz = [
        {
            "type": "list",
            "name": "voice",
            "message": "Escolha uma voz do menu:",
            "choices": VOICES + ["Sair"],
        },
    ]

    selected_voice = escolher_opcao(menu_voz)
    if selected_voice == "Sair":
        print("Saindo...")
        return

    # Menu para seleção de modelo
    menu_model = [
        {
            "type": "list",
            "name": "model",
            "message": "Escolha um modelo do menu:",
            "choices": list(MODELS.keys()) + ["Sair"],
        },
    ]

    selected_model = escolher_opcao(menu_model)
    if selected_model == "Sair":
        print("Saindo...")
        return

    # Exibindo as escolhas
    print(f"Voz escolhida: {selected_voice}")
    print(f"Modelo escolhido: {selected_model} ({MODELS[selected_model]})")

    # Solicitar texto ao usuário
    user_input = input("Digite o texto a ser falado: ")
    if not user_input:
        user_input = "Bem vindo, ao Lyra_Speech! Como posso ajudar você hoje?"

    # Verificar no cache antes de gerar o áudio
    cache_key = get_cache_key(user_input, selected_voice, 0.96)
    cached_audio = load_from_cache(cache_key, download_dir)

    if cached_audio:
        print(f"Usando áudio em cache: {cached_audio}")
    else:
        try:
            # Gerar o áudio usando a API da OpenAI
            response = generate_speech(client, user_input, selected_voice, 0.96)
            save_to_cache(response, cache_key, download_dir)
        except Exception as e:
            print(f"Ocorreu um erro ao processar a solicitação: {e}")


if __name__ == "__main__":
    main()
