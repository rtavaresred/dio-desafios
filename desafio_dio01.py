import textwrap
import time

# CONFIGURAÇÕES GERAIS

BANCO_VERSION = "v0.1.2"
BANCO_NAME = "Banco Dio"
AGENCIA = "0001"
TENTATIVAS_SENHA = 3
LIMITE_SAQUES = 3

# VARIÁVEIS DO SISTEMA

usuarios = []
contas = []

input_geral = "Digite a opção desejada > "
saques_realizados = 0 

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
    print("[4] Acessar Conta")
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

def selecionar_conta(usuario):
    contas_usuario = [c for c in contas if c["usuario"] == usuario]

    if not contas_usuario:
        print("❌ Nenhuma conta encontrada. Crie uma conta primeiro.")
        input("\nPressione [ENTER] para continuar...")
        return None
    
    if len(contas_usuario) == 1:
        return contas_usuario[0]
    
    print(line('SELECIONAR UMA CONTA'))
    print("\nUsuário possui várias contas,\nselecione uma conta para entrar:\n")

    for i, conta in enumerate(contas_usuario, 1):
        print(f"[{i}] Agência {conta['agencia']} - Conta {conta['numero']}")
    print()
    escolha = int(input("Escolha a conta: "))
    return contas_usuario[escolha - 1] if 1 <= escolha <= len(contas_usuario) else None

def menu_conta(usuario, conta):
    print(line(f"Agência: {conta['agencia']} | Conta: {conta['numero']}"))
    print(line(f'{usuario['nome'].upper()}',simbolo=' '))
    print()
    print("[1] Exibir Extrato")
    print("[2] Depositar")
    print("[3] Sacar")
    print("[0] Sair da Conta\n")
    print(line())
    return input("Digite a opção desejada > ")

def exibir_extrato(conta):
    print(line(F"EXTRATO"))
    print()
    print(f"👤 Usuário: {conta['usuario']['nome']}")
    print(f"🏦 Agência: {conta['agencia']}")
    print(f"💳 Conta: {conta['numero']}")
    print(line(simbolo='-'))
    if not conta["extrato"]:
        print("Nenhuma movimentação.")
    else:
        for mov in conta["extrato"]:
            print(mov)
    print(line(simbolo='-'))
    print(f"💰 Saldo atual: R$ {conta['saldo']:.2f}")
    print(line())
    input("\nPressione [ENTER] para continuar...")

def depositar(conta):
    valor = input("Informe o valor: ").replace(",", ".")
    valor = float(valor)
    if valor <= 0:
        print("❌ Valor inválido.")
        input("\nPressione [ENTER] para continuar...")
        return
    
    conta['saldo'] += valor
    conta['extrato'].append(f"➕ Crédito: R$ {valor:.2f}")

    print(f"\n✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
    time.sleep(2)
    
def sacar(conta):
    valor = input("Informe o valor: ").replace(",", ".")
    valor = float(valor)
    if valor <= 0:
        print("❌ Valor inválido.")
        time.sleep(2)
        return
    
    if valor > conta['saldo']:
        print('🚫 Saldo insuficiente.')
        time.sleep(2)
        return
    
    conta['saldo'] -= valor
    conta['extrato'].append(f"➖ Débito:  R$ {valor:.2f}")

    print(f"\n✅ Saque de R$ {valor:.2f} realizado com sucesso!")
    time.sleep(2)

def main():
    saques_realizados = 0

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
            print(line('ACESSAR CONTA'))
            print()
            cpf = input("Informe seu CPF: ")
            usuario = buscar_usuario(cpf)

            if not usuario:
                print("❌ Nenhuma conta encontrada. Crie uma conta primeiro.")
                input("\nPressione [ENTER] para continuar...")
                continue
            
            tentativas = 0

            while tentativas < TENTATIVAS_SENHA:
                senha = input("Informe sua senha: ")
                print()
                if usuario['senha'] == senha:
                    break
                tentativas += 1

                if tentativas < TENTATIVAS_SENHA:
                    restantes = TENTATIVAS_SENHA - tentativas
                    print(f"❌ Senha incorreta. Você ainda tem {restantes} tentativa{'s' if restantes > 1 else ''}.\n")
                else:
                    print("🚫 Acesso bloqueado por tentativas inválidas.")
                    input("\nPressione [ENTER] para continuar...")
                    usuario = None  # força o cancelamento do login
                    break

            if not usuario or tentativas == TENTATIVAS_SENHA:
                continue
            
            conta = selecionar_conta(usuario)
            if not conta:
                continue

            # Agora o usuário está logado
            while True:
                print()
                opcao_conta = menu_conta(usuario, conta)
                print(line())
                print()

                if opcao_conta == "1":
                    exibir_extrato(conta)
                elif opcao_conta == "2":
                    depositar(conta)
                elif opcao_conta == "3":
                    if saques_realizados >= LIMITE_SAQUES:
                        print("🚫 Limite de 3 saques por sessão atingido.")
                        input("\nPressione [ENTER] para continuar...")
                        continue
                    sacar(conta)
                    saques_realizados += 1

                elif opcao_conta == "0":
                    print(f"Saindo da conta {conta['numero']}...\n")
                    break
                else:
                    print("❌ Opção inválida.")
                    input("\nPressione [ENTER] para continuar...")

        else:
            print(f"Não existe opção {opcao}, por favor digite entre 0 a 4.")

        time.sleep(2)
        print()

print(f'\nIniciando o sistema do {BANCO_NAME}... Aguarde...')
time.sleep(1)
print()
main()