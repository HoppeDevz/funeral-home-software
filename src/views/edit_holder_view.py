from models.holder import Holder
from helpers.graphics import clear_screen, print_header

def edit_holder_view():
    
    while True:
        clear_screen()
        print_header("✏️ [Editar Titular]", "Edite os dados de um titular existente.")

        query = input("➡️ Digite o nome (ou parte do nome) do titular: ").strip()
        if query == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return

        holders = Holder.search_by_name(query)
        if not holders:
            print("\n❌ Nenhum titular encontrado.")
            input("Pressione Enter para tentar novamente...")
            continue

        print("\n📋 Titulares encontrados:")
        for holder in holders:
            print(f"[{holder.id}] {holder.name}")

        holder_id_input = input("\n➡️ Digite o ID do titular que deseja editar: ").strip()
        if holder_id_input == r"\c":
            print("\n✖️ Operação cancelada.")
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

        clear_screen()
        print_header(f"✏️ Editando Titular: {selected_holder.name}", "Deixe em branco para manter o valor atual.")

        new_name = input(f"➡️ Novo nome completo (atual: {selected_holder.name}): ").strip()
        if new_name == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return
        if new_name:
            selected_holder.name = new_name

        new_cpf = input(f"➡️ Novo CPF (atual: {selected_holder.cpf}): ").strip()
        if new_cpf == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return
        if new_cpf:
            if validate_cpf(new_cpf):
                selected_holder.cpf = new_cpf
            else:
                print("❌ CPF inválido. Mantendo o valor atual.")

        new_rg = input(f"➡️ Novo RG (atual: {selected_holder.rg}): ").strip()
        if new_rg == r"\c":
            print("\n✖️ Operação cancelada.")
            return
        if new_rg:
            selected_holder.rg = new_rg
    
        new_birthdate = input(f"➡️ Nova data de nascimento (dd/mm/aaaa) (atual: {selected_holder.birth_date}): ").strip()
        if new_birthdate == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return
        if new_birthdate:
            if validate_date(new_birthdate):
                selected_holder.birth_date = new_birthdate
            else:
                print("❌ Data inválida. Mantendo o valor atual.")

        new_phone = input(f"➡️ Novo telefone (atual: {selected_holder.phone}): ").strip()
        if new_phone == r"\c":
            print("\n✖️ Operação cancelada.")
            #input("Pressione Enter para continuar...")
            return
        if new_phone:
            selected_holder.phone = new_phone

        print("\n📋 Confirme os dados atualizados:")
        print(f"Nome: {selected_holder.name}")
        print(f"CPF: {selected_holder.cpf}")
        print(f"Data de nascimento: {selected_holder.birth_date}")
        print(f"Telefone: {selected_holder.phone}")
        print(f"Endereço: {selected_holder.address}")

        confirm = input("\n➡️ Confirmar alterações? (s/n): ").strip().lower()
        if confirm == r"\c" or confirm != 's':
            print("\n↩️ Edição cancelada ou não confirmada.")
            input("Pressione Enter para voltar...")
            return

        selected_holder.update()
        print("\n✔️ Titular atualizado com sucesso!")
        input("Pressione Enter para continuar...")
        break
