from django.conf import settings

from api.stellar.helpers.exceptions import InvalidNetwork


def get_network_data(network_name: str) -> dict[str, str]:
    data = {"api": None, "passphrase": None}
    if network_name == "PUBLIC":
        data["api"] = settings.HORIZON_PUBLIC_API_SERVER
        data["passphrase"] = settings.PUBLIC_NETWORK_PASSPHRASE
    elif network_name == "TESTNET":
        data["api"] = settings.HORIZON_TEST_API_SERVER
        data["passphrase"] = settings.TEST_NETWORK_PASSPHRASE
    else:
        raise InvalidNetwork(f"Invalid Network provided. Network: {network_name}")

    return data
