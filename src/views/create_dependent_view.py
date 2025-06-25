from models.holder import Holder
from models.dependent import Dependent
from helpers.graphics import clear_screen, print_header

def create_dependent_view():
        
    while True:
        clear_screen()
        print_header("🔹 [2] Criar dependente", "Associe um novo dependente a um titular já cadastrado.")

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

        print("\n📋 Titulares encontrados:")
        for holder in holders:
            print(f"[{holder.id}] {holder.name}")

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

        name = input("\n➡️ Nome completo do dependente: ").strip()
        if name == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return
        if not name:
            print("❌ Nome não pode ser vazio.")
            input("Pressione Enter para tentar novamente...")
            continue

        dependent = Dependent(name=name, holder_id=holder_id)
        dependent.create()

        print(f"\n✔️ Dependente \"{name}\" vinculado ao titular {selected_holder.name} cadastrado com sucesso! ID: {dependent.id}")
        input("Pressione Enter para continuar...")
        break
