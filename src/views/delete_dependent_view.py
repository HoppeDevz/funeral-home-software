from models.holder import Holder
from models.dependent import Dependent
from helpers.graphics import clear_screen, print_header

def delete_dependent_view():
    while True:
        clear_screen()
        print_header("🗑️ [Deletar Dependente]", "Selecione um titular para ver e excluir seus dependentes.")

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

        dependents = Dependent.list_by_holder(holder_id)
        if not dependents:
            print(f"\n❌ O titular '{selected_holder.name}' não possui dependentes.")
            input("Pressione Enter para continuar...")
            return

        clear_screen()
        print_header(f"🗑️ Dependentes de {selected_holder.name}", "Escolha qual deseja excluir.")

        for index, dependent in enumerate(dependents):
            print(f"[{index + 1}] {dependent.name} (Relação: {dependent.relation})")

        dependent_id_input = input("\n➡️ Digite o ID do dependente a ser excluído: ").strip()
        if dependent_id_input == r"\c":
            print("\n✖️ Operação cancelada.")
            return

        try:

            dependent_id = int(dependent_id_input)

            if dependent_id <= 0 or dependent_id > len(dependents):
                print("\n❌ ID deve ser maior que 0 e menor ou igual a", len(dependents))
                input("Pressione Enter para tentar novamente...")
                continue

        except ValueError:
            print("❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_dependent = dependents[dependent_id - 1] #next((d for d in dependents if d.id == dependent_id), None)
        if not selected_dependent:
            print("❌ Dependente não encontrado.")
            input("Pressione Enter para tentar novamente...")
            continue

        confirm = input(f"\n⚠️ Tem certeza que deseja excluir o dependente '{selected_dependent.name}'? (s/n): ").strip().lower()
        if confirm != "s":
            print("↩️ Exclusão cancelada.")
            input("Pressione Enter para voltar...")
            return

        Dependent.delete(dependent_id)
        print(f"\n✔️ Dependente '{selected_dependent.name}' excluído com sucesso!")
        input("Pressione Enter para continuar...")
        return
