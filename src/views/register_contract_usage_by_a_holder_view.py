from models.holder import Holder
from models.contract import Contract
from models.usage_contract_holder import UsageContractHolder
from models.usage_contract_dependent import UsageContractDependent
from models.dependent import Dependent

from helpers.graphics import clear_screen, print_header
from helpers.validations import validate_date

def register_contract_usage_by_a_holder_view():
    while True:
        clear_screen()
        print_header("🔹 [13] Registrar uso de contrato por titular", "Registre o uso do contrato pelo titular")

        query = input("➡️ Digite o nome (ou parte do nome) do titular: ").strip()
        if query == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return

        holders = Holder.search_by_name(query)
        if not holders:
            print("\n❌ Nenhum titular encontrado com esse nome.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header("🔹 [13] Registrar uso de contrato por titular", "Titulares encontrados:")

        for holder in holders:
            print(f"[{holder.id}] {holder.name}")

        raw_holder_id = input("\n➡️ Digite o ID do titular: ").strip()
        if raw_holder_id == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return

        try:
            holder_id = int(raw_holder_id)
        except ValueError:
            print("\n❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_holder = next((h for h in holders if h.id == holder_id), None)
        if not selected_holder:
            print("\n❌ Titular não encontrado na lista.")
            input("Pressione Enter para tentar novamente...")
            continue

        contracts = Contract.list_by_holder(holder_id)
        if not contracts:
            print(f"\n❌ Nenhum contrato encontrado para o titular {selected_holder.name}.")
            input("Pressione Enter para voltar...")
            return

        dependents_by_id = {d.id: d.name for d in Dependent.list_by_holder(holder_id)}

        contract_usage_map = {}
        for contract in contracts:
            usage_holder = UsageContractHolder.list_by_contract(contract.id)
            usage_dependents = UsageContractDependent.list_by_contract(contract.id)

            if usage_holder:
                contract_usage_map[contract.id] = f"Já usado pelo titular {usage_holder.holder_name}"
            elif usage_dependents:
                dep_name = dependents_by_id.get(usage_dependents.dependent_id, "Dependente desconhecido")
                contract_usage_map[contract.id] = f"Já usado pelo dependente {dep_name}"
            else:
                contract_usage_map[contract.id] = None

        clear_screen()
        print_header("🔹 [13] Registrar uso de contrato por titular", f"Contratos do titular {selected_holder.name}:")

        for contract in contracts:
            usage_msg = contract_usage_map.get(contract.id)
            if usage_msg:
                print(f"[{contract.id}] Plano: {contract.plan_name} | {usage_msg}")
            else:
                print(f"[{contract.id}] Plano: {contract.plan_name}")

        while True:
            raw_contract_id = input("\n➡️ Digite o ID do contrato: ").strip()
            if raw_contract_id == r"\c":
                print("\n✖️ Operação cancelada.")
                #input("Pressione Enter para continuar...")
                return

            try:
                contract_id = int(raw_contract_id)
            except ValueError:
                print("\n❌ ID inválido.")
                continue

            if contract_id not in [c.id for c in contracts]:
                print("\n❌ Contrato não encontrado na lista.")
                continue

            if contract_usage_map.get(contract_id) is not None:
                print("\n❌ Este contrato já foi usado e não pode ser selecionado.")
                continue

            selected_contract = next(c for c in contracts if c.id == contract_id)
            break

        while True:
            usage_date = input("\n📅 Data do uso (dd/mm/aaaa): ").strip()
            if usage_date == r"\c":
                print("\n✖️ Operação cancelada.")
                #input("Pressione Enter para continuar...")
                return
            if not validate_date(usage_date):
                print("\n❌ Data inválida. Use o formato dd/mm/aaaa.")
                continue
            break

        usage = UsageContractHolder(
            holder_id=holder_id,
            contract_id=contract_id,
            usage_date=usage_date
        )
        usage.create()

        print("\n✔️ Uso registrado com sucesso.")
        input("\nPressione Enter para continuar...")
        break
