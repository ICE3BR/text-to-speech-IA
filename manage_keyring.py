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
        case "ADD":  # Armazena a chave no keyring com segurança
            print("Opção escolhida: ADD")
            key_name = input("Digite o nome do serviço: ")
            key_tipe = input("Digite o identificador da chave: ")
            key_pass = input("Digite a chave a ser armazenada: ")

            try:
                keyring.set_password(key_name, key_tipe, key_pass)
                print("🔐 Chave salva com sucesso no keyring!")
                print(f"🔑 Serviço: {key_name} | Chave: {key_tipe}")
            except Exception as e:
                print(f"❌ Erro ao salvar a chave: {e}")

        case "Remove":
            print("Opção escolhida: Remove")
            key_name = input("Digite o nome do serviço: ")
            key_tipe = input("Digite o identificador da chave: ")

            try:
                keyring.delete_password(key_name, key_tipe)
                print("🔐 Chave removida com sucesso!")
                print(f"🔑 Serviço: {key_name} | Chave: {key_tipe}")
            except Exception as e:
                print(f"❌ Erro ao remover a chave: {e}")

        case "List":
            print("🔎 Opção escolhida: Listar chaves\n")
            print(
                f"Você pode saber as chaves armazenadas no sistema operacional:\n Win + R -> rundll32.exe keymgr.dll,KRShowKeyMgr\nIsso Abre o Gerenciador de Credenciais, onde você pode visualizar e remover chaves.\n"
            )
            key_name = input("Digite o nome do serviço para listar suas chaves: ")

            # Testa algumas chaves comuns
            common_keys = ["api_key", "token", "senha", "client_secret"]
            found_keys = []

            for key_tipe in common_keys:
                try:
                    stored_value = keyring.get_password(key_name, key_tipe)
                    if stored_value:
                        found_keys.append(
                            f"🔑 {key_tipe}: {stored_value[:6]}... (oculto)"
                        )
                except Exception as e:
                    print(f"❌ Erro ao buscar a chave {key_tipe}: {e}")

            if found_keys:
                print("\n🔐 Chaves encontradas:")
                for key in found_keys:
                    print(key)
            else:
                print("❌ Nenhuma chave encontrada para esse serviço.")

        case "Sair":
            print("👋 Saindo...")
            break
