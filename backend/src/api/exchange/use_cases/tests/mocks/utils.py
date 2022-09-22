from stellar_sdk import Account

from . import constants


def get_mocked_account_object(
    account_id: str = None, data: str = constants.STELLAR_ACCOUNT_RESPONSE
) -> Account:
    return Account(
        account=account_id if account_id else data["id"],
        sequence=int(data["sequence"]),
        raw_data=data,
    )
