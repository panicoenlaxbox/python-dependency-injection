from typing import Iterable
import pyodbc


class Customer:
    def __str__(self):
        return f'{self.__class__.__name__}, {self.name}'


class CustomersRepository:
    @staticmethod
    def get_all():
        connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=(LocalDB)\MSSQLLocalDB;DATABASE=DependencyInjector;Trusted_Connection=Yes;"
        connection = pyodbc.connect(connection_string)
        rows = connection.execute("SELECT Name FROM Customers").fetchall()
        customers = []
        for row in rows:
            customer = Customer()
            customer.name = row[0]
            customers.append(customer)
        return customers


class CustomersService:
    @staticmethod
    def get_all():
        customers_repository = CustomersRepository()
        return customers_repository.get_all()


def main():
    customers_service = CustomersService()

    for customer in customers_service.get_all():
        print(customer)


if __name__ == '__main__':
    main()
