from models.holder import Holder
from models.contract import Contract
from helpers.graphics import clear_screen, print_header

def increment_installments_paid_view():

    while True:
        clear_screen()
        print_header("🔹 [11] Dar baixa em parcelas de um contrato", "Atualize o número de parcelas pagas de um contrato")
        
        query = input("➡️ Digite o nome (ou parte do nome) do titular: ").strip()
        if query == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        holders = Holder.search_by_name(query)

        if not holders:
            print("\n❌ Nenhum titular encontrado com esse nome.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header("🔹 [11] Dar baixa em parcelas de um contrato", "Atualize o número de parcelas pagas de um contrato")
        print("\n📋 Titulares encontrados:")
        for index, holder in enumerate(holders):
            print(f"[{index + 1}] {holder.name}")

        raw_holder_id = input("\n➡️ Digite o ID do titular: ").strip()
        if raw_holder_id == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        try:

            holder_id = int(raw_holder_id)

            if holder_id <= 0 or holder_id > len(holders):
                print("\n❌ ID deve ser maior que 0 e menor ou igual a", len(holders))
                input("Pressione Enter para tentar novamente...")
                continue

        except ValueError:
            print("\n❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_holder = holders[holder_id - 1] #next((h for h in holders if h.id == holder_id), None)
        if not selected_holder:
            print("\n❌ Titular não encontrado na lista.")
            input("Pressione Enter para tentar novamente...")
            continue

        contracts = Contract.list_by_holder(holder_id)

        if not contracts:
            print(f"\n❌ Nenhum contrato encontrado para o titular {selected_holder.name}.")
            input("Pressione Enter para voltar...")
            return

        clear_screen()
        print_header("🔹 [11] Dar baixa em parcelas de um contrato", f"Titular selecionado: {selected_holder.name}")
        print(f"\n📄 Contratos do titular {selected_holder.name}:")
        for index, contract in enumerate(contracts):
            print(f"[{index + 1}] Plano: {contract.plan_name} - R$ {contract.monthly_price:.2f} - {contract.installments_paid} parcelas pagas")

        raw_contract_id = input("\n➡️ Digite o ID do contrato: ").strip()
        if raw_contract_id == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        try:

            contract_id = int(raw_contract_id)

            if contract_id <= 0 or contract_id > len(contracts):
                print("\n❌ ID deve ser maior que 0 e menor ou igual a", len(contracts))
                input("Pressione Enter para tentar novamente...")
                continue

        except ValueError:
            print("\n❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_contract = contracts[contract_id - 1] #next((c for c in contracts if c.id == contract_id), None)
        if not selected_contract:
            print("\n❌ Contrato não encontrado na lista.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header("🔹 [11] Dar baixa em parcelas de um contrato", f"Titular: {selected_holder.name} - Contrato ID: {selected_contract.id}")
        print(f"\n✅ Parcelas pagas atualmente: {selected_contract.installments_paid}")

        raw_to_add = input("\n➡️ Quantas parcelas deseja adicionar? ").strip()
        if raw_to_add == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        try:
            to_add = int(raw_to_add)
            if to_add <= 0:
                raise ValueError()
        except ValueError:
            print("\n❌ Valor inválido. Deve ser um número inteiro positivo.")
            input("Pressione Enter para tentar novamente...")
            continue

        # Atualiza parcelas pagas no contrato
        selected_contract.installments_paid += to_add
        selected_contract.update()

        print(f"\n✔️ Parcelas atualizadas com sucesso para o titular {selected_holder.name}.")
        print(f"✔️ Total agora: {selected_contract.installments_paid} parcelas pagas.")
        input("\nPressione Enter para continuar...")
        break
