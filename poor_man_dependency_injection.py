from typing import Iterable
import pyodbc


class Customer:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'{self.__class__.__name__}, {self.name}'


class CustomersRepository:
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def get_all(self) -> Iterable[Customer]:
        connection = pyodbc.connect(self._connection_string)
        customers = connection.execute("SELECT Name FROM Customers").fetchall()
        return [Customer(c[0]) for c in customers]


class CustomersService:
    def __init__(self, customers_repository: CustomersRepository):
        self._customers_repository = customers_repository

    def get_all(self) -> Iterable[Customer]:
        return self._customers_repository.get_all()


def main():
    # Poor Man's Dependency Injection
    connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=(LocalDB)\MSSQLLocalDB;DATABASE=DependencyInjector;Trusted_Connection=Yes;"
    customers_service = CustomersService(
        customers_repository=CustomersRepository(
            connection_string=connection_string))

    for customer in customers_service.get_all():
        print(customer)


if __name__ == '__main__':
    main()
