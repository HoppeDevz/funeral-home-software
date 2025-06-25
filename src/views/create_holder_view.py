from models.holder import Holder
from helpers.graphics import clear_screen, print_header

def format_cpf(cpf: str) -> str:
    nums = ''.join(filter(str.isdigit, cpf))
    return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}" if len(nums) == 11 else cpf

def create_holder_view():

    fields = [
        ("name",                "➡️ Nome completo"),
        ("birth_date",          "➡️ Data de nascimento (dd/mm/aaaa)"),
        ("marital_status",      "➡️ Estado civil (Solteiro, Casado, etc.)"),
        ("cpf",                 "➡️ CPF (somente números)"),
        ("rg",                  "➡️ RG"),
        ("address",             "➡️ Endereço (rua, número)"),
        ("neighborhood",        "➡️ Bairro"),
        ("zipcode",             "➡️ CEP"),
        ("city",                "➡️ Cidade"),
        ("phone",               "➡️ Telefone (opcional)"),
    ]

    data = {key: "" for key, _ in fields}
    idx = 0

    while True:

        clear_screen()
        print_header("🔹 [1] Criar novo titular", "Preencha os dados para cadastrar um novo titular.")

        key, label = fields[idx]
        current_value = data[key]
        prompt_text = f"{label}"
        if current_value:
            prompt_text += f" [{current_value}]"
        prompt_text += ": "

        value = input(prompt_text).strip()

        if value == r"\v":
            if idx > 0:
                idx -= 1
                continue
            else:
                continue
            

        if value == r"\c":
            print("\n\n✖️ Cadastro cancelado.")
            #input("Pressione Enter para continuar...")
            return

        if not value and not current_value and key != "phone":
            print("⚠️ Campo obrigatório. Digite um valor ou '\\c' para cancelar.")
            #input("Pressione Enter para continuar...")
            continue

        if value:
            data[key] = value

        idx += 1

        if idx == len(fields):

            clear_screen()

            print("📋 Confirmar os dados abaixo:\n")
            print(f"Nome: {data['name']}")
            print(f"Data de nascimento: {data['birth_date']}")
            print(f"Estado civil: {data['marital_status']}")
            print(f"CPF: {format_cpf(data['cpf'])}")
            print(f"RG: {data['rg']}")
            print(f"Endereço: {data['address']} – {data['neighborhood']} – {data['city']} – {data['zipcode']}")
            print(f"Telefone: {data['phone'] or '(não informado)'}")

            confirm = input("\n➡️ Confirmar cadastro? (s/n): ").strip().lower()
            if confirm == 's':
                holder = Holder(
                    name=               data['name'],
                    birth_date=         data['birth_date'],
                    marital_status=     data['marital_status'],
                    cpf=                data['cpf'],
                    rg=                 data['rg'],
                    address=            data['address'],
                    neighborhood=       data['neighborhood'],
                    zipcode=            data['zipcode'],
                    city=               data['city'],
                    phone=              data['phone']
                )
                holder.create()
                print(f"\n\n✔️ Titular cadastrado com sucesso! ID: {holder.id}")
                break
            else:
                print("\n\n↩️ Cadastro não confirmado. Recomeçando...")
                input("Pressione Enter para reiniciar o formulário...")
                idx = 0