from datetime import datetime

from transaction import Transfer
from importer import import_data


def test_from_csv_line():
    data = r"31-12-2025;Rente af indestående;2.534,48;DKK"
    transaction = Transfer.from_csv_line(data)

    assert transaction.date == datetime.strptime("31-12-2025", "%d-%m-%Y")
    assert transaction.description == "Rente af indestående"
    assert transaction.amount == 2534.48
    assert transaction.valuta == "DKK"


def test_import_data():
    transactions = import_data()
    print(transactions)



def main():
    test_from_csv_line()
    test_import_data()


if __name__ == "__main__":
    main()
