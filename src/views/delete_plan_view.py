from models.plan import Plan
from helpers.graphics import clear_screen, print_header

def delete_plan_view():
    while True:
        clear_screen()
        print_header("🗑️ [Deletar Plano]", "Selecione um plano para exclusão.")

        plans = Plan.list_all()
        if not plans:
            print("❌ Nenhum plano cadastrado.")
            input("Pressione Enter para voltar...")
            return

        print("\n📋 Planos disponíveis:")
        for plan in plans:
            print(f"[{plan.id}] {plan.name} - R$ {plan.monthly_price:.2f} - {plan.installment_count} parcelas")

        plan_id_input = input("\n➡️ Digite o ID do plano a ser excluído: ").strip()
        if plan_id_input == r"\c":
            print("\n✖️ Operação cancelada.")
            return

        try:
            plan_id = int(plan_id_input)
        except ValueError:
            print("❌ ID inválido.")
            input("Pressione Enter para tentar novamente...")
            continue

        selected_plan = next((p for p in plans if p.id == plan_id), None)
        if not selected_plan:
            print("❌ Plano não encontrado.")
            input("Pressione Enter para tentar novamente...")
            continue

        confirm = input(f"\n⚠️ Tem certeza que deseja excluir o plano \"{selected_plan.name}\"? (s/n): ").strip().lower()
        if confirm != 's':
            print("↩️ Exclusão cancelada.")
            input("Pressione Enter para voltar...")
            return

        selected_plan.delete()
        print(f"\n✔️ Plano \"{selected_plan.name}\" excluído com sucesso!")
        input("Pressione Enter para continuar...")
        return
