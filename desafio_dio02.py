from abc import ABC, abstractmethod
from datetime import datetime
import time
import textwrap

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================
BANCO_NAME = "Banco Dio"
BANCO_VERSION = "v3.0.0"
AGENCIA_PADRAO = "0001"
LIMITE_SAQUES = 3


# ==========================================================
# CLASSES DO SISTEMA
# ==========================================================
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = AGENCIA_PADRAO
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    def sacar(self, valor):
        if valor <= 0:
            print("❌ Valor inválido para saque.")
            return False
        if valor > self._saldo:
            print("🚫 Saldo insuficiente.")
            return False
        self._saldo -= valor
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("❌ Valor inválido para depósito.")
            return False
        self._saldo += valor
        print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)


# class ContaCorrente(Conta):
#     def __init__(self, numero, cliente, limite=500, limite_saques=LIMITE_SAQUES):
#         super().__init__(numero, cliente)
#         self._limite = limite
#         self._limite_saques = limite_saques
#         self._saques_realizados = 0

#     def sacar(self, valor):
#         if self._saques_realizados >= self._limite_saques:
#             print("🚫 Limite de saques atingido.")
#             return False
#         if valor <= 0:
#             print("❌ Valor inválido para saque.")
#             return False
#         # agora valida saldo + limite
#         if valor > (self._saldo + self._limite):
#             print("🚫 Saldo + limite insuficiente.")
#             return False

#         self._saldo -= valor
#         self._saques_realizados += 1
#         print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
#         return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=3, limite_saques=LIMITE_SAQUES):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0

    def sacar(self, valor):
        # 1) controla quantidade de saques
        if self._saques_realizados >= self._limite_saques:
            print("🚫 Limite de saques atingido.")
            return False

        # 2) usa a lógica de saque da classe-mãe (valida >0 e >saldo)
        sucesso = super().sacar(valor)

        # 3) se deu certo, contabiliza o saque
        if sucesso:
            self._saques_realizados += 1

        return sucesso


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco, senha):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._senha = senha

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    @property
    def senha(self):
        return self._senha


# ==========================================================
# FUNÇÕES AUXILIARES (MENU)
# ==========================================================
clientes = []

def line(texto: str = "", tamanho: int = 40, simbolo: str = "=") -> str:
    if not texto:
        return simbolo * tamanho
    texto_formatado = f"[ {texto} ]"
    sobra = tamanho - len(texto_formatado)
    lado_esq = sobra // 2
    lado_dir = sobra - lado_esq
    return f"{simbolo * lado_esq}{texto_formatado}{simbolo * lado_dir}"


def buscar_cliente_por_cpf(cpf):
    for c in clientes:
        if c.cpf == cpf:
            return c
    return None


def menu_principal():
    print()
    print(line(f"{BANCO_NAME} {BANCO_VERSION}") + "\n")
    print("[1] Criar Cliente")
    print("[2] Criar Conta")
    print("[3] Acessar Conta")
    print("[0] Sair\n")
    return input("Escolha uma opção > ")

# ==========================================================
# FUNÇÃO PRINCIPAL (INTERFACE)
# ==========================================================
def main():
    numero_conta = 1

    while True:
        opcao = menu_principal()
        print()

        if opcao == "0":
            print("Encerrando o sistema...\n")
            time.sleep(1)
            break

        elif opcao == "1":
            print(line("CRIAR CLIENTE"))
            cpf = input("CPF: ")
            if buscar_cliente_por_cpf(cpf):
                print("❌ Já existe cliente com esse CPF.")
                continue
            nome = input("Nome completo: ").title()
            data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
            endereco = input("Endereço: ")
            senha = input("Crie uma senha: ")
            cliente = PessoaFisica(nome, cpf, data_nasc, endereco, senha)
            clientes.append(cliente)
            print(f"✅ Cliente {nome} criado com sucesso!")

        elif opcao == "2":
            print(line("CRIAR CONTA"))
            cpf = input("CPF do cliente: ")
            cliente = buscar_cliente_por_cpf(cpf)
            if not cliente:
                print("❌ Cliente não encontrado.")
                continue
            conta = ContaCorrente(numero_conta, cliente)
            cliente.adicionar_conta(conta)
            numero_conta += 1
            print(f"✅ Conta {conta.numero} criada para {cliente.nome}.")

        elif opcao == "3":
            print(line("ACESSAR CONTA"))
            cpf = input("CPF: ")
            cliente = buscar_cliente_por_cpf(cpf)
            if not cliente:
                print("❌ Cliente não encontrado.")
                continue
            senha = input("Senha: ")
            if senha != cliente.senha:
                print("❌ Senha incorreta.")
                continue

            if not cliente.contas:
                print("❌ Cliente não possui contas.")
                continue

            conta = cliente.contas[0]  # usa a primeira conta
            while True:
                print()
                print(line(f"{cliente.nome.upper()} - CONTA {conta.numero}"))
                print("[1] Exibir Extrato")
                print("[2] Depositar")
                print("[3] Sacar")
                print("[0] Sair da Conta\n")
                escolha = input("> ")
                print()

                if escolha == "1":
                    print(line("EXTRATO"))
                    if not conta.historico.transacoes:
                        print('Não há histórico de transações.')
                    else:
                        for t in conta.historico.transacoes:
                            print(f"{t['data']} | {t['tipo']} | R$ {t['valor']:.2f}")
                    print(line(simbolo='-'))
                    print(f"Saldo atual: R$ {conta.saldo:.2f}\n")
                    input("Pressione ENTER para continuar...")

                elif escolha == "2":
                    valor = float(input("Valor do depósito: ").replace(",", "."))
                    deposito = Deposito(valor)
                    cliente.realizar_transacao(conta, deposito)

                elif escolha == "3":
                    valor = float(input("Valor do saque: ").replace(",", "."))
                    saque = Saque(valor)
                    cliente.realizar_transacao(conta, saque)

                elif escolha == "0":
                    print("Saindo da conta...\n")
                    break
                else:
                    print("Opção inválida.")

        else:
            print("❌ Opção inválida.")
        time.sleep(1)


# ==========================================================
# EXECUÇÃO DO SISTEMA
# ==========================================================
if __name__ == "__main__":
    print(f"\nIniciando o sistema do {BANCO_NAME}...")
    time.sleep(1)
    main()