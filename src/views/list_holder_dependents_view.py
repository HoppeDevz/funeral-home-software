from models.holder import Holder
from models.dependent import Dependent
from helpers.graphics import clear_screen, print_header

def list_holder_dependents_view():
    while True:
        clear_screen()
        print_header("🔹 [6] Listar dependentes de um titular", "Informe o nome para localizar o titular.")

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
        print_header("🔹 [6] Listar dependentes de um titular", "Titulares encontrados:")

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

        dependents = Dependent.list_by_holder(holder_id)

        clear_screen()
        print_header("🔹 [6] Listar dependentes de um titular", f"Dependentes de {selected_holder.name}:")

        print(f"\n👨\u200d👧 Dependentes de {selected_holder.name}:")
        if not dependents:
            print("(Nenhum dependente cadastrado)")
        else:
            for idx, dep in enumerate(dependents, 1):
                print(f"[{idx}] {dep.name}")

        input("\nPressione Enter para continuar...")
        break
