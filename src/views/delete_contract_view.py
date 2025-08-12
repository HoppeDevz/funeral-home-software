from models.holder import Holder
from models.contract import Contract
from helpers.graphics import clear_screen, print_header

def delete_contract_view():
    while True:
        clear_screen()
        print_header("🗑️ [Deletar Contrato]", "Selecione um titular e um contrato para exclusão.")

        query = input("➡️ Digite o nome (ou parte do nome) do titular: ").strip()
        if query == r"\c":
            print("\n✖️ Operação cancelada.")
            return

        holders = Holder.search_by_name(query)
        if not holders:
            print("❌ Nenhum titular encontrado.")
            input("Pressione Enter para tentar novamente...")
            continue

        print("\n📋 Titulares encontrados:")
        for index, holder in enumerate(holders):
            print(f"[{index + 1}] {holder.name} - CPF: {holder.cpf}")
        
        holder_id_input = input("\n➡️ Digite o ID do titular: ").strip()
        if holder_id_input == r"\c":
            print("\n✖️ Operação cancelada.")
            return

        try:

            holder_id = int(holder_id_input)

            if holder_id <= 0 or holder_id > len(holders):
                print("\n❌ ID deve ser maior que 0 e menor ou igual a", len(holders))
                input("Pressione Enter para tentar novamente...")
                continue

        except ValueError:
            print("❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_holder = holders[holder_id - 1] #next((h for h in holders if h.id == holder_id), None)
        if not selected_holder:
            print("❌ Titular não encontrado.")
            input("Pressione Enter para tentar novamente...")
            continue

        contracts = Contract.list_by_holder(holder_id)
        if not contracts:
            print(f"\n❌ O titular '{selected_holder.name}' não possui contratos.")
            input("Pressione Enter para continuar...")
            return

        clear_screen()
        print_header(f"🗑️ Contratos de {selected_holder.name}", "Escolha o contrato que deseja excluir.")

        for index, conctract in enumerate(contracts):
            print(f"[{index + 1}] Plano: {conctract.plan_name} - R$ {conctract.monthly_price:.2f} - Parcelas pagas: {conctract.installments_paid}")

        contract_id_input = input("\n➡️ Digite o ID do contrato a ser excluído: ").strip()
        if contract_id_input == r"\c":
            print("\n✖️ Operação cancelada.")
            return

        try:

            contract_id = int(contract_id_input)
        
            if contract_id <= 0 or contract_id > len(contracts):
                print("\n❌ ID deve ser maior que 0 e menor ou igual a", len(contracts))
                input("Pressione Enter para tentar novamente...")
                continue

        except ValueError:
            print("❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_contract = contracts[contract_id - 1] #next((c for c in contracts if c.id == contract_id), None)
        if not selected_contract:
            print("❌ Contrato não encontrado.")
            input("Pressione Enter para tentar novamente...")
            continue

        confirm = input(f"\n⚠️ Tem certeza que deseja excluir o contrato ID {selected_contract.id}? (s/n): ").strip().lower()
        if confirm != "s":
            print("↩️ Exclusão cancelada.")
            input("Pressione Enter para voltar...")
            return

        selected_contract.delete()
        print(f"\n✔️ Contrato ID {selected_contract.id} excluído com sucesso!")
        input("Pressione Enter para continuar...")
        return
