from models.plan import Plan
from helpers.graphics import clear_screen, print_header

def create_plan_view():

    while True:
        clear_screen()
        print_header("🔹 [3] Criar plano", "Cadastre um modelo genérico de plano com valor e parcelas.")

        name = input("➡️ Nome do plano: ").strip()
        if name == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return
        if not name:
            print("❌ Nome do plano é obrigatório.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header("🔹 [3] Criar plano", "Cadastre um modelo genérico de plano com valor e parcelas.")
        print(f"Nome do plano: {name}")

        preco_str = input("➡️ Preço da mensalidade (R$): ").strip().replace(',', '.')
        if preco_str == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return
        try:
            preco = float(preco_str)
            if preco <= 0:
                raise ValueError()
        except ValueError:
            print("❌ Preço inválido. Informe um número maior que zero.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header("🔹 [3] Criar plano", "Cadastre um modelo genérico de plano com valor e parcelas.")
        print(f"Nome do plano: {name}")
        print(f"Preço da mensalidade: R$ {preco:.2f}")

        parcelas_str = input("➡️ Quantidade de parcelas: ").strip()
        if parcelas_str == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return
        try:
            parcelas = int(parcelas_str)
            if parcelas <= 0:
                raise ValueError()
        except ValueError:
            print("❌ Quantidade de parcelas inválida. Informe um número inteiro maior que zero.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header("🔹 [3] Criar plano", "Cadastre um modelo genérico de plano com valor e parcelas.")
        print(f"\n📋 Confirmar os dados abaixo:\n")
        print(f"Nome do plano: {name}")
        print(f"Preço da mensalidade: R$ {preco:.2f}")
        print(f"Quantidade de parcelas: {parcelas}")

        confirm = input("\n➡️ Confirmar cadastro? (s/n): ").strip().lower()
        if confirm == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return
        if confirm == 's':
            plan = Plan(name=name, monthly_price=preco, installment_count=parcelas)
            plan.create()
            print(f"\n✔️ Plano \"{name}\" cadastrado com sucesso! ID: {plan.id}")
            input("\nPressione Enter para continuar...")
            break
        else:
            print("\n↩️ Cadastro não confirmado. Recomeçando...")
            input("Pressione Enter para reiniciar o formulário...")
