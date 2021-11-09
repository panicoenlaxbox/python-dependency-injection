from typing import List

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
import pyodbc


class Customer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.__class__.__name__}, {self.name}'


class CustomersRepository:
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def get_all(self) -> List[Customer]:
        connection = pyodbc.connect(self._connection_string)
        customers = connection.execute("SELECT * FROM Customers").fetchall()
        return [Customer(c[1]) for c in customers]


class CustomersService:
    def __init__(self, customers_repository: CustomersRepository):
        self._customers_repository = customers_repository

    def get_all(self) -> List[Customer]:
        return self._customers_repository.get_all()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    customers_repository = providers.Singleton(
            CustomersRepository,
            connection_string=config.connection_string)

    customers_service = providers.Singleton(
        CustomersService,
        customers_repository=customers_repository)


@inject
def main(customers_service: CustomersService = Provide[Container.customers_service]):
    for customer in customers_service.get_all():
        print(customer)


if __name__ == '__main__':
    container = Container()
    container.config.connection_string.from_value("DRIVER={ODBC Driver 17 for SQL Server};SERVER=(LocalDB)\MSSQLLocalDB;DATABASE=DependencyInjector;Trusted_Connection=Yes;")
    container.wire(modules=[__name__])

    main()
