import textwrap

def exibir_menu():
    menu_opcoes = """\n
    ================ MENU PRINCIPAL ================
    [d]\tAdicionar saldo
    [r]\tRetirar saldo
    [v]\tVer movimentações
    [cc]\tCriar nova conta
    [ac]\tExibir contas cadastradas
    [cu]\tCadastrar novo usuário
    [s]\tSair
    => """
    return input(textwrap.dedent(menu_opcoes))

def adicionar_saldo(saldo, valor, historico, /):
    if valor > 0:
        saldo += valor
        historico += f"Crédito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito bem-sucedido! ===")
    else:
        print("\n@@@ Depósito falhou! Valor inválido. @@@")

    return saldo, historico

def retirar_saldo(*, saldo, valor, historico, limite, saques_realizados, max_saques):
    saldo_insuficiente = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = saques_realizados >= max_saques

    if saldo_insuficiente:
        print("\n@@@ Falha! Saldo insuficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Falha! Valor excede o limite permitido. @@@")
    elif excedeu_saques:
        print("\n@@@ Falha! Limite de saques atingido. @@@")
    elif valor > 0:
        saldo -= valor
        historico += f"Débito:\t\tR$ {valor:.2f}\n"
        saques_realizados += 1
        print("\n=== Saque bem-sucedido! ===")
    else:
        print("\n@@@ Falha! Valor informado é inválido. @@@")

    return saldo, historico

def mostrar_historico(saldo, /, *, historico):
    print("\n================ MOVIMENTAÇÕES ================")
    print("Nenhuma transação realizada." if not historico else historico)
    print(f"\nSaldo atual:\tR$ {saldo:.2f}")
    print("===============================================")

def criar_usuario(usuarios):
    cpf = input("Digite o CPF (apenas números): ")
    usuario_existente = buscar_usuario(cpf, usuarios)

    if usuario_existente:
        print("\n@@@ Usuário já cadastrado com este CPF! @@@")
        return

    nome = input("Digite o nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (rua, número, bairro, cidade/estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário cadastrado com sucesso! ===")

def buscar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite o CPF do usuário: ")
    usuario = buscar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ CPF não cadastrado, criação de conta abortada! @@@")

def exibir_contas(contas):
    for conta in contas:
        detalhes_conta = f"""\
            Agência:\t{conta['agencia']}
            Número:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(detalhes_conta))

def iniciar_sistema():
    LIMITE_SAQUES = 3
    AGENCIA = "1234"

    saldo = 0
    limite = 500
    historico = ""
    saques_realizados = 0
    usuarios = []
    contas = []

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            valor = float(input("Valor a ser depositado: "))
            saldo, historico = adicionar_saldo(saldo, valor, historico)

        elif opcao == "r":
            valor = float(input("Valor a ser retirado: "))
            saldo, historico = retirar_saldo(
                saldo=saldo,
                valor=valor,
                historico=historico,
                limite=limite,
                saques_realizados=saques_realizados,
                max_saques=LIMITE_SAQUES,
            )

        elif opcao == "v":
            mostrar_historico(saldo, historico=historico)

        elif opcao == "cu":
            criar_usuario(usuarios)

        elif opcao == "cc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "ac":
            exibir_contas(contas)

        elif opcao == "s":
            break

        else:
            print("Opção inválida. Tente novamente.")

iniciar_sistema()
