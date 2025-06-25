from database.sqlite import Database

from models.holder_migrations import HolderMigrations
from models.dependent_migrations import HolderDependentsMigrations
from models.plan_migrations import PlanMigrations
from models.contract_migrations import ContractMigrations
from models.usage_contract_holder_migrations import UsageContractHolderMigrations
from models.usage_contract_dependent_migrations import UsageContractDependentMigrations

from views.main import View

def run_all_migrations():
    
    print("Running migrations...")

    HolderMigrations.migrate()
    HolderDependentsMigrations.migrate()
    PlanMigrations.migrate()
    ContractMigrations.migrate()
    UsageContractHolderMigrations.migrate()
    UsageContractDependentMigrations.migrate()

    View.start()


if __name__ == "__main__":
    run_all_migrations()
