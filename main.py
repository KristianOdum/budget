from arguments import Arguments
from data_processing import *
from importer import import_data
import log_setup
from transaction import Transaction, Category, get_timespan_months

log = log_setup.getLogger("budget_main")


def main():
    args = Arguments()

    transactions: list[Transaction] = import_data(
        args.dir,
        filter_name=args.filter_name,
        filter_category=args.filter_category,
        filter_description=args.filter_description,
        exclude_name=args.exclude_name,
        exclude_category=args.exclude_category,
        exclude_description=args.exclude_description,
    )

    if not transactions:
        log.info("No transactions")
        return

    expenses: dict[Category, float] = aggregate_by_category(transactions)
    inflated_expenses = inflate_linked_categories(expenses)
    num_months: float = get_timespan_months(transactions)

    # List description -> category
    if args.matches:
        list_category_matchings(transactions)

    if args.pretty_print_categories:
        pretty_print_expenses_with_subcats(inflated_expenses, num_months)

    if args.luksus_faelden:
        print_overview_budget(inflated_expenses, num_months)

    if args.disposable_income:
        print_disposable_income(inflated_expenses, num_months)

if __name__ == "__main__":
    main()
