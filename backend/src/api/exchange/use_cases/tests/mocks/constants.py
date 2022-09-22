STELLAR_ACCOUNT_RESPONSE = {
    "_links": {
        "self": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT"
        },
        "transactions": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT/transactions{?cursor,limit,order}",
            "templated": True,
        },
        "operations": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT/operations{?cursor,limit,order}",
            "templated": True,
        },
        "payments": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT/payments{?cursor,limit,order}",
            "templated": True,
        },
        "effects": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT/effects{?cursor,limit,order}",
            "templated": True,
        },
        "offers": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT/offers{?cursor,limit,order}",
            "templated": True,
        },
        "trades": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT/trades{?cursor,limit,order}",
            "templated": True,
        },
        "data": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT/data/{key}",
            "templated": True,
        },
    },
    "id": "GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT",
    "account_id": "GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT",
    "sequence": "6385276339355649",
    "sequence_ledger": 1486694,
    "sequence_time": "1655237875",
    "subentry_count": 1,
    "last_modified_ledger": 1486694,
    "last_modified_time": "2022-06-14T20:17:55Z",
    "thresholds": {"low_threshold": 1, "med_threshold": 2, "high_threshold": 3},
    "flags": {
        "auth_required": True,
        "auth_revocable": True,
        "auth_immutable": False,
        "auth_clawback_enabled": True,
    },
    "balances": [
        {
            "balance": "999.9990000",
            "buying_liabilities": "0.0000000",
            "selling_liabilities": "0.0000000",
            "asset_type": "native",
        },
        {
            "balance": "0.0000000",
            "limit": "400.0000000",
            "buying_liabilities": "0.0000000",
            "selling_liabilities": "0.0000000",
            "last_modified_ledger": 1002735,
            "is_authorized": False,
            "is_authorized_to_maintain_liabilities": False,
            "asset_type": "credit_alphanum4",
            "asset_code": "TKN",
            "asset_issuer": "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
        },
    ],
    "signers": [
        {
            "weight": 1,
            "key": "GBCCHTXB3HLKHKJFMGF3EABMMHCL3IOMF573AVAXVN2WWJBKZJ7HXFAC",
            "type": "ed25519_public_key",
        },
        {
            "weight": 3,
            "key": "GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT",
            "type": "ed25519_public_key",
        },
    ],
    "data": {},
    "num_sponsoring": 0,
    "num_sponsored": 2,
    "sponsor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
    "paging_token": "GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT",
}

STELLAR_ACCOUNT_NOT_FOUND_RESPONSE = {
    "type": "https://stellar.org/horizon-errors/not_found",
    "title": "Resource Missing",
    "status": 404,
    "detail": "The resource at the url requested was not found.  This usually occurs for one of two reasons:  The url requested is not valid, or no data in our database could be found with the parameters provided.",
}

STELLAR_ASSETS_RESPONSE = {
    "_links": {
        "self": {
            "href": "https://horizon-testnet.stellar.org/assets?asset_issuer=GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23&cursor=&limit=10&order=asc"
        },
        "next": {
            "href": "https://horizon-testnet.stellar.org/assets?asset_issuer=GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23&cursor=USD_GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23_credit_alphanum4&limit=10&order=asc"
        },
        "prev": {
            "href": "https://horizon-testnet.stellar.org/assets?asset_issuer=GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23&cursor=RIO_GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23_credit_alphanum4&limit=10&order=desc"
        },
    },
    "_embedded": {
        "records": [
            {
                "_links": {"toml": {"href": ""}},
                "asset_type": "credit_alphanum4",
                "asset_code": "RIO",
                "asset_issuer": "GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23",
                "paging_token": "RIO_GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23_credit_alphanum4",
                "num_accounts": 276,
                "num_claimable_balances": 0,
                "num_liquidity_pools": 0,
                "amount": "922337203685.4700000",
                "accounts": {
                    "authorized": 276,
                    "authorized_to_maintain_liabilities": 0,
                    "unauthorized": 0,
                },
                "claimable_balances_amount": "0.0000000",
                "liquidity_pools_amount": "0.0000000",
                "balances": {
                    "authorized": "922337203685.4700000",
                    "authorized_to_maintain_liabilities": "0.0000000",
                    "unauthorized": "0.0000000",
                },
                "flags": {
                    "auth_required": False,
                    "auth_revocable": False,
                    "auth_immutable": False,
                    "auth_clawback_enabled": False,
                },
            },
            {
                "_links": {"toml": {"href": ""}},
                "asset_type": "credit_alphanum4",
                "asset_code": "USD",
                "asset_issuer": "GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23",
                "paging_token": "USD_GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23_credit_alphanum4",
                "num_accounts": 275,
                "num_claimable_balances": 0,
                "num_liquidity_pools": 0,
                "amount": "922337203685.4700000",
                "accounts": {
                    "authorized": 275,
                    "authorized_to_maintain_liabilities": 0,
                    "unauthorized": 0,
                },
                "claimable_balances_amount": "0.0000000",
                "liquidity_pools_amount": "0.0000000",
                "balances": {
                    "authorized": "922337203685.4700000",
                    "authorized_to_maintain_liabilities": "0.0000000",
                    "unauthorized": "0.0000000",
                },
                "flags": {
                    "auth_required": False,
                    "auth_revocable": False,
                    "auth_immutable": False,
                    "auth_clawback_enabled": False,
                },
            },
        ]
    },
}

STELLAR_ASSETS_EMPTY_RESPONSE = {
    "_links": {
        "self": {
            "href": "https://horizon-testnet.stellar.org/assets?asset_issuer=GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23\u0026cursor=USD_GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23_credit_alphanum4\u0026limit=10\u0026order=asc"
        },
        "next": {
            "href": "https://horizon-testnet.stellar.org/assets?asset_issuer=GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23\u0026cursor=USD_GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23_credit_alphanum4\u0026limit=10\u0026order=asc"
        },
        "prev": {
            "href": "https://horizon-testnet.stellar.org/assets?asset_issuer=GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23\u0026cursor=USD_GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23_credit_alphanum4\u0026limit=10\u0026order=desc"
        },
    },
    "_embedded": {"records": []},
}

ENVELOPE_XDR = "AAAAAgAAAADx8iG9cDQ/aQn0w/G3zP4IlJ70xrgFqLHxGZzAiczzMAAAJxAADk2pAAAAAgAAAAEAAAAAAAAAAAAAAABi/p3LAAAAAAAAAAEAAAABAAAAAPHyIb1wND9pCfTD8bfM/giUnvTGuAWosfEZnMCJzPMwAAAABgAAAAJUS05PVk8AAAAAAAAAAAAAH6Wjl6Bu2ZwWyEpAN4i1mR71TD2lIivfR4ssHZN+3GoAAAAA7msoAAAAAAAAAAAA"

STELLAR_SUBMIT_ENVELOPE_SUCCESSFULLY = {
    "_links": {
        "self": {
            "href": "https://horizon-testnet.stellar.org/transactions/32fc6f4b6c48d47e39da7242796171f644ac777cead60c9cad09890614aa6b99"
        },
        "account": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBNLUD3HK5ZSVG3EWWM5QP5KXZ6ZFF6XLFAM2DXLLVYAC6DYHHAHIC57"
        },
        "ledger": {"href": "https://horizon-testnet.stellar.org/ledgers/84528"},
        "operations": {
            "href": "https://horizon-testnet.stellar.org/transactions/32fc6f4b6c48d47e39da7242796171f644ac777cead60c9cad09890614aa6b99/operations{?cursor,limit,order}",
            "templated": True,
        },
        "effects": {
            "href": "https://horizon-testnet.stellar.org/transactions/32fc6f4b6c48d47e39da7242796171f644ac777cead60c9cad09890614aa6b99/effects{?cursor,limit,order}",
            "templated": True,
        },
        "precedes": {
            "href": "https://horizon-testnet.stellar.org/transactions?order=asc&cursor=363044995612672"
        },
        "succeeds": {
            "href": "https://horizon-testnet.stellar.org/transactions?order=desc&cursor=363044995612672"
        },
        "transaction": {
            "href": "https://horizon-testnet.stellar.org/transactions/32fc6f4b6c48d47e39da7242796171f644ac777cead60c9cad09890614aa6b99"
        },
    },
    "id": "32fc6f4b6c48d47e39da7242796171f644ac777cead60c9cad09890614aa6b99",
    "paging_token": "363044995612672",
    "successful": True,
    "hash": "32fc6f4b6c48d47e39da7242796171f644ac777cead60c9cad09890614aa6b99",
    "ledger": 84528,
    "created_at": "2022-06-27T13:59:34Z",
    "source_account": "GBNLUD3HK5ZSVG3EWWM5QP5KXZ6ZFF6XLFAM2DXLLVYAC6DYHHAHIC57",
    "source_account_sequence": "101219494264839",
    "fee_account": "GBNLUD3HK5ZSVG3EWWM5QP5KXZ6ZFF6XLFAM2DXLLVYAC6DYHHAHIC57",
    "fee_charged": "500",
    "max_fee": "50000",
    "operation_count": 5,
    "envelope_xdr": "AAAAAgAAAABaug9nV3Mqm2S1mdg/qr59kpfXWUDNDutdcAF4eDnAdAAAw1AAAFwPAAAABwAAAAEAAAAAAAAAAAAAAABiub7GAAAAAAAAAAUAAAABAAAAAFq6D2dXcyqbZLWZ2D+qvn2Sl9dZQM0O611wAXh4OcB0AAAAEAAAAADl0KUcAg1BU800QYNCCbcCyA+Zup6Cqr45Xqp+fZE5MgAAAAEAAAAAWroPZ1dzKptktZnYP6q+fZKX11lAzQ7rXXABeHg5wHQAAAAAAAAAAOXQpRwCDUFTzTRBg0IJtwLID5m6noKqvjleqn59kTkyAAAAAAEys6AAAAABAAAAAOXQpRwCDUFTzTRBg0IJtwLID5m6noKqvjleqn59kTkyAAAABgAAAAFDREJDAAAAAFWb9OOBDWQWwDlUMVEg6VDiAV8nVu1IbM4y2Q8maRphf/////////8AAAABAAAAAOXQpRwCDUFTzTRBg0IJtwLID5m6noKqvjleqn59kTkyAAAAEQAAAAEAAAAAVZv044ENZBbAOVQxUSDpUOIBXydW7UhszjLZDyZpGmEAAAAVAAAAAOXQpRwCDUFTzTRBg0IJtwLID5m6noKqvjleqn59kTkyAAAAAUNEQkMAAAAAVZv044ENZBbAOVQxUSDpUOIBXydW7UhszjLZDyZpGmEAAAAAAAAAAQAAAAAAAAAD7+AKjAAAAEBfZqtLQb+ki1Vg/Okblm3hmTQHEsjx+IYG6VbW2n97Je9VJlZ3DeaQ6cFrhTtwv5ippTj7+okFI3vDD0AOCasOeDnAdAAAAEBTl/ykM/q4p1faqUUe+CaUYNgE2AlMbzWEoszZqtmkAKCWQj5uIWlHLpV5mf4VBB35z+7yvnK4JXMdMh3f6coGfZE5MgAAAEAl93GSLyRahbu+hEZxn62CQv7/OrE0a1DzSzw5sy8BGPQpEW81Y9F04afqgNTMpp576XKV/NgZu9CUihOiCooN",
    "result_xdr": "AAAAAAAAAfQAAAAAAAAABQAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAARAAAAAAAAAAAAAAAVAAAAAAAAAAA=",
    "result_meta_xdr": "AAAAAgAAAAIAAAADAAFKMAAAAAAAAAAAWroPZ1dzKptktZnYP6q+fZKX11lAzQ7rXXABeHg5wHQAAAASm5LAuAAAXA8AAAAGAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAABEAAAAAAAAAAwAAAAAAAIfUAAAAAGK1ugEAAAAAAAAAAQABSjAAAAAAAAAAAFq6D2dXcyqbZLWZ2D+qvn2Sl9dZQM0O611wAXh4OcB0AAAAEpuSwLgAAFwPAAAABwAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAARAAAAAAAAAAMAAAAAAAFKMAAAAABiubfGAAAAAAAAAAUAAAAAAAAAAwAAAAMAAUowAAAAAAAAAABaug9nV3Mqm2S1mdg/qr59kpfXWUDNDutdcAF4eDnAdAAAABKbksC4AABcDwAAAAcAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAEQAAAAAAAAADAAAAAAABSjAAAAAAYrm3xgAAAAAAAAABAAFKMAAAAAAAAAAAWroPZ1dzKptktZnYP6q+fZKX11lAzQ7rXXABeHg5wHQAAAASmmANGAAAXA8AAAAHAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAABMAAAAAAAAAAwAAAAAAAUowAAAAAGK5t8YAAAAAAAAAAAABSjAAAAAAAAAAAOXQpRwCDUFTzTRBg0IJtwLID5m6noKqvjleqn59kTkyAAAAAAEys6AAAUowAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAIAAAAAAAAAAAAAAAAAAAABAAAAAQAAAABaug9nV3Mqm2S1mdg/qr59kpfXWUDNDutdcAF4eDnAdAAAAAAAAAAFAAAAAwABSjAAAAAAAAAAAFq6D2dXcyqbZLWZ2D+qvn2Sl9dZQM0O611wAXh4OcB0AAAAEppgDRgAAFwPAAAABwAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAATAAAAAAAAAAMAAAAAAAFKMAAAAABiubfGAAAAAAAAAAEAAUowAAAAAAAAAABaug9nV3Mqm2S1mdg/qr59kpfXWUDNDutdcAF4eDnAdAAAABKaYA0YAABcDwAAAAcAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAFAAAAAAAAAADAAAAAAABSjAAAAAAYrm3xgAAAAAAAAAAAAFKMAAAAAEAAAAA5dClHAINQVPNNEGDQgm3AsgPmbqegqq+OV6qfn2ROTIAAAABQ0RCQwAAAABVm/TjgQ1kFsA5VDFRIOlQ4gFfJ1btSGzOMtkPJmkaYQAAAAAAAAAAf/////////8AAAAEAAAAAAAAAAEAAAABAAAAAFq6D2dXcyqbZLWZ2D+qvn2Sl9dZQM0O611wAXh4OcB0AAAAAAAAAAMAAUowAAAAAAAAAADl0KUcAg1BU800QYNCCbcCyA+Zup6Cqr45Xqp+fZE5MgAAAAABMrOgAAFKMAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAACAAAAAAAAAAAAAAAAAAAAAQAAAAEAAAAAWroPZ1dzKptktZnYP6q+fZKX11lAzQ7rXXABeHg5wHQAAAAAAAAAAQABSjAAAAAAAAAAAOXQpRwCDUFTzTRBg0IJtwLID5m6noKqvjleqn59kTkyAAAAAAEys6AAAUowAAAAAAAAAAEAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAMAAAAAAAAAAAAAAAAAAAABAAAAAQAAAABaug9nV3Mqm2S1mdg/qr59kpfXWUDNDutdcAF4eDnAdAAAAAAAAAAAAAAAAgAAAAMAAUowAAAAAQAAAADl0KUcAg1BU800QYNCCbcCyA+Zup6Cqr45Xqp+fZE5MgAAAAFDREJDAAAAAFWb9OOBDWQWwDlUMVEg6VDiAV8nVu1IbM4y2Q8maRphAAAAAAAAAAB//////////wAAAAQAAAAAAAAAAQAAAAEAAAAAWroPZ1dzKptktZnYP6q+fZKX11lAzQ7rXXABeHg5wHQAAAAAAAAAAQABSjAAAAABAAAAAOXQpRwCDUFTzTRBg0IJtwLID5m6noKqvjleqn59kTkyAAAAAUNEQkMAAAAAVZv044ENZBbAOVQxUSDpUOIBXydW7UhszjLZDyZpGmEAAAAAAAAAAH//////////AAAABQAAAAAAAAABAAAAAQAAAABaug9nV3Mqm2S1mdg/qr59kpfXWUDNDutdcAF4eDnAdAAAAAAAAAAA",
    "fee_meta_xdr": "AAAAAgAAAAMAAIfUAAAAAAAAAABaug9nV3Mqm2S1mdg/qr59kpfXWUDNDutdcAF4eDnAdAAAABKbksKsAABcDwAAAAYAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAEQAAAAAAAAADAAAAAAAAh9QAAAAAYrW6AQAAAAAAAAABAAFKMAAAAAAAAAAAWroPZ1dzKptktZnYP6q+fZKX11lAzQ7rXXABeHg5wHQAAAASm5LAuAAAXA8AAAAGAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAABEAAAAAAAAAAwAAAAAAAIfUAAAAAGK1ugEAAAAA",
    "memo_type": "none",
    "signatures": [
        "X2arS0G/pItVYPzpG5Zt4Zk0BxLI8fiGBulW1tp/eyXvVSZWdw3mkOnBa4U7cL+YqaU4+/qJBSN7ww9ADgmrDg==",
        "U5f8pDP6uKdX2qlFHvgmlGDYBNgJTG81hKLM2arZpACglkI+biFpRy6VeZn+FQQd+c/u8r5yuCVzHTId3+nKBg==",
        "Jfdxki8kWoW7voRGcZ+tgkL+/zqxNGtQ80s8ObMvARj0KRFvNWPRdOGn6oDUzKaee+lylfzYGbvQlIoTogqKDQ==",
    ],
    "valid_after": "1970-01-01T00:00:00Z",
    "valid_before": "2022-06-27T14:29:26Z",
    "preconditions": {"timebounds": {"min_time": "0", "max_time": "1656340166"}},
}

STELLAR_SUBMIT_ENVELOPE_FAIL_TOO_LATE = {
    "type": "https://stellar.org/horizon-errors/transaction_failed",
    "title": "Transaction Failed",
    "status": 400,
    "detail": "The transaction failed when submitted to the stellar network. The `extras.result_codes` field on this response contains further details.  Descriptions of each code can be found at: https://developers.stellar.org/api/errors/http-status-codes/horizon-specific/transaction-failed/",
    "extras": {
        "envelope_xdr": "AAAAAgAAAABaug9nV3Mqm2S1mdg/qr59kpfXWUDNDutdcAF4eDnAdAAAw1AAAFwPAAAACAAAAAEAAAAAAAAAAAAAAABiud8/AAAAAAAAAAUAAAABAAAAAFq6D2dXcyqbZLWZ2D+qvn2Sl9dZQM0O611wAXh4OcB0AAAAEAAAAAAJyfJU3HBkREBbp8FTPbFXrAsBSWYG28jykpEP8/g3/gAAAAEAAAAAWroPZ1dzKptktZnYP6q+fZKX11lAzQ7rXXABeHg5wHQAAAAAAAAAAAnJ8lTccGREQFunwVM9sVesCwFJZgbbyPKSkQ/z+Df+AAAAAAEys6AAAAABAAAAAAnJ8lTccGREQFunwVM9sVesCwFJZgbbyPKSkQ/z+Df+AAAABgAAAAFDREJDAAAAAFWb9OOBDWQWwDlUMVEg6VDiAV8nVu1IbM4y2Q8maRphf/////////8AAAABAAAAAAnJ8lTccGREQFunwVM9sVesCwFJZgbbyPKSkQ/z+Df+AAAAEQAAAAEAAAAAVZv044ENZBbAOVQxUSDpUOIBXydW7UhszjLZDyZpGmEAAAAVAAAAAAnJ8lTccGREQFunwVM9sVesCwFJZgbbyPKSkQ/z+Df+AAAAAUNEQkMAAAAAVZv044ENZBbAOVQxUSDpUOIBXydW7UhszjLZDyZpGmEAAAAAAAAAAQAAAAAAAAAD7+AKjAAAAEDUWy8w0N4FsQ8DwubkqQHLPKVdCw9JUKl3FaOjtaNwwuEwFkn/jLBy0XT/3M4W+xyzIK6xtCO7HYc9yy/ak+oPeDnAdAAAAEDPjndDMu/p/o0dKVRVeIeP05YUgxq+9Ygzt3Yz7ESIl3nodhYvSkpWhJn2gogIaDrz9alPkzU+Gg1EhayWO7gM8/g3/gAAAECnjg9lG0HpeiuNcroLiAGdj6IsLd/qwW1Xj4n0FDcQ0L4Ag1Q6wPxAXf2p9UnzjeSc3cyzg2tQmu3USTJC+p4B",
        "result_codes": {"transaction": "tx_too_late"},
        "result_xdr": "AAAAAAAAAfT////9AAAAAA==",
    },
}

STELLAR_GET_PAYMENTS_WITHOUT_PAYMENT_TYPE_RESPONSE = {
    "_links": {
        "self": {
            "href": "https://horizon-testnet.stellar.org/accounts/GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6/payments?cursor=&limit=10&order=asc"
        },
        "next": {
            "href": "https://horizon-testnet.stellar.org/accounts/GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6/payments?cursor=4020798058672129&limit=10&order=asc"
        },
        "prev": {
            "href": "https://horizon-testnet.stellar.org/accounts/GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6/payments?cursor=4020798058672129&limit=10&order=desc"
        },
    },
    "_embedded": {
        "records": [
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/4020798058672129"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/de9f0f684e01522eea8adbf0d67e972a67390f9e3612a36ee84cb8f40cd8f459"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/4020798058672129/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=4020798058672129"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=4020798058672129"
                    },
                },
                "id": "4020798058672129",
                "paging_token": "4020798058672129",
                "transaction_successful": True,
                "source_account": "GAIH3ULLFQ4DGSECF2AR555KZ4KNDGEKN4AFI4SU2M7B43MGK3QJZNSR",
                "type": "create_account",
                "type_i": 0,
                "created_at": "2022-08-18T12:08:55Z",
                "transaction_hash": "de9f0f684e01522eea8adbf0d67e972a67390f9e3612a36ee84cb8f40cd8f459",
                "starting_balance": "10000.0000000",
                "funder": "GAIH3ULLFQ4DGSECF2AR555KZ4KNDGEKN4AFI4SU2M7B43MGK3QJZNSR",
                "account": "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
            }
        ]
    },
}

STELLAR_GET_PAYMENTS_EMPTY_RESPONSE = {
    "_links": {
        "self": {
            "href": "https://horizon-testnet.stellar.org/accounts/GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6/payments?cursor=4020798058672129&limit=10&order=asc"
        },
        "next": {
            "href": "https://horizon-testnet.stellar.org/accounts/GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6/payments?cursor=4020798058672129&limit=10&order=asc"
        },
        "prev": {
            "href": "https://horizon-testnet.stellar.org/accounts/GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6/payments?cursor=4020798058672129&limit=10&order=desc"
        },
    },
    "_embedded": {"records": []},
}

STELLAR_GET_PAYMENTS_RESPONSE = {
    "_links": {
        "self": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5/payments?cursor=&limit=10&order=asc"
        },
        "next": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5/payments?cursor=345396974985217&limit=10&order=asc"
        },
        "prev": {
            "href": "https://horizon-testnet.stellar.org/accounts/GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5/payments?cursor=6012954222593&limit=10&order=desc"
        },
    },
    "_embedded": {
        "records": [
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/6012954222593"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/db44c864bbcb087e0bce36a6989843099b975b987b29e07b3e23e0ce27beb4b3"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/6012954222593/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=6012954222593"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=6012954222593"
                    },
                },
                "id": "6012954222593",
                "paging_token": "6012954222593",
                "transaction_successful": True,
                "source_account": "GAIH3ULLFQ4DGSECF2AR555KZ4KNDGEKN4AFI4SU2M7B43MGK3QJZNSR",
                "type": "create_account",
                "type_i": 0,
                "created_at": "2022-06-22T12:26:26Z",
                "transaction_hash": "db44c864bbcb087e0bce36a6989843099b975b987b29e07b3e23e0ce27beb4b3",
                "starting_balance": "10000.0000000",
                "funder": "GAIH3ULLFQ4DGSECF2AR555KZ4KNDGEKN4AFI4SU2M7B43MGK3QJZNSR",
                "account": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
            },
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/10067403354113"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/d55d14a456b178be887d17824ef323d1e7b334ca1a8e29b1b6e99d0fe320a727"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/10067403354113/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=10067403354113"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=10067403354113"
                    },
                },
                "id": "10067403354113",
                "paging_token": "10067403354113",
                "transaction_successful": True,
                "source_account": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "type": "payment",
                "type_i": 1,
                "created_at": "2022-06-22T13:49:13Z",
                "transaction_hash": "d55d14a456b178be887d17824ef323d1e7b334ca1a8e29b1b6e99d0fe320a727",
                "asset_type": "credit_alphanum4",
                "asset_code": "USDC",
                "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "from": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "to": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "amount": "1000000.0000000",
            },
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/10071698321409"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/e8341e587ea540083597c5854c6c930da38eb053483c798275c77c82035942d9"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/10071698321409/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=10071698321409"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=10071698321409"
                    },
                },
                "id": "10071698321409",
                "paging_token": "10071698321409",
                "transaction_successful": True,
                "source_account": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "type": "payment",
                "type_i": 1,
                "created_at": "2022-06-22T13:49:18Z",
                "transaction_hash": "e8341e587ea540083597c5854c6c930da38eb053483c798275c77c82035942d9",
                "asset_type": "credit_alphanum4",
                "asset_code": "USDC",
                "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "from": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "to": "GBKJAUNVUZCSBFRXYZKURV5FKHMWWCSNJ7LB2ZUOBVJGJALBUI7ACLHD",
                "amount": "1000000.0000000",
            },
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/22462678962177"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/f06eff6582d2c32c5b51a1fede557e6c3f37deb6327ba1c7c3edf73ec5627eda"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/22462678962177/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=22462678962177"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=22462678962177"
                    },
                },
                "id": "22462678962177",
                "paging_token": "22462678962177",
                "transaction_successful": True,
                "source_account": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "type": "payment",
                "type_i": 1,
                "created_at": "2022-06-22T18:02:01Z",
                "transaction_hash": "f06eff6582d2c32c5b51a1fede557e6c3f37deb6327ba1c7c3edf73ec5627eda",
                "asset_type": "credit_alphanum4",
                "asset_code": "USDC",
                "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "from": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "to": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "amount": "1.0000000",
            },
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/344318938189825"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/2295484fcb2aa59844972c322142e2ca8e7fc4c63ada5930fe0a0488e8c8a331"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/344318938189825/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=344318938189825"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=344318938189825"
                    },
                },
                "id": "344318938189825",
                "paging_token": "344318938189825",
                "transaction_successful": True,
                "source_account": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "type": "payment",
                "type_i": 1,
                "created_at": "2022-06-27T07:37:50Z",
                "transaction_hash": "2295484fcb2aa59844972c322142e2ca8e7fc4c63ada5930fe0a0488e8c8a331",
                "asset_type": "credit_alphanum4",
                "asset_code": "USDC",
                "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "from": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "to": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "amount": "0.3400000",
            },
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/344374772768769"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/2af31bb8aee44745e09db2e0c2781230506d97bd1bf3f48fced7962248a042f2"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/344374772768769/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=344374772768769"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=344374772768769"
                    },
                },
                "id": "344374772768769",
                "paging_token": "344374772768769",
                "transaction_successful": True,
                "source_account": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "type": "payment",
                "type_i": 1,
                "created_at": "2022-06-27T07:38:56Z",
                "transaction_hash": "2af31bb8aee44745e09db2e0c2781230506d97bd1bf3f48fced7962248a042f2",
                "asset_type": "credit_alphanum4",
                "asset_code": "USDC",
                "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "from": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "to": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "amount": "0.0400000",
            },
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/344473557012481"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/7cdd0e12cb38456e57a433a517aece92d2aca9dfa43f45277cd2b93e5364a223"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/344473557012481/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=344473557012481"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=344473557012481"
                    },
                },
                "id": "344473557012481",
                "paging_token": "344473557012481",
                "transaction_successful": True,
                "source_account": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "type": "payment",
                "type_i": 1,
                "created_at": "2022-06-27T07:40:54Z",
                "transaction_hash": "7cdd0e12cb38456e57a433a517aece92d2aca9dfa43f45277cd2b93e5364a223",
                "asset_type": "credit_alphanum4",
                "asset_code": "USDC",
                "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "from": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "to": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "amount": "0.3400000",
            },
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/344516506685441"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/e1fe29591f6805b90ec29d249bd1e1c17776235c5dac918b2e6a968874e5cb4a"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/344516506685441/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=344516506685441"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=344516506685441"
                    },
                },
                "id": "344516506685441",
                "paging_token": "344516506685441",
                "transaction_successful": True,
                "source_account": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "type": "payment",
                "type_i": 1,
                "created_at": "2022-06-27T07:41:45Z",
                "transaction_hash": "e1fe29591f6805b90ec29d249bd1e1c17776235c5dac918b2e6a968874e5cb4a",
                "asset_type": "credit_alphanum4",
                "asset_code": "USDC",
                "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "from": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "to": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "amount": "0.0800000",
            },
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/344619585904641"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/853a16b7019ab0e2d2e6784f8390fea1dd170f07e4b2111643818aca78b98517"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/344619585904641/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=344619585904641"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=344619585904641"
                    },
                },
                "id": "344619585904641",
                "paging_token": "344619585904641",
                "transaction_successful": True,
                "source_account": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "type": "payment",
                "type_i": 1,
                "created_at": "2022-06-27T07:43:51Z",
                "transaction_hash": "853a16b7019ab0e2d2e6784f8390fea1dd170f07e4b2111643818aca78b98517",
                "asset_type": "credit_alphanum4",
                "asset_code": "USDC",
                "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "from": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "to": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "amount": "0.0300000",
            },
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/operations/345396974985217"
                    },
                    "transaction": {
                        "href": "https://horizon-testnet.stellar.org/transactions/2432e880008b21caf94daedda4ab0bfe407a20404954f8eae014f9d1668cae9c"
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/operations/345396974985217/effects"
                    },
                    "succeeds": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=desc&cursor=345396974985217"
                    },
                    "precedes": {
                        "href": "https://horizon-testnet.stellar.org/effects?order=asc&cursor=345396974985217"
                    },
                },
                "id": "345396974985217",
                "paging_token": "345396974985217",
                "transaction_successful": True,
                "source_account": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "type": "payment",
                "type_i": 1,
                "created_at": "2022-06-27T07:59:47Z",
                "transaction_hash": "2432e880008b21caf94daedda4ab0bfe407a20404954f8eae014f9d1668cae9c",
                "asset_type": "credit_alphanum4",
                "asset_code": "USDC",
                "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "from": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
                "to": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                "amount": "0.0100000",
            },
        ]
    },
}

STELLAR_GET_ACCOUNTS_RESPONSE = {
    "_links": {
        "self": {
            "href": "https://horizon-testnet.stellar.org/accounts?asset=TKN%3AGAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6&cursor=&limit=50&order=asc"
        },
        "next": {
            "href": "https://horizon-testnet.stellar.org/accounts?asset=TKN%3AGAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6&cursor=GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R&limit=50&order=asc"
        },
        "prev": {
            "href": "https://horizon-testnet.stellar.org/accounts?asset=TKN%3AGAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6&cursor=GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R&limit=50&order=desc"
        },
    },
    "_embedded": {
        "records": [
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R"
                    },
                    "transactions": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R/transactions{?cursor,limit,order}",
                        "templated": True,
                    },
                    "operations": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R/operations{?cursor,limit,order}",
                        "templated": True,
                    },
                    "payments": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R/payments{?cursor,limit,order}",
                        "templated": True,
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R/effects{?cursor,limit,order}",
                        "templated": True,
                    },
                    "offers": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R/offers{?cursor,limit,order}",
                        "templated": True,
                    },
                    "trades": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R/trades{?cursor,limit,order}",
                        "templated": True,
                    },
                    "data": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R/data/{key}",
                        "templated": True,
                    },
                },
                "id": "GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R",
                "account_id": "GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R",
                "sequence": "4306683966783489",
                "sequence_ledger": 1002735,
                "sequence_time": "1661174199",
                "subentry_count": 1,
                "last_modified_ledger": 1002735,
                "last_modified_time": "2022-08-22T13:16:39Z",
                "thresholds": {
                    "low_threshold": 0,
                    "med_threshold": 0,
                    "high_threshold": 0,
                },
                "flags": {
                    "auth_required": False,
                    "auth_revocable": False,
                    "auth_immutable": False,
                    "auth_clawback_enabled": False,
                },
                "balances": [
                    {
                        "balance": "0.0000000",
                        "limit": "400.0000000",
                        "buying_liabilities": "0.0000000",
                        "selling_liabilities": "0.0000000",
                        "last_modified_ledger": 1002735,
                        "is_authorized": False,
                        "is_authorized_to_maintain_liabilities": False,
                        "asset_type": "credit_alphanum4",
                        "asset_code": "TKN",
                        "asset_issuer": "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
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
                        "key": "GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R",
                        "type": "ed25519_public_key",
                    }
                ],
                "data": {},
                "num_sponsoring": 0,
                "num_sponsored": 0,
                "paging_token": "GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R",
            },
            {
                "_links": {
                    "self": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE"
                    },
                    "transactions": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE/transactions{?cursor,limit,order}",
                        "templated": True,
                    },
                    "operations": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE/operations{?cursor,limit,order}",
                        "templated": True,
                    },
                    "payments": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE/payments{?cursor,limit,order}",
                        "templated": True,
                    },
                    "effects": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE/effects{?cursor,limit,order}",
                        "templated": True,
                    },
                    "offers": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE/offers{?cursor,limit,order}",
                        "templated": True,
                    },
                    "trades": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE/trades{?cursor,limit,order}",
                        "templated": True,
                    },
                    "data": {
                        "href": "https://horizon-testnet.stellar.org/accounts/GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE/data/{key}",
                        "templated": True,
                    },
                },
                "id": "GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE",
                "account_id": "GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE",
                "sequence": "2076728356765696",
                "subentry_count": 5,
                "last_modified_ledger": 483526,
                "last_modified_time": "2022-07-21T23:20:32Z",
                "thresholds": {
                    "low_threshold": 20,
                    "med_threshold": 20,
                    "high_threshold": 20,
                },
                "flags": {
                    "auth_required": False,
                    "auth_revocable": False,
                    "auth_immutable": False,
                    "auth_clawback_enabled": False,
                },
                "balances": [
                    {
                        "balance": "0.0000000",
                        "limit": "922337203685.4775807",
                        "buying_liabilities": "0.0000000",
                        "selling_liabilities": "0.0000000",
                        "sponsor": "GCJZ7KZUY5QABS5OZYHORALKWZYDLGSY7PD2A5CNSQBL7XJN6LC4MB5Z",
                        "last_modified_ledger": 483526,
                        "is_authorized": True,
                        "is_authorized_to_maintain_liabilities": True,
                        "asset_type": "credit_alphanum4",
                        "asset_code": "ARST",
                        "asset_issuer": "GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO",
                    },
                    {
                        "balance": "0.0000000",
                        "limit": "10000",
                        "buying_liabilities": "0.0000000",
                        "selling_liabilities": "0.0000000",
                        "sponsor": "GCJZ7KZUY5QABS5OZYHORALKWZYDLGSY7PD2A5CNSQBL7XJN6LC4MB5Z",
                        "last_modified_ledger": 483526,
                        "is_authorized": True,
                        "is_authorized_to_maintain_liabilities": True,
                        "asset_type": "credit_alphanum4",
                        "asset_code": "USDC",
                        "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
                    },
                    {
                        "balance": "0.0000000",
                        "buying_liabilities": "0.0000000",
                        "selling_liabilities": "0.0000000",
                        "asset_type": "native",
                    },
                ],
                "signers": [
                    {
                        "weight": 10,
                        "key": "GDD5RALWGNC5LBOFQQK2TXHA6JE4NEUGRI6PSWMVUSSICROF2OLHLNHH",
                        "type": "ed25519_public_key",
                        "sponsor": "GCJZ7KZUY5QABS5OZYHORALKWZYDLGSY7PD2A5CNSQBL7XJN6LC4MB5Z",
                    },
                    {
                        "weight": 10,
                        "key": "GDCCZPOOCHGH5G257NOIDB6ZVZYGH4EAFRWQOWBNNDD23RQNP2REY2HD",
                        "type": "ed25519_public_key",
                        "sponsor": "GCJZ7KZUY5QABS5OZYHORALKWZYDLGSY7PD2A5CNSQBL7XJN6LC4MB5Z",
                    },
                    {
                        "weight": 20,
                        "key": "GCWMB7GHCIKCURO3VZZ74R64GPIM7FZV5T5OWNA5HOXNTIMSVMFCG2GB",
                        "type": "ed25519_public_key",
                        "sponsor": "GCJZ7KZUY5QABS5OZYHORALKWZYDLGSY7PD2A5CNSQBL7XJN6LC4MB5Z",
                    },
                    {
                        "weight": 0,
                        "key": "GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE",
                        "type": "ed25519_public_key",
                    },
                ],
                "data": {},
                "num_sponsoring": 0,
                "num_sponsored": 7,
                "sponsor": "GCJZ7KZUY5QABS5OZYHORALKWZYDLGSY7PD2A5CNSQBL7XJN6LC4MB5Z",
                "paging_token": "GDZZWUSWSALSWWH7TVBD54QWUUZQU4NCCVUF3DRU5WTEFCICKQBIPEIE",
            },
        ]
    },
}

STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE = {
    "_links": {
        "self": {
            "href": "https://horizon-testnet.stellar.org/accounts?asset=TKN%3AGAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6&cursor=GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R&limit=50&order=asc"
        },
        "next": {
            "href": "https://horizon-testnet.stellar.org/accounts?asset=TKN%3AGAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6&cursor=GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R&limit=50&order=asc"
        },
        "prev": {
            "href": "https://horizon-testnet.stellar.org/accounts?asset=TKN%3AGAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6&cursor=GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R&limit=50&order=desc"
        },
    },
    "_embedded": {"records": []},
}

TOML_LIST = [
    """VERSION = \"2.5.0\"
NETWORK_PASSPHRASE = \"Test SDF Network ; September 2015\"
""",
    """VERSION = \"2.5.0\"
NETWORK_PASSPHRASE = \"Public Global Stellar Network ; September 2015\"
""",
    """VERSION = \"2.5.0\"
NETWORK_PASSPHRASE = \"Test SDF Network ; September 2015\"
ACCOUNTS = [ \"GDBCIQ764FRXBKLR47Y3BYJ3ZJWZ663XO64LCSYNK3X27EW6NGMKOXJW\",]
[[PRINCIPALS]]
name = "John Doe"
email = "john@domain.org"

[[CURRENCIES]]
code = "TKN"
issuer = "GDYSPBVZHPQTYMGSYNOHRZQNLB3ZWFVQ2F7EP7YBOLRGD42XIC3QUX5G"
status = "live"
name = "Token Name"
desc = "Token description"
image = "https://domain.org/static/TKN.200x200.png"
is_asset_anchored = true
anchor_asset_type = "crypto"
anchor_asset = "TKN"
attestation_of_reserve = "https://www.domain.org/prospectus.pdf"
redemption_instructions = "Instructions ..."

[[CURRENCIES]]
code = "TEST"
issuer = "GDYSPBVZHPQTYMGSYNOHRZQNLB3ZWFVQ2F7EP7YBOLRGD42XIC3QUX5G"
status = "test"
name = "Test token"

[DOCUMENTATION]
ORG_NAME = "Org name"
ORG_DBA = "Org dba"
ORG_URL = "https://domain.org"
ORG_LOGO = "https://www.domain.org/images/logo-icon.png"
ORG_DESCRIPTION = "Some organization description."
ORG_PHYSICAL_ADDRESS = "P.O. Box 2681 Road Town, Tortola BVI"
ORG_TWITTER = "orgtwitter"
ORG_GITHUB = "orggithub"
ORG_OFFICIAL_EMAIL = "official@domain.org"
ORG_SUPPORT_EMAIL = "support@domain.org"
""",
]

GENERATE_TOML_RESPONSE = (
    (
        "TESTNET",
        {},
        {},
        [],
        [],
        TOML_LIST[0],
    ),
    (
        "PUBLIC",
        {},
        {},
        [],
        [],
        TOML_LIST[1],
    ),
    (
        "TESTNET",
        {"ACCOUNTS": ["GDBCIQ764FRXBKLR47Y3BYJ3ZJWZ663XO64LCSYNK3X27EW6NGMKOXJW"]},
        {
            "ORG_NAME": "Org name",
            "ORG_DBA": "Org dba",
            "ORG_URL": "https://domain.org",
            "ORG_LOGO": "https://www.domain.org/images/logo-icon.png",
            "ORG_DESCRIPTION": "Some organization description.",
            "ORG_PHYSICAL_ADDRESS": "P.O. Box 2681 Road Town, Tortola BVI",
            "ORG_TWITTER": "orgtwitter",
            "ORG_GITHUB": "orggithub",
            "ORG_OFFICIAL_EMAIL": "official@domain.org",
            "ORG_SUPPORT_EMAIL": "support@domain.org",
        },
        [{"name": "John Doe", "email": "john@domain.org"}],
        [
            {
                "code": "TKN",
                "issuer": "GDYSPBVZHPQTYMGSYNOHRZQNLB3ZWFVQ2F7EP7YBOLRGD42XIC3QUX5G",
                "status": "live",
                "name": "Token Name",
                "desc": "Token description",
                "image": "https://domain.org/static/TKN.200x200.png",
                "is_asset_anchored": True,
                "anchor_asset_type": "crypto",
                "anchor_asset": "TKN",
                "attestation_of_reserve": "https://www.domain.org/prospectus.pdf",
                "redemption_instructions": "Instructions ...",
            },
            {
                "code": "TEST",
                "issuer": "GDYSPBVZHPQTYMGSYNOHRZQNLB3ZWFVQ2F7EP7YBOLRGD42XIC3QUX5G",
                "status": "test",
                "name": "Test token",
            },
        ],
        TOML_LIST[2],
    ),
)

FETCH_STELLAR_TOML_RESPONSE = {
    "VERSION": "2.2.0",
    "NETWORK_PASSPHRASE": "Public Global Stellar Network ; September 2015",
    "ACCOUNTS": [
        "GAVBS6SXMRD7C3IRN5K2SY5C2CAUFHBVOGWTQXADSBUHAFDDUKVTQWWY",
        "GCBPMB2VK3POXU3QL2IPOUYKEDNZYRCYPFQGLLYVX6D2OLLRO7SWTTBO",
        "GADFXROGGR74V3MSWU2SUKCEUPQFZEIIF3IUHLRN3NKZ4JN2IPBMCODA",
        "GD7G6G56JHGQ3LY37ZYHALJRSAJYXWMYMKAF5G2GBXD5ETRPY4U5XS33",
        "GA3UK3JHOYYD3TAUH5C7NDOUDWBRF5FC4MECXFA2VRPEHIDQUOJIVOAJ",
        "GDGTVWSM4MGS4T7Z6W4RPWOCHE2I6RDFCIFZGS3DOA63LWQTRNZNTTFF",
        "GDYQNEF2UWTK4L6HITMT53MZ6F5QWO3Q4UVE6SCGC4OMEQIZQQDERQFD",
        "GARDNV3Q7YGT4AKSDF25LT32YSCCW4EV22Y2TV3I2PU2MMXJTEDL5T55",
        "GBUVRNH4RW4VLHP4C5MOF46RRIRZLAVHYGX45MVSTKA2F6TMR7E7L6NW",
        "GDVKAVKZDKMLPEXXFXPVKARRO4BNFJXRRPKENEDERK5PBYIWCJ2GQOOF",
        "GANESLOXBZWPLB5ZM2KFUTBGSBGISB7JTWFXO67G4TGQINWRMI6766GV",
    ],
    "SIGNING_KEY": "GA3UK3JHOYYD3TAUH5C7NDOUDWBRF5FC4MECXFA2VRPEHIDQUOJIVOAJ",
    "TRANSFER_SERVER": "https://ultrastellar.com/sep6",
    "TRANSFER_SERVER_SEP0024": "https://ultrastellar.com/sep24",
    "WEB_AUTH_ENDPOINT": "https://ultrastellar.com/auth",
    "DOCUMENTATION": {
        "ORG_NAME": "Ultra Stellar LLC",
        "ORG_DBA": "Ultra Stellar",
        "ORG_URL": "https://ultrastellar.com/",
        "ORG_LOGO": "https://ultrastellar.com/static/images/org_logo.png",
        "ORG_PHYSICAL_ADDRESS": "Tallinn, Estonia",
        "ORG_OFFICIAL_EMAIL": "hello@ultrastellar.com",
        "ORG_SUPPORT_EMAIL": "support@ultrastellar.com",
        "ORG_TWITTER": "ultrastellarhq",
        "ORG_DESCRIPTION": "Ultra Stellar is building the future of money on the Stellar network. Our products provide access to a new financial infrastructure that helps anyone in the world to achieve financial freedom.",
    },
    "PRINCIPALS": [
        {"name": "Gleb Pitsevich", "email": "gleb@ultrastellar.com"},
        {"name": "Dmitri Gmyza", "email": "dima@ultrastellar.com"},
    ],
    "CURRENCIES": [
        {
            "code": "yUSDC",
            "issuer": "GDGTVWSM4MGS4T7Z6W4RPWOCHE2I6RDFCIFZGS3DOA63LWQTRNZNTTFF",
            "image": "https://ultrastellar.com/static/images/icons/yUSDC.png",
            "desc": "yUSDC is an interest earning USDC tethered token. Earn interest on your USDC by holding yUSDC. yUSDC are liquid tokens that you can trade, redeem or send at any time. 1 yUSDC is always redeemable for 1 USDC through Ultra Stellar anchor. SDEX trading is live on yUSDC/USDC pair.",
            "conditions": "The interest share is distributed daily to yUSDC holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "USDC",
            "status": "live",
        },
        {
            "code": "yXLM",
            "issuer": "GARDNV3Q7YGT4AKSDF25LT32YSCCW4EV22Y2TV3I2PU2MMXJTEDL5T55",
            "image": "https://ultrastellar.com/static/images/icons/yXLM.png",
            "desc": "yXLM is an interest earning XLM tethered token. Earn interest on your XLM by holding yXLM. yXLM are liquid tokens that you can trade, redeem or send at any time. 1 yXLM is always redeemable for 1 XLM through Ultra Stellar anchor.",
            "conditions": "The interest share is distributed daily to yXLM holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "XLM",
            "status": "live",
        },
        {
            "code": "yETH",
            "issuer": "GDYQNEF2UWTK4L6HITMT53MZ6F5QWO3Q4UVE6SCGC4OMEQIZQQDERQFD",
            "image": "https://ultrastellar.com/static/images/icons/yETH.png",
            "desc": "yETH is an interest earning ETH tethered token. Earn interest on your ETH by holding yETH. yETH are liquid tokens that you can trade, redeem or send at any time. 1 yETH is always redeemable for 1 ETH through Ultra Stellar anchor. SDEX trading is live on yETH/ETH (ultrastellar.com) pair.",
            "conditions": "The interest share is distributed daily to yETH holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "ETH",
            "status": "live",
        },
        {
            "code": "yBTC",
            "issuer": "GBUVRNH4RW4VLHP4C5MOF46RRIRZLAVHYGX45MVSTKA2F6TMR7E7L6NW",
            "image": "https://ultrastellar.com/static/images/icons/yBTC.png",
            "desc": "yBTC is an interest earning BTC tethered token. Earn interest on your BTC by holding yBTC. yBTC are liquid tokens that you can trade, redeem or send at any time. 1 yBTC is always redeemable for 1 BTC through Ultra Stellar anchor. SDEX trading is live on yBTC/BTC (ultrastellar.com) pair.",
            "conditions": "The interest share is distributed daily to yBTC holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "BTC",
            "status": "live",
        },
        {
            "code": "ETH",
            "issuer": "GBFXOHVAS43OIWNIO7XLRJAHT3BICFEIKOJLZVXNT572MISM4CMGSOCC",
            "image": "https://ultrastellar.com/static/images/icons/ETH.png",
            "desc": "This is a tethered ETH token issued by Ultra Stellar. For each ETH in circulation on Stellar, Ultra Stellar holds the same amount of Ether in reserves. SDEX trading is live on ETH/USDC pair.",
            "conditions": "To get a 1:1 conversion between ETH on Stellar and native Ether use Deposit / Withdraw functionality supported in most Stellar wallets.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "ETH",
            "status": "live",
        },
        {
            "code": "BTC",
            "issuer": "GDPJALI4AZKUU2W426U5WKMAT6CN3AJRPIIRYR2YM54TL2GDWO5O2MZM",
            "image": "https://ultrastellar.com/static/images/icons/BTC.png",
            "desc": "This is a tethered BTC token issued by Ultra Stellar. For each BTC in circulation on Stellar, Ultra Stellar holds the same amount of Bitcoin in reserves. SDEX trading is live on BTC/USDC pair.",
            "conditions": "To get a 1:1 conversion between BTC on Stellar and native Bitcoin use Deposit / Withdraw functionality supported in most Stellar wallets.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "BTC",
            "status": "live",
        },
    ],
}

RETRIEVE_TOML_RESPONSE = {
    "currency_doc": [
        {
            "code": "yUSDC",
            "issuer": "GDGTVWSM4MGS4T7Z6W4RPWOCHE2I6RDFCIFZGS3DOA63LWQTRNZNTTFF",
            "image": "https://ultrastellar.com/static/images/icons/yUSDC.png",
            "desc": "yUSDC is an interest earning USDC tethered token. Earn interest on your USDC by holding yUSDC. yUSDC are liquid tokens that you can trade, redeem or send at any time. 1 yUSDC is always redeemable for 1 USDC through Ultra Stellar anchor. SDEX trading is live on yUSDC/USDC pair.",
            "conditions": "The interest share is distributed daily to yUSDC holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "USDC",
            "status": "live",
        },
        {
            "code": "yXLM",
            "issuer": "GARDNV3Q7YGT4AKSDF25LT32YSCCW4EV22Y2TV3I2PU2MMXJTEDL5T55",
            "image": "https://ultrastellar.com/static/images/icons/yXLM.png",
            "desc": "yXLM is an interest earning XLM tethered token. Earn interest on your XLM by holding yXLM. yXLM are liquid tokens that you can trade, redeem or send at any time. 1 yXLM is always redeemable for 1 XLM through Ultra Stellar anchor.",
            "conditions": "The interest share is distributed daily to yXLM holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "XLM",
            "status": "live",
        },
        {
            "code": "yETH",
            "issuer": "GDYQNEF2UWTK4L6HITMT53MZ6F5QWO3Q4UVE6SCGC4OMEQIZQQDERQFD",
            "image": "https://ultrastellar.com/static/images/icons/yETH.png",
            "desc": "yETH is an interest earning ETH tethered token. Earn interest on your ETH by holding yETH. yETH are liquid tokens that you can trade, redeem or send at any time. 1 yETH is always redeemable for 1 ETH through Ultra Stellar anchor. SDEX trading is live on yETH/ETH (ultrastellar.com) pair.",
            "conditions": "The interest share is distributed daily to yETH holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "ETH",
            "status": "live",
        },
        {
            "code": "yBTC",
            "issuer": "GBUVRNH4RW4VLHP4C5MOF46RRIRZLAVHYGX45MVSTKA2F6TMR7E7L6NW",
            "image": "https://ultrastellar.com/static/images/icons/yBTC.png",
            "desc": "yBTC is an interest earning BTC tethered token. Earn interest on your BTC by holding yBTC. yBTC are liquid tokens that you can trade, redeem or send at any time. 1 yBTC is always redeemable for 1 BTC through Ultra Stellar anchor. SDEX trading is live on yBTC/BTC (ultrastellar.com) pair.",
            "conditions": "The interest share is distributed daily to yBTC holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "BTC",
            "status": "live",
        },
        {
            "code": "ETH",
            "issuer": "GBFXOHVAS43OIWNIO7XLRJAHT3BICFEIKOJLZVXNT572MISM4CMGSOCC",
            "image": "https://ultrastellar.com/static/images/icons/ETH.png",
            "desc": "This is a tethered ETH token issued by Ultra Stellar. For each ETH in circulation on Stellar, Ultra Stellar holds the same amount of Ether in reserves. SDEX trading is live on ETH/USDC pair.",
            "conditions": "To get a 1:1 conversion between ETH on Stellar and native Ether use Deposit / Withdraw functionality supported in most Stellar wallets.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "ETH",
            "status": "live",
        },
        {
            "code": "BTC",
            "issuer": "GDPJALI4AZKUU2W426U5WKMAT6CN3AJRPIIRYR2YM54TL2GDWO5O2MZM",
            "image": "https://ultrastellar.com/static/images/icons/BTC.png",
            "desc": "This is a tethered BTC token issued by Ultra Stellar. For each BTC in circulation on Stellar, Ultra Stellar holds the same amount of Bitcoin in reserves. SDEX trading is live on BTC/USDC pair.",
            "conditions": "To get a 1:1 conversion between BTC on Stellar and native Bitcoin use Deposit / Withdraw functionality supported in most Stellar wallets.",
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "BTC",
            "status": "live",
        },
    ],
    "point_of_contact_doc": [
        {"name": "Gleb Pitsevich", "email": "gleb@ultrastellar.com"},
        {"name": "Dmitri Gmyza", "email": "dima@ultrastellar.com"},
    ],
    "org_doc": {
        "ORG_NAME": "Ultra Stellar LLC",
        "ORG_DBA": "Ultra Stellar",
        "ORG_URL": "https://ultrastellar.com/",
        "ORG_LOGO": "https://ultrastellar.com/static/images/org_logo.png",
        "ORG_PHYSICAL_ADDRESS": "Tallinn, Estonia",
        "ORG_OFFICIAL_EMAIL": "hello@ultrastellar.com",
        "ORG_SUPPORT_EMAIL": "support@ultrastellar.com",
        "ORG_TWITTER": "ultrastellarhq",
        "ORG_DESCRIPTION": "Ultra Stellar is building the future of money on the Stellar network. Our products provide access to a new financial infrastructure that helps anyone in the world to achieve financial freedom.",
    },
    "general_info": {
        "VERSION": "2.2.0",
        "NETWORK_PASSPHRASE": "Public Global Stellar Network ; September 2015",
        "ACCOUNTS": [
            "GAVBS6SXMRD7C3IRN5K2SY5C2CAUFHBVOGWTQXADSBUHAFDDUKVTQWWY",
            "GCBPMB2VK3POXU3QL2IPOUYKEDNZYRCYPFQGLLYVX6D2OLLRO7SWTTBO",
            "GADFXROGGR74V3MSWU2SUKCEUPQFZEIIF3IUHLRN3NKZ4JN2IPBMCODA",
            "GD7G6G56JHGQ3LY37ZYHALJRSAJYXWMYMKAF5G2GBXD5ETRPY4U5XS33",
            "GA3UK3JHOYYD3TAUH5C7NDOUDWBRF5FC4MECXFA2VRPEHIDQUOJIVOAJ",
            "GDGTVWSM4MGS4T7Z6W4RPWOCHE2I6RDFCIFZGS3DOA63LWQTRNZNTTFF",
            "GDYQNEF2UWTK4L6HITMT53MZ6F5QWO3Q4UVE6SCGC4OMEQIZQQDERQFD",
            "GARDNV3Q7YGT4AKSDF25LT32YSCCW4EV22Y2TV3I2PU2MMXJTEDL5T55",
            "GBUVRNH4RW4VLHP4C5MOF46RRIRZLAVHYGX45MVSTKA2F6TMR7E7L6NW",
            "GDVKAVKZDKMLPEXXFXPVKARRO4BNFJXRRPKENEDERK5PBYIWCJ2GQOOF",
            "GANESLOXBZWPLB5ZM2KFUTBGSBGISB7JTWFXO67G4TGQINWRMI6766GV",
        ],
        "SIGNING_KEY": "GA3UK3JHOYYD3TAUH5C7NDOUDWBRF5FC4MECXFA2VRPEHIDQUOJIVOAJ",
        "TRANSFER_SERVER": "https://ultrastellar.com/sep6",
        "TRANSFER_SERVER_SEP0024": "https://ultrastellar.com/sep24",
        "WEB_AUTH_ENDPOINT": "https://ultrastellar.com/auth",
    },
}
