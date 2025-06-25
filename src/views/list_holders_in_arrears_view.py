from datetime import datetime

from models.plan import Plan
from models.contract import Contract
from models.holder import Holder

from helpers.graphics import clear_screen, print_header

def list_holders_in_arrears_view():
    clear_screen()
    print_header("🔹 [11] Listar titulares em atraso", "Visualize titulares com parcelas em atraso por plano.")

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
        # Parse creation_date dd/mm/yyyy para datetime
        creation_dt = datetime.strptime(contract.creation_date, "%d/%m/%Y")

        # Calcular quantas parcelas deveriam estar pagas até hoje
        months_passed = (today.year - creation_dt.year) * 12 + (today.month - creation_dt.month)
        # Adiciona +1 se o dia do pagamento já passou no mês atual
        if today.day >= contract.payment_day:
            months_passed += 1
        # Limita ao total de parcelas do plano
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
        for idx, entry in enumerate(holders_in_arrears, 1):
            h = entry["holder"]
            c = entry["contract"]
            print(f"[{idx}] {h.name} (Contrato ID: {c.id})")
            print(f"    Parcelas pagas: {entry['actual_paid']} / Esperadas até hoje: {entry['expected_paid']}")
            print(f"    Data de criação: {c.creation_date}")
            print(f"    Dia do pagamento: {c.payment_day}")
            print()

    input("Pressione Enter para continuar...")
