from models.holder import Holder
from models.contract import Contract
from models.plan import Plan
from models.usage_contract_holder import UsageContractHolder
from models.usage_contract_dependent import UsageContractDependent
from models.dependent import Dependent
from helpers.graphics import clear_screen, print_header

def list_holder_contracts_view():
    while True:
        clear_screen()
        print_header("🔹 [7] Listar contratos de um titular", "Visualize os contratos ativos de um titular.")

        query = input("➡️ Digite o nome (ou parte do nome) do titular: ").strip()
        if query == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        holders = Holder.search_by_name(query)
        if not holders:
            print("❌ Nenhum titular encontrado.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header("🔹 [7] Listar contratos de um titular", "Titulares encontrados:")

        print("\n📋 Titulares encontrados:")
        for holder in holders:
            print(f"[{holder.id}] {holder.name}")

        raw_holder_id = input("\n➡️ Digite o ID do titular: ").strip()
        if raw_holder_id == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        try:
            holder_id = int(raw_holder_id)
        except ValueError:
            print("❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_holder = next((h for h in holders if h.id == holder_id), None)
        if not selected_holder:
            print("❌ Titular não encontrado na lista.")
            input("Pressione Enter para tentar novamente...")
            continue

        contracts = Contract.list_by_holder(holder_id)

        clear_screen()
        print_header("🔹 [7] Listar contratos de um titular", f"Contratos de {selected_holder.name}:")

        print(f"\n📄 Contratos de {selected_holder.name}:")
        if not contracts:
            print("Nenhum contrato encontrado para este titular.")
        else:
            dependents_by_id = {d.id: d.name for d in Dependent.list_by_holder(holder_id)}

            for idx, contract in enumerate(contracts, 1):
                plan = Plan.get_by_id(contract.plan_id)
                usage_holder = UsageContractHolder.list_by_contract(contract.id)
                usage_dependents = UsageContractDependent.list_by_contract(contract.id)

                print(f"[{idx}] Plano: {plan.name} - R$ {float(plan.monthly_price):.2f}")
                print(f"    Dia do pagamento: {contract.payment_day}")
                print(f"    Data de criação: {contract.creation_date}")
                print(f"    Parcelas pagas: {contract.installments_paid} / Quantidade de parcelas: {plan.installment_count}")

                if usage_holder or usage_dependents:
                    print("    Foi usado: Sim")
                    print("    Usuários que usaram:")

                    if usage_holder:
                        print(f"      - Titular ({usage_holder.usage_date})")

                    if usage_dependents:
                        name = dependents_by_id.get(usage_dependents.dependent_id, "Dependente desconhecido")
                        print(f"      - {name} (dependente) ({usage_dependents.usage_date})")

                else:
                    print("    Foi usado: Não")
                print()

        input("Pressione Enter para continuar...")
        break
