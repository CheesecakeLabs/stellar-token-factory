from typing import List

from stellar_sdk import TrustLineFlags

from .constants import (
    AUTHORIZED_FLAG,
    AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
    TRUSTLINE_CLAWBACK_ENABLED_FLAG,
)


def trustline_flags_parser(flags: int) -> List[TrustLineFlags]:
    mapping = {
        AUTHORIZED_FLAG: TrustLineFlags.AUTHORIZED_FLAG,
        AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG: TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
        TRUSTLINE_CLAWBACK_ENABLED_FLAG: TrustLineFlags.TRUSTLINE_CLAWBACK_ENABLED_FLAG,
    }
    return [mapping.get(flag, 0) for flag in flags]
