from pathlib import Path, PurePath

from matching import transfer_to_category
from transaction import Transfer, Transaction, Category
import log_setup

log = log_setup.getLogger('importer')

DATA_DIR = r"C:\Users\kristian\Desktop\budget\data"


def import_data(
        data_dir: Path,
        filter_name: list[str] | None = None,
        filter_category: list[Category] | None = None,
        filter_description: list[str] | None = None,
        exclude_name: list[str] | None = None,
        exclude_category: list[Category] | None = None,
        exclude_description: list[str] | None = None,
) -> list[Transaction]:
    log.debug(f"Importing data from '{data_dir}'")
    assert data_dir.exists(), f"Data path '{data_dir}' does not exist"

    transactions = []

    for file in data_dir.iterdir():
        if file.suffix != ".csv":
            log.debug(f"Skipping non-csv file '{file.name}'")
            continue

        log.debug(f"Loading data from '{file.name}'")
        file_transactions = []

        # Read owner/name
        owner: str = owner_from_filename(file)
        # Apply filter
        if filter_name and not any(owner in name for name in filter_name):
            continue
        if exclude_name and any(owner in name for name in exclude_name):
            continue

        for line in file.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            # Read transfer
            transfer = Transfer.from_csv_line(line.strip())
            # Apply filter
            description = transfer.description
            if filter_description and not any(desc in description for desc in filter_description):
                continue
            if exclude_description and any(desc in description for desc in exclude_description):
                continue

            # Read category
            category = transfer_to_category(transfer, owner)
            # Apply filter
            if filter_category and not any(category in cat for cat in filter_category):
                continue
            if exclude_category and any(category in cat for cat in exclude_category):
                continue

            # Create result
            transaction = Transaction(transfer=transfer, category=category, owner=owner)

            # Add to transactions for given file
            file_transactions.append(transaction)

        transactions += file_transactions
        log.info(f"Loaded {len(file_transactions)} from '{file.name}'")

    log.info(f"Imported a total of {len(transactions)} transactions")

    return transactions


def owner_from_filename(path: PurePath) -> str:
    return path.stem.split("_")[0]
