from helpers.graphics import clear_screen

from views.create_holder_view import create_holder_view
from views.create_dependent_view import create_dependent_view
from views.create_plan_view import create_plan_view
from views.create_contract_view import create_contract_view

from views.list_holders_view import list_holders_view
from views.list_holder_dependents_view import list_holder_dependents_view
from views.list_holder_contracts_view import list_holder_contracts_view
from views.list_holders_in_arrears_view import list_holders_in_arrears_view

from views.increment_installments_paid_view import increment_installments_paid_view

from views.register_contract_usage_by_a_dependent_view import register_contract_usage_by_a_dependent_view
from views.register_contract_usage_by_a_holder_view import register_contract_usage_by_a_holder_view

from views.edit_plan_view import edit_plan_view
from views.edit_holder_view import edit_holder_view


class View:
    @staticmethod
    def start():
        while True:
            clear_screen()
            print("╔" + "═" * 60 + "╗")
            print("║{:^60}║".format("Sistema Funerária"))
            print("╠" + "═" * 60 + "╣")
            print("║ {:<2} - {:<54}║".format("1",       "Criar novo titular"))
            print("║ {:<2} - {:<54}║".format("2",       "Criar dependente"))
            print("║ {:<2} - {:<54}║".format("3",       "Criar plano"))
            print("║ {:<2} - {:<54}║".format("4",       "Criar contrato"))
            print("║ {:<2} - {:<54}║".format("5",       "Editar titular"))
            print("║ {:<2} - {:<54}║".format("6",       "Editar Plano"))
            print("║ {:<2} - {:<54}║".format("7",       "Listar titulares"))
            print("║ {:<2} - {:<54}║".format("8",       "Listar dependentes de um titular"))
            print("║ {:<2} - {:<54}║".format("9",       "Listar contratos de um titular"))
            print("║ {:<2} - {:<54}║".format("10",      "Listar titulares em atraso"))
            print("║ {:<2} - {:<54}║".format("11",      "Dar baixa em parcelas de um contrato"))
            print("║ {:<2} - {:<54}║".format("12",      "Registrar uso de contrato por dependente"))
            print("║ {:<2} - {:<54}║".format("13",      "Registrar uso de contrato por titular"))
            print("║ {:<2} - {:<54}║".format("14",      "Imprimir contrato"))
            #print("║ {:<2} - {:<54}║".format("0",   "Sair"))
            print("╚" + "═" * 60 + "╝")

            option = input("\nEscolha uma opção: ").strip()

            if option == '1':
                create_holder_view()
            elif option == '2':
                create_dependent_view()
            elif option == '3':
                create_plan_view()
            elif option == '4':
                create_contract_view()
            elif option == '5':
                edit_plan_view()
            elif option == '6':
                edit_holder_view()
            elif option == '7':
                list_holders_view()
            elif option == '8':
                list_holder_dependents_view()
            elif option == '9':
                list_holder_contracts_view()
            elif option == '10':
                list_holders_in_arrears_view()
            elif option == '11':
                increment_installments_paid_view()
            elif option == '12':
                register_contract_usage_by_a_dependent_view()
            elif option == '13':
                register_contract_usage_by_a_holder_view()
            
            else:
                print("\nOpção inválida, tente novamente.")
                input("Pressione Enter para continuar...")
