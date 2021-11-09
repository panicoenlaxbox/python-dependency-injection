from unittest.mock import create_autospec, MagicMock

from assertpy import assert_that

from with_dependency_injector import Container, CustomersRepository, Customer


def test_dependency_injector():
    container = Container()
    container.wire(modules=[__name__])

    mock_customers_repository: MagicMock = create_autospec(CustomersRepository)
    mock_customers_repository.get_all.return_value = [Customer("Acme")]
    with container.customers_repository.override(mock_customers_repository):
        customers_service = container.customers_service()
        customers = customers_service.get_all()
        assert_that(customers).is_length(1)
        assert_that(customers[0].name).is_equal_to("Acme")
