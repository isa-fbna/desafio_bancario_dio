from datetime import date

class Transacao:
    def registrar(self, conta):
        raise NotImplementedError("Método precisa ser implementado pelas subclasses")

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)
        print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso.")

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            print(f"Saque de R$ {self.valor:.2f} realizado com sucesso.")
        else:
            print("Operação falhou. Saque não realizado.")

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, cliente, numero, agencia):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    @staticmethod
    def nova_conta(cliente, numero, agencia):
        return Conta(cliente, numero, agencia)

    def sacar(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia):
        super().__init__(cliente, numero, agencia)
        self.limite = 500
        self.limite_saques = 3
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques < self.limite_saques and valor <= self.limite and super().sacar(valor):
            self.numero_saques += 1
            return True
        return False

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

def menu():
    return """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    => """

def main():
    cliente = PessoaFisica("João Silva", "123.456.789-00", date(1980, 5, 12), "Rua A, 123")
    conta = ContaCorrente(cliente, 12345, "0001")
    cliente.adicionar_conta(conta)

    while True:
        opcao = input(menu())
        
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            deposito = Deposito(valor)
            cliente.realizar_transacao(conta, deposito)
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saque = Saque(valor)
            cliente.realizar_transacao(conta, saque)
        elif opcao == "e":
            print("\n================ EXTRATO ================")
            if not conta.historico.transacoes:
                print("Não foram realizadas movimentações.")
            else:
                for transacao in conta.historico.transacoes:
                    tipo = "Depósito" if isinstance(transacao, Deposito) else "Saque"
                    print(f"{tipo}: R$ {transacao.valor:.2f}")
            print(f"\nSaldo: R$ {conta.saldo:.2f}")
            print("==========================================")
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
