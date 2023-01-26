PAYEES_LIST = [
    "GC27BXCORFXR4JLVPWVZXXALHWICY7YF5B3UN76RPRGFGQAK5LOVNL6E",
    "GCONTCA4CM6EBCIJATWTLEPI52ZOFXT7STWZ6WOYZU7ZON6SXYHABJ3K",
    "GCU6AOSXXERDXMR4FEKUWOKNITGCHJ6VRSIVHNGNB4OYMOHL2DBWPCNC",
    "GDQTU4W3UFE73VCEJ4SLISP3KLM36AYQWXLAKKDI4FOJ7T5ZBQHZVXHU",
    "GB6QNWJI4ERDKF3HPJOGHXN7IY5WE3BOIUGPSHJWPJSCLKQUQ57O5YFS",
    "GA3ABN3IJ2RKWWJVZDLPUUGRMDBBS23EIHPRBYAALLII2CAE5JAF7X36",
]

STELLAR_ACCOUNT_RESPONSE = {
    "_links": {
        "self": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2"
        },
        "transactions": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2/transactions{?cursor,limit,order}",
            "templated": True,
        },
        "operations": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2/operations{?cursor,limit,order}",
            "templated": True,
        },
        "payments": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2/payments{?cursor,limit,order}",
            "templated": True,
        },
        "effects": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2/effects{?cursor,limit,order}",
            "templated": True,
        },
        "offers": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2/offers{?cursor,limit,order}",
            "templated": True,
        },
        "trades": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2/trades{?cursor,limit,order}",
            "templated": True,
        },
        "data": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2/data/{key}",
            "templated": True,
        },
    },
    "id": "GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2",
    "account_id": "GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2",
    "sequence": "2831444304986113",
    "sequence_ledger": 659248,
    "sequence_time": "1674473684",
    "subentry_count": 1,
    "last_modified_ledger": 659248,
    "last_modified_time": "2023-01-23T11:34:44Z",
    "thresholds": {"low_threshold": 0, "med_threshold": 0, "high_threshold": 0},
    "flags": {
        "auth_required": False,
        "auth_revocable": False,
        "auth_immutable": False,
        "auth_clawback_enabled": False,
    },
    "balances": [
        {
            "balance": "10000000000.0000000",
            "limit": "922337203685.4775807",
            "buying_liabilities": "0.0000000",
            "selling_liabilities": "0.0000000",
            "last_modified_ledger": 659249,
            "is_authorized": True,
            "is_authorized_to_maintain_liabilities": True,
            "asset_type": "credit_alphanum4",
            "asset_code": "EUR",
            "asset_issuer": "GC3XSOYSQDYBBGBBMV7OBZJOZQL47POSV6R4WPPXQVYMIEQBDFTAK46U",
        },
        {
            "balance": "10.0000000",
            "limit": "922337203685.4775807",
            "buying_liabilities": "0.0000000",
            "selling_liabilities": "0.0000000",
            "last_modified_ledger": 659249,
            "is_authorized": True,
            "is_authorized_to_maintain_liabilities": True,
            "asset_type": "credit_alphanum4",
            "asset_code": "USD",
            "asset_issuer": "GDGDATWYNYC5SBZORXK3JVU5NSIHSZWB72FWCBWYCQIMYS5V3BUK4PH7",
        },
        {
            "balance": "9999.9990000",
            "buying_liabilities": "0.0000000",
            "selling_liabilities": "0.0000000",
            "asset_type": "native",
        },
    ],
    "signers": [
        {
            "weight": 1,
            "key": "GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2",
            "type": "ed25519_public_key",
        }
    ],
    "data": {},
    "num_sponsoring": 0,
    "num_sponsored": 0,
    "paging_token": "GBZSWG2IZQHAEFEJNOQ6OUAICPVK7DO7R5GTAIOBGXFDCYU5PFYT3TA2",
}
