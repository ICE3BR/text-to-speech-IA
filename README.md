# 🎙️ Text-to-Speech IA (Lyra Speech)

**Converta texto em áudio de forma eficiente e flexível usando a API da OpenAI.**\
Este projeto permite a conversão de texto para fala, suportando múltiplas vozes, modelos e personalização de velocidade.

---

## 🚀 **Recursos**

✅ **Conversão de texto para áudio:** usando a API da OpenAI\
✅ **Vozes personalizáveis:** (`echo`, `alloy`, `fable`, `onyx`, e mais)\
✅ **Escolha do modelo OpenAI:** (`tts-1`, `tts-1-hd`)\
✅ **Velocidade de fala ajustável:** (`0.25x` até `4.0x`)\
✅ **Cache de áudios:** para evitar chamadas repetidas à API\
✅ **Segurança:** Chave da API armazenada no `keyring` ou `.env`\
✅ **Interface interativa:** via `InquirerPy`

---

## 📌 **Pré-requisitos**

✅ **Gerenciador de pacotes** [UV](https://docs.astral.sh/uv/) para instalação eficiente\

Antes de começar, instale os seguintes pacotes no seu ambiente Python:

```sh
uv sync
```

> **Nota:** Este projeto requer **Python 3.9+**.

---

## 🔧 **Configuração**

### **1️⃣ Obtendo a Chave da API OpenAI**

- Crie uma conta em [OpenAI](https://platform.openai.com/signup).
- Gere uma **API Key** em: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).

### **2️⃣ Salvando a API Key no Keyring (Recomendado)**

Execute o arquivo `manage_keyring.py` para armazenar a chave da API no keyring:

Ou se preferir, use o `.env` para armazenar a chave:

```env
OPENAI_API_KEY = "SUA_CHAVE_AQUI"
```

---

## 🛠 **Como Usar**

Execute o script principal:

```sh
python main.py
```

O programa guiará você por um **menu interativo** para selecionar **voz, modelo e velocidade**.

1️⃣ **Escolha a voz:**\
🎤 `echo` | 🎤 `alloy` | 🎤 `fable` | 🎤 `onyx`

2️⃣ **Escolha o modelo OpenAI:**\
🤖 `tts-1` (barato) | 🤖 `tts-1-hd` (qualidade superior)

3️⃣ **Digite a velocidade da fala:**\
⚡ Entre **`0.25`** e **`4.0`** (padrão: `1`)

4️⃣ **Insira o texto para conversão**

---

## 📂 **Onde os arquivos são salvos?**

Os áudios são gerados na **pasta do projeto**, dentro de `downloads_ia/`:

```
📂 text-to-speech-IA/
 ├── 📂 downloads_ia/
 │   ├── audio_1.mp3
 │   ├── audio_2.mp3
 ├── main.py
 ├── config.py
 ├── README.md
```

Se o mesmo texto for solicitado novamente, o **cache será usado** para evitar nova cobrança.

---

## 🎯 **Exemplo de Uso**

```sh
python main.py
```

🎙️ **Saída esperada no terminal:**

```
🎤 Escolha uma voz: [echo, alloy, fable, onyx, ...]
🛠 Escolha um modelo: [tts-1, tts-1-hd]
⚡ Digite a velocidade da fala (Padrão: 1 | 0.25 - 4.0): 1.2
📝 Digite o texto a ser falado: Olá, seja bem-vindo ao Lyra Speech!
🎵 Áudio salvo em downloads_ia/audio_1234.mp3
```

✅ **Agora o áudio está pronto para reprodução!**

---

## 🛠 **Configuração Avançada**

Se desejar personalizar os valores padrão, edite o **`config.py`**:

```python
# Configurações do projeto

# Modelos disponíveis
MODELS = {
    "tts-1": "Menor qualidade | barato",
    "tts-1-hd": "Maior qualidade | 2x mais caro",
}

# Vozes disponíveis
VOICES = ["echo", "alloy", "fable", "onyx", "ash", "coral", "nova", "sage", "shimmer"]

# Configurações padrões
DEFAULT_MODEL = "tts-1"
DEFAULT_VOICE = "echo"
DEFAULT_SPEED = 1
DEFAULT_FORMAT = "mp3"

# Pasta onde os áudios serão armazenados
DOWNLOAD_FOLDER = "downloads_ia"
```

Alterar esses valores atualizará o **comportamento padrão** do programa.

---

## ❌ **Erros Comuns e Soluções**

### **1️⃣ "A chave da API não foi encontrada no keyring nem no .env."**

💡 **Solução:** Configure a API Key no `keyring` ou no `.env`.

### **2️⃣ "Erro ao processar a solicitação na OpenAI."**

💡 **Solução:** Verifique sua **conexão com a internet** e se sua **API Key é válida**.

### **3️⃣ "Velocidade inválida! Insira um valor entre 0.25 e 4.0."**

💡 **Solução:** O valor deve ser um **número decimal** entre `0.25` a `4.0`.

---

## 📜 **Licença**

Este projeto é licenciado sob a **MIT License**.\
Sinta-se à vontade para usá-lo e melhorá-lo!

🔗 **Repositório GitHub:** [Text-to-Speech IA](https://github.com/ICE3BR/text-to-speech-IA)
