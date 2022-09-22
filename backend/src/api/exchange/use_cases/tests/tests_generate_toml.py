import pytest
from pytest_mock import MockerFixture

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import GenerateTOMLUseCase
from api.exchange.use_cases.generate_toml import GenerateTOMLUseCase
from api.stellar.helpers.utils import get_network_data

from .mocks import constants


def test_generate_toml_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "invalid",
    }

    get_network_data_mock = mocker.patch(
        "api.exchange.use_cases.generate_toml.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        GenerateTOMLUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))


@pytest.mark.parametrize(
    "network,general_info,org_doc,point_of_contact_doc,currency_doc,expected_toml",
    constants.GENERATE_TOML_RESPONSE,
)
def test_generate_toml_succesfully(
    mocker: MockerFixture,
    network: str,
    general_info: dict,
    org_doc: dict,
    point_of_contact_doc: list,
    currency_doc: list,
    expected_toml: str,
):

    get_network_data_mock = mocker.patch(
        "api.exchange.use_cases.generate_toml.get_network_data",
        side_effect=get_network_data,
    )

    response: dict = GenerateTOMLUseCase().execute(
        network=network,
        general_info=general_info,
        org_doc=org_doc,
        point_of_contact_doc=point_of_contact_doc,
        currency_doc=currency_doc,
    )

    get_network_data_mock.assert_called_with(network)

    assert response == expected_toml
