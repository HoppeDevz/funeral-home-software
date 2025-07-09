import os
import sys
import fitz

from pathlib import Path
from datetime import datetime

from models.dependent import Dependent, RELATION_MAP
from models.holder import Holder
from models.contract import Contract
from models.plan import Plan

from helpers.graphics import clear_screen, print_header

def print_pdf(path_pdf):
    os.startfile(path_pdf)

def fill_template_pdf(holder, dependents, plan, contract) -> str:

    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # template_path = os.path.join(current_dir, "..", "data", "front.pdf")
    # template_back = os.path.join(current_dir, "..", "data", "back.pdf")

    template_path = os.path.join(sys._MEIPASS, "data", "front.pdf")
    template_back = os.path.join(sys._MEIPASS, "data", "back.pdf")

    # Gera nome baseado na data e hora atual
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Contrato_{timestamp}.pdf"

    # Caminho da pasta Documents do usuário
    documents_folder = Path.home() / "Documents"
    output_path = documents_folder / filename

    # Preenche a frente
    doc = fitz.open(template_path)
    page = doc[0]

    page.insert_text((100, 145), f"{holder.name}", fontsize=8)
    page.insert_text((190, 158), f"{holder.cpf}", fontsize=8)
    page.insert_text((400, 159), f"{holder.rg}", fontsize=8)
    page.insert_text((469, 146), f"{holder.birth_date}", fontsize=8)
    page.insert_text((105, 170), f"{holder.address}", fontsize=8)
    page.insert_text((417, 171), f"{holder.neighborhood}", fontsize=8)
    page.insert_text((94, 185),  f"{holder.zipcode}", fontsize=8)
    page.insert_text((195, 185), f"{holder.city}", fontsize=8)
    page.insert_text((440, 185), f"{holder.phone}", fontsize=8)

    page.insert_text((450, 96), f"{contract.id}", fontsize=18)
    page.insert_text((365, 128), f"{plan.name}", fontsize=18)

    # page.insert_text((91, 900), f"Valor da mensalidade: R$ {plan.monthly_price:.2f}", fontsize=10)
    # page.insert_text((91, 408), f"Número de parcelas: {plan.installment_count}", fontsize=10)
    # page.insert_text((91, 426), f"Dia de vencimento: {contract.payment_day}", fontsize=10)

    for dependent in dependents:

        if dependent.relation == 1:
            page.insert_text((110, 210), f"{dependent.name}", fontsize=10)

        if dependent.relation == 2:
            page.insert_text((115, 228), f"{dependent.name}", fontsize=10)

        if dependent.relation == 3:
            page.insert_text((130, 246), f"{dependent.name}", fontsize=10)

        if dependent.relation == 4:
            page.insert_text((130, 265), f"{dependent.name}", fontsize=10)

        if dependent.relation == 5:
            page.insert_text((150, 283), f"{dependent.name}", fontsize=10)

        if dependent.relation == 6:
            page.insert_text((130, 300), f"{dependent.name}", fontsize=10)

    others = [dependent.name for dependent in dependents if dependent.relation == 0]
    others_str = ", ".join(others)

    if others_str:
        page.insert_text((92, 315), f"Outros dependentes: {others_str}", fontsize=10)

    # Salva frente temporária
    temp_path = os.path.join(sys._MEIPASS, "contrato_frente_temp.pdf")
    #temp_path = os.path.join(current_dir, "contrato_frente_temp.pdf")
    doc.save(temp_path)
    doc.close()

    # Junta frente + verso
    front = fitz.open(temp_path)
    back = fitz.open(template_back)

    page_back = back[0]
    page_back.insert_text((315, 273), f"{plan.monthly_price:.2f}", fontsize=10)

    final = fitz.open()
    final.insert_pdf(front)
    final.insert_pdf(back)

    final.save(output_path)
    final.close()
    front.close()

    os.remove(temp_path)

    return str(output_path)

    
def print_contract_view():

    while True:
        clear_screen()
        print_header("🔹 [14] Imprimir contrato", "Selecione um titular e contrato para gerar o PDF.")

        query = input("➡️ Digite o nome (ou parte do nome) do titular: ").strip()
        if query == r"\c":
            print("\n✖️ Operação cancelada.")
            return

        holders = Holder.search_by_name(query)

        if not holders:
            print("\n❌ Nenhum titular encontrado com esse nome.")
            input("Pressione Enter para tentar novamente...")
            continue

        clear_screen()
        print_header("🔹 [14] Imprimir contrato", "Titulares encontrados:")
        for holder in holders:
            print(f"[{holder.id}] {holder.name}")

        raw_holder_id = input("\n➡️ Digite o ID do titular: ").strip()
        if raw_holder_id == r"\c":
            print("\n✖️ Operação cancelada.")
            return

        try:
            holder_id = int(raw_holder_id)
        except ValueError:
            clear_screen()
            print("\n❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_holder = next((h for h in holders if h.id == holder_id), None)
        if not selected_holder:
            clear_screen()
            print("\n❌ Titular não encontrado na lista.")
            input("Pressione Enter para tentar novamente...")
            continue

        contracts = Contract.list_by_holder(holder_id)
        if not contracts:
            clear_screen()
            print(f"\n❌ Nenhum contrato encontrado para {selected_holder.name}.")
            input("Pressione Enter para continuar...")
            return

        clear_screen()
        print_header("🔹 [14] Imprimir contrato", f"Contratos de {selected_holder.name}:")
        for c in contracts:
            print(f"[{c.id}] Plano: {c.plan_name} - R$ {c.monthly_price:.2f} - Parcelas pagas: {c.installments_paid}")

        raw_contract_id = input("\n➡️ Digite o ID do contrato: ").strip()
        if raw_contract_id == r"\c":
            print("\n✖️ Operação cancelada.")
            return

        try:
            contract_id = int(raw_contract_id)
        except ValueError:
            clear_screen()
            print("\n❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_contract = next((c for c in contracts if c.id == contract_id), None)
        if not selected_contract:
            clear_screen()
            print("\n❌ Contrato não encontrado na lista.")
            input("Pressione Enter para tentar novamente...")
            continue

        dependents = Dependent.list_by_holder(selected_holder.id)
        plan = Plan.get_by_id(selected_contract.plan_id)
        output_path = fill_template_pdf(selected_holder, dependents, plan, selected_contract)

        print_pdf(output_path)
        
        clear_screen()
        print_header("🔹 [14] Imprimir contrato", "Arquivo gerado com sucesso!")

        print(f"\n✔️ Contrato gerado com sucesso: {output_path}")
        input("\nPressione Enter para continuar...")
        break
