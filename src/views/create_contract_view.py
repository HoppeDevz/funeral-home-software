from datetime import datetime
from models.holder import Holder
from models.plan import Plan
from models.contract import Contract
from helpers.graphics import clear_screen, print_header

def create_contract_view():
    while True:
        clear_screen()
        print_header("🔹 [4] Criar contrato", "Selecione um titular e um plano para gerar um novo contrato.")

        # Buscar titular
        query = input("➡️ Digite o nome (ou parte do nome) do titular: ").strip()
        if query == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        holders = Holder.search_by_name(query)
        if not holders:
            print("❌ Nenhum titular encontrado com esse nome.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header("🔹 [4] Criar contrato", "Selecione um titular e um plano para gerar um novo contrato.")
        print("\n📋 Titulares encontrados:")
        for h in holders:
            print(f"[{h.id}] {h.name}")

        holder_id_input = input("\n➡️ Digite o ID do titular: ").strip()
        if holder_id_input == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        try:
            holder_id = int(holder_id_input)
        except ValueError:
            print("❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_holder = next((h for h in holders if h.id == holder_id), None)
        if not selected_holder:
            print("❌ Titular não encontrado na lista.")
            input("Pressione Enter para tentar novamente...")
            continue

        # Listar planos disponíveis
        plans = Plan.list_all()
        if not plans:
            print("❌ Nenhum plano cadastrado disponível.")
            input("Pressione Enter para voltar...")
            return

        clear_screen()
        print_header("🔹 [4] Criar contrato", "Selecione um titular e um plano para gerar um novo contrato.")
        print("\n📋 Planos disponíveis:")
        for p in plans:
            print(f"[{p.id}] {p.name} - R$ {p.monthly_price:.2f}")

        plan_id_input = input("\n➡️ Digite o ID do plano: ").strip()
        if plan_id_input == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        try:
            plan_id = int(plan_id_input)
        except ValueError:
            print("❌ ID do plano inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_plan = next((p for p in plans if p.id == plan_id), None)
        if not selected_plan:
            print("❌ Plano não encontrado na lista.")
            input("Pressione Enter para tentar novamente...")
            continue

        due_day_input = input("➡️ Dia do pagamento (1-31): ").strip()
        if due_day_input == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        try:
            due_day = int(due_day_input)
            if due_day < 1 or due_day > 31:
                raise ValueError()
        except ValueError:
            print("❌ Dia do pagamento inválido. Informe um número entre 1 e 31.")
            input("Pressione Enter para tentar novamente...")
            continue

        creation_input = input("➡️ Data de criação (dd/mm/aaaa) [Enter para hoje]: ").strip()
        if creation_input == r"\c":
            print("\n✖️ Operação cancelada")
            return

        if creation_input:
            try:
                creation_dt = datetime.strptime(creation_input, "%d/%m/%Y")
                creation_date = creation_dt.strftime("%d/%m/%Y")
            except ValueError:
                print("❌ Data inválida. Use o formato dd/mm/aaaa.")
                input("Pressione Enter para tentar novamente...")
                continue
        else:
            creation_date = datetime.now().strftime("%d/%m/%Y")

        parcels_paid_input = input("➡️ Parcelas pagas (inicialmente 0): ").strip()
        if parcels_paid_input == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        try:
            parcels_paid = int(parcels_paid_input)
            if parcels_paid < 0:
                raise ValueError()
        except ValueError:
            print("❌ Número de parcelas pagas inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header("🔹 [4] Criar contrato", "Confirme os dados abaixo")
        print(f"Titular: {selected_holder.name}")
        print(f"Plano: {selected_plan.name} - R$ {selected_plan.monthly_price:.2f}")
        print(f"Dia do pagamento: {due_day}")
        print(f"Data de criação: {creation_date}")
        print(f"Parcelas pagas: {parcels_paid}")

        confirm = input("\n➡️ Confirmar cadastro? (s/n): ").strip().lower()
        if confirm == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return
        if confirm == 's':
            contract = Contract(
                holder_id=holder_id,
                plan_id=plan_id,
                payment_day=due_day,
                creation_date=creation_date,
                installments_paid=parcels_paid
            )
            contract.create()
            print(f"\n✔️ Contrato do plano \"{selected_plan.name}\" vinculado ao titular {selected_holder.name} cadastrado com sucesso! ID: {contract.id}")
            input("\nPressione Enter para continuar...")
            break
        else:
            print("\n↩️ Cadastro não confirmado. Recomeçando...")
            input("Pressione Enter para reiniciar o formulário...")
