import os

from datetime import datetime
from pathlib import Path
from openpyxl import Workbook

from models.plan import Plan
from models.contract import Contract
from models.holder import Holder

from helpers.graphics import clear_screen, print_header

def list_holders_in_arrears_view():
    clear_screen()
    print_header("🔹 [10] Listar titulares em atraso", "Visualize titulares com parcelas em atraso por plano.")

    plans = Plan.list_all()
    if not plans:
        print("❌ Nenhum plano cadastrado disponível.")
        input("Pressione Enter para continuar...")
        return

    print("📋 Planos disponíveis:")
    for p in plans:
        print(f"[{p.id}] {p.name} - {p.installment_count} parcelas - R$ {p.monthly_price:.2f}")

    plan_id_input = input("\n➡️ Digite o ID do plano para verificar atraso: ").strip()
    if plan_id_input == r"\c":
        print("\n✖️ Operação cancelada")
        return

    try:
        plan_id = int(plan_id_input)
    except ValueError:
        print("❌ ID do plano inválido.")
        input("Pressione Enter para continuar...")
        return

    selected_plan = next((p for p in plans if p.id == plan_id), None)
    if not selected_plan:
        print("❌ Plano não encontrado.")
        input("Pressione Enter para continuar...")
        return

    contracts = Contract.list_by_plan(plan_id)
    if not contracts:
        print("❌ Nenhum contrato encontrado para este plano.")
        input("Pressione Enter para continuar...")
        return

    today = datetime.now()
    holders_in_arrears = []

    for contract in contracts:
        creation_dt = datetime.strptime(contract.creation_date, "%d/%m/%Y")

        months_passed = (today.year - creation_dt.year) * 12 + (today.month - creation_dt.month)
        if today.day >= contract.payment_day:
            months_passed += 1
        months_passed = min(months_passed, selected_plan.installment_count)

        if contract.installments_paid < months_passed:
            holder = Holder.get_by_id(contract.holder_id)
            holders_in_arrears.append({
                "holder": holder,
                "contract": contract,
                "expected_paid": months_passed,
                "actual_paid": contract.installments_paid,
            })

    clear_screen()
    print_header(f"Titulares em atraso no plano {selected_plan.name}", "")

    if not holders_in_arrears:
        print("Nenhum titular em atraso encontrado.")
    else:
        # Criar planilha Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Em Atraso"

        ws.append([
            "Nome do Titular", "Contrato ID", "Parcelas Pagas",
            "Esperadas", "Data de Criação", "Dia do Pagamento"
        ])

        for entry in holders_in_arrears:
            h = entry["holder"]
            c = entry["contract"]
            ws.append([
                h.name,
                c.id,
                entry["actual_paid"],
                entry["expected_paid"],
                c.creation_date,
                c.payment_day
            ])

        documents_path = Path.home() / "Documents"
        filename = f"Titulares_em_Atraso_{selected_plan.name}_{today.strftime('%Y-%m-%d')}.xlsx"
        output_path = documents_path / filename

        wb.save(output_path)
        os.startfile(output_path)

        print(f"✔️ {len(holders_in_arrears)} titulares em atraso encontrados.")
        print(f"📁 Planilha gerada com sucesso: {output_path}")

    input("\nPressione Enter para continuar...")
