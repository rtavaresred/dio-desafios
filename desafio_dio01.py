import textwrap
import time

# CONFIGURAÇÕES GERAIS

BANCO_NAME = "Banco Crowex"
AGENCIA = "0001"
BANCO_VERSION = "v0.1.1"

# VARIÁVEIS DO SISTEMA

usuarios = []
contas = []

input_geral = "Digite a opção desejada > "

# FUNÇÕES

def line(texto: str = "", tamanho: int = 40, simbolo: str = "=") -> str:
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
    print(line(f'{BANCO_NAME} {BANCO_VERSION}') + '\n')
    print("[1] Criar Usuário")
    print("[2] Abrir Conta")
    print("[3] Listar Contas")
    print("[4] Entrar na Conta")
    print("[0] Sair do Sistema")
    print()
    print(line())
    return input(input_geral)

def buscar_usuario(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_usuario(cpf: str = ""):
    if cpf:
        verificar_cpf = input(f"Deseja continuar o CPF informado: {cpf}? [s/n]: ")

        if verificar_cpf.lower() == 'n':
            cpf = input("Informe o CPF (somente números): ")
    else:
        cpf = input("Informe o CPF (somente números): ")

    if buscar_usuario(cpf):
        print("❌ Já existe usuário com esse CPF.")
        input("\nPressione [ENTER] para continuar...")
        return
    
    nome = input("Nome completo: ").title()
    senha = input("Crie uma senha (mínimo de 6): ")

    while True:
        if len(senha) < 6:
            print("❌ Senha não aceita, crie uma senha com mínimo de 6.")
            senha = input("> ")
            continue
        else:
            break

    logradouro = input("Logradouro: ").title()
    numero = input("Número: ").title()
    bairro = input("Bairro: ").title()
    cidade = input("Cidade: ").title()
    estado = input("Estado: ").upper()

    while True:
        if len(estado) != 2:
            print("❌ Use sigla do estado, por exemplo: SP")
            estado = input("Sigla do estado > ").upper()
            continue
        else:
            break

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"
    usuarios.append({"nome": nome, "cpf": cpf, "senha": senha, "endereco": endereco})

    print(f"\n✅ Usuário {nome} criado com sucesso!")
    print(f"📇 Endereço: {endereco}")
    input("\nPressione [ENTER] para continuar...")

def criar_conta():
    cpf = input("Informe o CPF do usuário: ")
    usuario = buscar_usuario(cpf)

    if not usuario:
        print("❌ Usuário não está cadastrado no sistema. Crie novo usuário.")
        return
    
    numero_conta = len(contas) + 1
    contas.append({
        "agencia": AGENCIA,
        "numero": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": []
    })

    print(f"\n✅ Conta {numero_conta} criada para {usuario['nome'].upper()} com sucesso!")
    input("\nPressione [ENTER] para continuar...")

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        print()
        print(line())
        input("\nPressione [ENTER] para continuar...")
        return
    
    for conta in contas:
        print(line(simbolo="-"))
        linha = f"Agência: {conta['agencia']} | Conta: {conta['numero']}\nTitular: {conta['usuario']['nome']}"
        print(textwrap.dedent(linha))
    print(line(simbolo="-"))

    print()
    print(line())

    input("\nPressione [ENTER] para continuar...")


def main():
    while True:
        opcao = menu_principal()

        print(line() + '\n')
        time.sleep(1)

        if opcao == "0":
            print(f"Saindo do {BANCO_NAME}...\n")
            time.sleep(2)
            print(f"{BANCO_NAME} agradece, volte sempre...\n")
            break

        if opcao == "1":
            print(line('CRIAR USUÁRIO'))
            print()
            criar_usuario()

        elif opcao == "2":
            print(line('ABRIR CONTA'))
            print()
            criar_conta()

        elif opcao == "3":
            print(line('LISTAR CONTAS'))
            print()
            listar_contas()

        elif opcao == "4":
            print(line('ENTRAR NA CONTA'))
            print('> Entrou no opção [4]')

        else:
            print(f"Não existe opção {opcao}, por favor digite entre 0 a 4.")

        time.sleep(2)
        print()

print('\nIniciando o sistema do banco... Aguarde...')
time.sleep(1)
print()
main()