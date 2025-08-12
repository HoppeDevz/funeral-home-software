from models.holder import Holder
from helpers.graphics import clear_screen, print_header

def delete_holder_view():
    while True:
        clear_screen()
        print_header("🗑️ [Deletar Titular]", "Exclua um titular permanentemente do sistema.")

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

        holder_id_input = input("\n➡️ Digite o ID do titular que deseja deletar: ").strip()
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
            print("❌ Titular não encontrado na lista.")
            input("Pressione Enter para tentar novamente...")
            continue

        confirm = input(f"\n⚠️ Tem certeza que deseja excluir '{selected_holder.name}' e todos os dados relacionados? (s/n): ").strip().lower()
        if confirm != "s":
            print("↩️ Exclusão cancelada.")
            input("Pressione Enter para voltar...")
            return

        selected_holder.delete()
        print(f"\n✔️ Titular '{selected_holder.name}' deletado com sucesso!")
        input("Pressione Enter para continuar...")
        return
