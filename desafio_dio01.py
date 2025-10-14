import textwrap
import time

# CONFIGURAÇÕES GERAIS

BANCO_NAME = "Banco Crowex"
AGENCIA = "0001"
BANCO_VERSION = "v0.1"

# VARIÁVEIS DO SISTEMA

input_geral = "Digite a opção desejada > "

# FUNÇÕES

def linha(texto: str = "", tamanho: int = 40, simbolo: str = "=") -> str:
    if not texto:
        return simbolo * tamanho

    texto_formatado = f"[ {texto} ]"
    sobra = tamanho - len(texto_formatado)

    if sobra < 0:
        texto_formatado = texto_formatado[:tamanho]
        sobra = 0

    lado_esq = sobra // 2
    lado_dir = sobra - lado_esq
    return f"{simbolo * lado_esq}{texto_formatado}{simbolo * lado_dir}"

def menu_principal():
    print(linha(f'{BANCO_NAME} {BANCO_VERSION}') + '\n')
    print("[1] Criar Usuário")
    print("[2] Abrir Conta")
    print("[3] Listar Contas")
    print("[4] Entrar na Conta")
    print("[0] Sair do Sistema")
    print()
    print(linha())
    return input(input_geral)

def main():
    while True:
        opcao = menu_principal()

        print(linha() + '\n')
        time.sleep(1)

        if opcao == "0":
            print(f"Saindo do {BANCO_NAME}...\n")
            time.sleep(2)
            print(f"{BANCO_NAME} agradece, volte sempre...\n")
            break

        if opcao == "1":
            print(linha('CRIAR USUÁRIO'))
            print('> Entrou no opção [1]')

        elif opcao == "2":
            print(linha('ABRIR CONTA'))
            print('> Entrou no opção [2]')

        elif opcao == "3":
            print(linha('LISTAR CONTAS'))
            print('> Entrou no opção [3]')

        elif opcao == "4":
            print(linha('ENTRAR NA CONTA'))
            print('> Entrou no opção [4]')
            
        else:
            print(f"Não existe opção {opcao}, por favor digite entre 0 a 4.")

        time.sleep(2)
        print()

print('\nIniciando o sistema do banco... Aguarde...')
time.sleep(1)
print()
main()