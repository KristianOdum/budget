from transaction import Transaction, Category, category_to_pretty_dk, max_category_width, get_timespan_months, get_subcats


def aggregate_by_category(transactions: list[Transaction]) -> dict[Category, float]:
    result = {cat: 0.0 for cat in Category}

    for t in transactions:
        result[t.category] += t.transfer.amount

    return result


def list_category_matchings(transactions: list[Transaction]):
    sorted_t = sorted(transactions, key=lambda t: (t.category.value, t.transfer.description.lower(), t.transfer.amount))

    print("Listing all transactions")
    for t in sorted_t:
        print(
            f"{t.transfer.description[:50]: <50} -> {t.category.value: <{max_category_width}}"
            f" [{t.transfer.amount: 8.2f} {t.transfer.valuta} @ {t.owner} - {t.transfer.date.strftime('%Y-%m-%d')}]"
        )


def inflate_linked_categories(expenses: dict[Category, float]):
    sub_cats = get_subcats()

    inflated_expenses: dict[Category, float] = expenses.copy()
    def visit(cat: Category) -> float:
        inflated_expenses[cat] = expenses[cat] + sum([visit(sub_cat) for sub_cat in sub_cats[cat]])
        return inflated_expenses[cat]
    visit(Category.TOP)
    # print(inflated_expenses)

    return inflated_expenses


def print_overview_budget(expenses: dict[Category, float], num_months: float):
    ingoing_cats = [Category.INCOME]
    outgoing_cats = [
        Category.HOUSING,
        Category.FIXED_EXPENSES,
        Category.TRANSPORT,
        Category.FOOD_AND_HOUSEHOLD,
        Category.MISC,
        Category.DEBT,
    ]
    relevant_cats = ingoing_cats + outgoing_cats
    filtered_expenses = {cat: expenses[cat] for cat in Category if cat in relevant_cats}

    pretty_print_expenses(filtered_expenses, num_months, header="Luksusfælden Tavle")

    ingoing = int(sum(abs(expenses[cat]) for cat in ingoing_cats))
    outgoing = int(sum(abs(expenses[cat]) for cat in outgoing_cats))
    print(f"Total indtægt = {ingoing} | Måned = {int(ingoing / num_months)}")
    print(f"Total udgift  = {outgoing} | Måned = {int(outgoing / num_months)}")
    diff = int(ingoing - outgoing)
    print(f"Total diff    = {diff} | Måned = {int(diff / num_months)}")


def print_expenses(expenses: dict[Category, float], num_months: float):
    pretty_print_expenses(expenses, num_months)


def pretty_print_expenses(expenses: dict[Category, float], num_months: float, header: str = "Kategorier"):
    print()
    print()
    print(f"---- {header} ----")
    print(f'{"POST": <{max_category_width+6}}TOTAL      MÅNED')
    for cat, amount in expenses.items():
        if cat in [Category.TOP]:
            continue
        print(f"{category_to_pretty_dk(cat): <{max_category_width}} {int(amount): >10.0f} {int(amount / num_months): >10.0f}")
    print("----")


def pretty_print_expenses_with_subcats(expenses: dict[Category, float], num_months: float, header: str = "Kategorier"):
    subcats = get_subcats()

    def find_roots(tree):
        children = {c for kids in tree.values() for c in kids}
        return [n for n in tree if n not in children]

    print()
    print()
    print(f"---- {header} ----")
    print(f'{"POST": <{max_category_width+12}}TOTAL   MÅNED')

    def print_tree(tree: dict, root, prefix=""):
        children = tree.get(root, [])

        for i, child in enumerate(children):
            amount = expenses[child]
            is_last = i == len(children) - 1

            connector = "└── " if is_last else "├── "
            print(f"{prefix + connector + category_to_pretty_dk(child): <{max_category_width+8}} {int(amount): >8.0f} {int(amount / num_months): >7.0f}")


            extension = "    " if is_last else "│   "
            print_tree(tree, child, prefix + extension)

    for root in find_roots(subcats):
        amount = expenses[root]
        # if root == Category.TOP:
        #     continue
        print(f"{category_to_pretty_dk(root): <{max_category_width + 8}} {int(amount): >8.0f} {int(amount / num_months): >7.0f}")
        print_tree(subcats, root)
    # print_tree(subcats, Category.TOP)

    print("----")


def print_disposable_income(expenses: dict[Category, float], num_months: float):
    fixed_cats = [
        Category.FIXED_EXPENSES,
        Category.HOUSING,
        Category.TRANSPORT,
        Category.DEBT,
    ]

    total_fixed = sum([abs(expenses[cat]) for cat in fixed_cats])
    income = expenses[Category.INCOME]
    total_diff = income - total_fixed

    print()
    print()
    print("------------- Rådighedsbeløb -------------")
    print("POST                      TOTAL      MÅNED")
    print(f"Indtægt              {int(income): 10.0f} {int(income) / num_months: 10.0f}")
    print(f"Faste udgifter       {int(total_fixed): 10.0f} {int(total_fixed) / num_months: 10.0f}")
    print(f"Rådighedsbeløb       {int(total_diff): 10.0f} {int(total_diff) / num_months: 10.0f}")

