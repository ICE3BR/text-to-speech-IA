# Gerenciador de credenciais de chave para autenticação que se integra com o gerenciador de senhas nativo do sistema operacional
# uv add keyring
"""
🔐 O que é keyring?
O keyring é uma biblioteca Python que permite armazenar e recuperar credenciais de maneira segura, utilizando o gerenciador de credenciais do próprio sistema operacional.
Isso significa que você não precisa armazenar senhas ou chaves de API no código ou em arquivos .env, tornando sua aplicação mais segura contra vazamentos.
"""
import keyring
from InquirerPy import prompt

menu_voz = [
    {
        "type": "list",
        "name": "opcao",  # A chave para acessar a resposta
        "message": "Escolha uma opção do menu:",
        "choices": ["ADD", "Remove", "List", "Sair"],
    },
]

while True:
    result = prompt(menu_voz)
    escolha = result["opcao"]  # Acessando a escolha do usuário
    match escolha:
        case (
            "ADD"
        ):  # Isso armazenará a chave de API com segurança no gerenciador do seu sistema.
            print("Opção escolhida: ADD")
            key_name = input("Digite o nome para achave: ")
            key_tipe = input("Digite o tipo da chave: ")
            key_pass = input(
                "Digite a chave: "
            )  # Substitua pelo seu valor real da chave
            try:
                keyring.set_password(
                    key_name, key_tipe, key_pass
                )  # ()"openai", "api_key", "SUA_CHAVE_AQUI")
                print("Chave salva com sucesso no keyring!")
            except Exception as e:
                print(f"Erro ao salvar a chave da API: {e}")

        case "Remove":
            print("opção escolhida: Remove")
            key_name = input("Digite o nome para achave: ")
            key_tipe = input("Digite o tipo da chave: ")
            try:
                keyring.delete_password(key_name, key_tipe)
                print("Chave removida do keyring.")
            except Exception as e:
                print(f"Erro ao remover a chave da API: {e}")

        case "List":
            print("Opção escolhida: List")
            # Codigo precisa ser feito ainda...

        case "Sair":
            print("Saindo...")
            break
