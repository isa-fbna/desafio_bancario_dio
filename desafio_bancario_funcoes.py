usuarios = []

def menu():
    return """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    => """

def depositar(saldo, extrato):
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso.")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def sacar(saldo, extrato, numero_saques, limite_saques, limite):
    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso.")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(nome, cpf):
    usuarios.append({'nome': nome, 'cpf': cpf})
    print(f'Usuário {nome} criado com sucesso.')

def filtrar_usuarios(cpf):
    return [usuario for usuario in usuarios if usuario['cpf'] == cpf]

def criar_conta(agencia, numero_conta, usuario_index):
    if 0 <= usuario_index < len(usuarios):
        usuario = usuarios[usuario_index]
        usuario['conta'] = {'agencia': agencia, 'numero_conta': numero_conta}
        print(f'Conta {agencia}-{numero_conta} criada para o usuário {usuario["nome"]}.')
    else:
        print('Índice de usuário inválido.')

def listar_contas(usuario_index):
    if 0 <= usuario_index < len(usuarios):
        usuario = usuarios[usuario_index]
        if 'conta' in usuario:
            print(f'Conta do usuário {usuario["nome"]}:')
            print(f'Agência: {usuario["conta"]["agencia"]}, Número da conta: {usuario["conta"]["numero_conta"]}')
        else:
            print(f'O usuário {usuario["nome"]} não possui conta.')
    else:
        print('Índice de usuário inválido.')

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = input(menu())

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques, LIMITE_SAQUES, limite)
        elif opcao == "e":
            exibir_extrato(saldo, extrato)
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
