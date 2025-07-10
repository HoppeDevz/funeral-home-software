import os

from datetime import date, datetime
from calendar import monthrange
from pathlib import Path
from openpyxl import Workbook

from models.plan import Plan
from models.contract import Contract
from models.holder import Holder

from helpers.graphics import clear_screen, print_header

def calculate_due_installments(creation_date: date, payment_day: int, today: date, paid_installments: int) -> int:
    # Garante que today seja um objeto date (caso venha como datetime)
    if isinstance(today, datetime):
        today = today.date()

    if today < creation_date:
        return 0

    # Define o primeiro vencimento
    if creation_date.day <= payment_day:
        try:
            first_due_date = creation_date.replace(day=payment_day)
        except ValueError:
            # Se o dia não existe (ex: dia 31 em fevereiro), ajusta para o último dia do mês
            last_day = monthrange(creation_date.year, creation_date.month)[1]
            first_due_date = creation_date.replace(day=last_day)
    else:
        # Próximo mês
        year = creation_date.year + (creation_date.month // 12)
        month = (creation_date.month % 12) + 1
        try:
            first_due_date = date(year, month, payment_day)
        except ValueError:
            last_day = monthrange(year, month)[1]
            first_due_date = date(year, month, last_day)

    # Conta parcelas vencidas até hoje
    count = 0
    current_due = first_due_date

    while current_due <= today:
        count += 1
        # Próximo mês
        year = current_due.year + (current_due.month // 12)
        month = (current_due.month % 12) + 1
        try:
            current_due = date(year, month, payment_day)
        except ValueError:
            last_day = monthrange(year, month)[1]
            current_due = date(year, month, last_day)

    # Parcelas devidas = vencidas - pagas
    due_installments = count - paid_installments
    return max(due_installments, 0)


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

        creation_dt = datetime.strptime(contract.creation_date, "%d/%m/%Y").date()

        due_installments = calculate_due_installments(
            creation_date=creation_dt,
            payment_day=contract.payment_day,
            today=today,
            paid_installments=contract.installments_paid
        )

        if due_installments > 0:
            holder = Holder.get_by_id(contract.holder_id)
            holders_in_arrears.append({
                "holder": holder,
                "contract": contract,
                "expected_paid": due_installments,
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
