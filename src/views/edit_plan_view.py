from models.plan import Plan
from helpers.graphics import clear_screen, print_header

def edit_plan_view():
    while True:
        clear_screen()
        print_header("✏️ [Editar Plano]", "Edite os dados de um plano existente.")

        query = input("➡️ Digite o nome (ou parte do nome) do plano: ").strip()
        if query == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return

        plans = Plan.search_by_name(query)
        if not plans:
            print("\n❌ Nenhum plano encontrado.")
            input("Pressione Enter para tentar novamente...")
            continue

        print("\n📋 Planos encontrados:")
        for index, plan in enumerate(plans):
            print(f"[{index + 1}] {plan.name} - R$ {plan.monthly_price:.2f} - {plan.installment_count} parcelas")

        plan_id_input = input("\n➡️ Digite o ID do plano que deseja editar: ").strip()
        if plan_id_input == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return

        try:

            plan_id = int(plan_id_input)

            if plan_id <= 0 or plan_id > len(plans):
                print("\n❌ ID deve ser maior que 0 e menor ou igual a", len(plans))
                input("Pressione Enter para tentar novamente...")
                continue

        except ValueError:
            print("❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_plan = plans[plan_id - 1] #next((p for p in plans if p.id == plan_id), None)
        if not selected_plan:
            print("❌ Plano não encontrado na lista.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header(f"✏️ Editando Plano: {selected_plan.name}", "Deixe em branco para manter o valor atual.")

        new_name = input(f"➡️ Novo nome (atual: {selected_plan.name}): ").strip()
        if new_name == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return
        if new_name:
            selected_plan.name = new_name

        new_price_str = input(f"➡️ Novo preço mensal (atual: R$ {selected_plan.monthly_price:.2f}): ").strip().replace(',', '.')
        if new_price_str == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return
        if new_price_str:
            try:
                new_price = float(new_price_str)
                if new_price <= 0:
                    raise ValueError()
                selected_plan.monthly_price = new_price
            except ValueError:
                print("❌ Preço inválido. Mantendo valor atual.")

        new_installments_str = input(f"➡️ Nova quantidade de parcelas (atual: {selected_plan.installment_count}): ").strip()
        if new_installments_str == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return
        if new_installments_str:
            try:
                new_installments = int(new_installments_str)
                if new_installments <= 0:
                    raise ValueError()
                selected_plan.installment_count = new_installments
            except ValueError:
                print("❌ Quantidade inválida. Mantendo valor atual.")

        # Confirmar alterações
        print("\n📋 Confirme os dados atualizados:")
        print(f"Nome: {selected_plan.name}")
        print(f"Preço mensal: R$ {selected_plan.monthly_price:.2f}")
        print(f"Quantidade de parcelas: {selected_plan.installment_count}")

        confirm = input("\n➡️ Confirmar alterações? (s/n): ").strip().lower()
        if confirm == r"\c" or confirm != 's':
            print("\n↩️ Edição cancelada ou não confirmada.")
            input("Pressione Enter para voltar...")
            return

        selected_plan.update()
        print("\n✔️ Plano atualizado com sucesso!")
        input("Pressione Enter para continuar...")
        break
