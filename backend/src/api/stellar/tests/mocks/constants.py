MISSING_ONE_SIGNATURE = {
    "type": "https://stellar.org/horizon-errors/transaction_failed",
    "title": "Transaction Failed",
    "status": 400,
    "detail": "The transaction failed when submitted to the stellar network. The `extras.result_codes` field on this response contains further details.  Descriptions of each code can be found at: https://developers.stellar.org/api/errors/http-status-codes/horizon-specific/transaction-failed/",
    "extras": {
        "envelope_xdr": "",
        "result_codes": {
            "transaction": "tx_failed",
            "operations": ["op_success", "op_success", "op_bad_auth"],
        },
        "result_xdr": "AAAAAAAAASz/////AAAAAwAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAP////8AAAAA",
    },
}
WRONG_ACCOUNT_FORMAT = {
    "type": "https://stellar.org/horizon-errors/bad_request",
    "title": "Bad Request",
    "status": 400,
    "detail": "The request you sent was invalid in some way.",
    "extras": {
        "invalid_field": "account_id",
        "reason": "Account ID must start with `G` and contain 56 alphanum characters",
    },
}

NO_SHAPE_TRANSACTION = {
    "FieldX": "Some value",
    "FieldY": "Some other value",
}

LOW_RESERVE_TRANSACTION = {
    "type": "https://stellar.org/horizon-errors/transaction_failed",
    "title": "Transaction Failed",
    "status": 400,
    "detail": "The transaction failed when submitted to the stellar network. The `extras.result_codes` field on this response contains further details.  Descriptions of each code can be found at: https://developers.stellar.org/api/errors/http-status-codes/horizon-specific/transaction-failed/",
    "extras": {
        "envelope_xdr": "",
        "result_codes": {
            "transaction": "tx_failed",
            "operations": ["op_low_reserve"],
        },
        "result_xdr": "AAAAAAAAAGT/////AAAAAQAAAAAAAAAA/////QAAAAA=",
    },
}

NOT_FOUND_TRANSACTION = {
    "type": "https://stellar.org/horizon-errors/not_found",
    "title": "Resource Missing",
    "status": 404,
    "detail": "The resource at the url requested was not found.  This usually occurs for one of two reasons:  The url requested is not valid, or no data in our database could be found with the parameters provided.",
}

UNDERFUNDED_TRANSACTION = {
    "type": "https://stellar.org/horizon-errors/transaction_failed",
    "title": "Transaction Failed",
    "status": 400,
    "detail": "The transaction failed when submitted to the stellar network. The `extras.result_codes` field on this response contains further details.  Descriptions of each code can be found at: https://developers.stellar.org/api/errors/http-status-codes/horizon-specific/transaction-failed/",
    "extras": {
        "envelope_xdr": "AAAAAgAAAADsfA+8x4rDPcncMDg67m9Is6gQoZRD5N8PGn45AWa47AAAAGQAA88hAAAAOAAAAAEAAAAAAAAAAAAAAABiaozFAAAAAAAAAAEAAAABAAAAAOx8D7zHisM9ydwwODrub0izqBChlEPk3w8afjkBZrjsAAAADgAAAAJCYWJ5QmFjb24AAAAAAAAA5KGfQSgtJHni8BPO9UJov7lW+WGy1g/6tsfj9WW/Z2Q6SWW/WKQAAAAAAAEAAAAAAAAAAOEIXV84YMremKTOCjmb3JGDl0TCbbB1RQh0E3G+bVLtAAAAAAAAAAAAAAABAWa47AAAAECrck/zHrJS8gqp5AX5KXAXoRPxd9/Mm8ohN0VtbKL71qbtpoW4O6bR3oMAjUhTX3fcC/Vk8dvBYrRJC889X5gF",
        "result_codes": {"transaction": "tx_failed", "operations": ["op_underfunded"]},
        "result_xdr": "AAAAAAAAAGT/////AAAAAQAAAAAAAAAO////+wAAAAA=",
    },
}

TRANSACTION_ALREADY_EXISTS = {
    "type": "https://stellar.org/horizon-errors/transaction_failed",
    "title": "Transaction Failed",
    "status": 400,
    "detail": "The transaction failed when submitted to the stellar network. The `extras.result_codes` field on this response contains further details.  Descriptions of each code can be found at: https://developers.stellar.org/api/errors/http-status-codes/horizon-specific/transaction-failed/",
    "extras": {
        "envelope_xdr": "AAAAAgAAAADsfA+8x4rDPcncMDg67m9Is6gQoZRD5N8PGn45AWa47AAAAGQAA88hAAAAOwAAAAEAAAAAAAAAAAAAAABiawr1AAAAAQAAAAtUZXN0IFNjcmlwdAAAAAABAAAAAQAAAADsfA+8x4rDPcncMDg67m9Is6gQoZRD5N8PGn45AWa47AAAAAAAAAAA4QhdXzhgyt6YpM4KOZvckYOXRMJtsHVFCHQTcb5tUu0AAAAAdzWUAAAAAAAAAAABAWa47AAAAEA2OWRlN41oO2levr9Fa9Fp+0RD+E3GUQN1xuWUt5bmG6k3yXwqA0+QTTWEq2Z/cKqv+R7rKcnHfU8MGqgAN/oK",
        "result_codes": {
            "transaction": "tx_failed",
            "operations": ["op_already_exists"],
        },
        "result_xdr": "AAAAAAAAAGT/////AAAAAQAAAAAAAAAA/////AAAAAA=",
    },
}
MALFORMED_TRANSACTION = {
    "type": "https://stellar.org/horizon-errors/transaction_failed",
    "title": "Transaction Failed",
    "status": 400,
    "detail": "The transaction failed when submitted to the stellar network. The `extras.result_codes` field on this response contains further details.  Descriptions of each code can be found at: https://developers.stellar.org/api/errors/http-status-codes/horizon-specific/transaction-failed/",
    "extras": {
        "envelope_xdr": "AAAAAgAAAADsfA+8x4rDPcncMDg67m9Is6gQoZRD5N8PGn45AWa47AAAAGQAA88hAAAAPgAAAAEAAAAAAAAAAAAAAABiaxTkAAAAAQAAAAtUZXN0IFNjcmlwdAAAAAABAAAAAQAAAADsfA+8x4rDPcncMDg67m9Is6gQoZRD5N8PGn45AWa47AAAAAEAAAAA4QhdXzhgyt6YpM4KOZvckYOXRMJtsHVFCHQTcb5tUu0AAAACQmFieUJhY29uAAAAAAAAAOShn0EoLSR54vATzvVCaL+5VvlhstYP+rbH4/Vlv2dkAAAAAAAAAAAAAAAAAAAAAQFmuOwAAABA7LGv1hnCqVA77NYp2Gol/hzfdHSa7FU8m3p5bkWnIA4xxbknkqjg0Jgs3PBWxfQPlSAe4PO7EnJy0qWss+GgDg==",
        "result_codes": {"transaction": "tx_failed", "operations": ["op_malformed"]},
        "result_xdr": "AAAAAAAAAGT/////AAAAAQAAAAAAAAAB/////wAAAAA=",
    },
}
