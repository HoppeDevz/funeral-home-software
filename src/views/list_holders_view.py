from models.holder import Holder
from helpers.graphics import clear_screen, print_header

def format_cpf(cpf: str) -> str:
    nums = ''.join(filter(str.isdigit, cpf))
    return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}" if len(nums) == 11 else cpf

def list_holders_view():
    while True:
        clear_screen()
        print_header("🔹 [5] Listar titulares", "Filtra e exibe titulares cadastrados pelo nome.")

        query = input("➡️ Digite o nome (ou parte do nome) do titular: ").strip()
        if query == r"\c":
            print("\n✖️ Operação cancelada")
            #input("Pressione Enter para continuar...")
            return

        if not query:
            print("⚠️ Por favor, digite algo para pesquisar.")
            input("Pressione Enter para tentar novamente...")
            continue

        holders = Holder.search_by_name(query)

        if not holders:
            print("\n❌ Nenhum titular encontrado com esse nome.")
            input("Pressione Enter para tentar novamente...")
            continue

        print("\n📋 Titulares encontrados:\n")
        for h in holders:
            print(f"Nome: {h.name}")
            print(f"Data de nascimento: {h.birth_date}")
            print(f"Estado civil: {h.marital_status}")
            print(f"CPF: {format_cpf(h.cpf)}")
            print(f"RG: {h.rg}")
            print(f"Endereço: {h.address} – {h.neighborhood} – {h.city} – {h.zipcode}")
            print(f"Telefone: {h.phone or '(não informado)'}\n")

        input("Pressione Enter para continuar...")
        break
