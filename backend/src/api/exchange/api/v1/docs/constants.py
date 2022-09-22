ISSUER_INFO_RESPONSE = {
    "clawback": False,
    "freeze": True,
    "assets": [
        {
            "code": "TKN1",
            "issuer": "GAFQPTJUWBLFAQ2PETKBNGUF5TDMJ3DK7SI4EZZCKIJLNTYYYE7VS62L",
            "supply": 100.0,
            "name": "TKN1-GAFQPTJUWBLFAQ2PETKBNGUF5TDMJ3DK7SI4EZZCKIJLNTYYYE7VS62L",
        },
        {
            "code": "TKN2",
            "issuer": "GAFQPTJUWBLFAQ2PETKBNGUF5TDMJ3DK7SI4EZZCKIJLNTYYYE7VS62L",
            "supply": 9223685.47,
            "name": "TKN2-GAFQPTJUWBLFAQ2PETKBNGUF5TDMJ3DK7SI4EZZCKIJLNTYYYE7VS62L",
        },
    ],
}

ACCOUNT_NOT_FOUND_RESPONSE = {"code": 2, "detail": "account_not_found"}

INVALID_PUBLIC_KEY_RESPONSE = {"code": 1, "detail": "invalid_public_key"}

ENVELOPE_CREATED_RESPONSE = {
    "envelope_xdr": "AAAAAgAAAADA...AAAAAA==",
    "required_signatures": ["GDA...U7PL"],
}

CREATE_ASSET_MISSING_FIELDS_RESPONSE = {
    "issuer": ["This field is required."],
    "distributor": ["This field is required."],
    "asset_code": ["This field is required."],
}

SUBMIT_ENVELOPE_RESPONSE = {
    "transaction_hash": "9ea8db4bc3...bc4842fc4a",
    "transaction_link": "https://stellar.expert/explorer/testnet/tx/9ea8db4bc3...bc4842fc4a",
}

SUBMIT_ENVELOPE_INVALID_RESPONSE = {"code": 7, "detail": "invalid_envelope_xdr"}

SUBMIT_ENVELOPE_MISSING_SIGNATURES_RESPONSE = {
    "stellar_status_code": 400,
    "message": "Err: needs more signatures to complete this operation.",
}

SUBMIT_ENVELOPE_OP_ERROR_RESPONSE = {
    "stellar_status_code": 400,
    "message": "Err: One of the operations failed.",
}

PUBLIC_KEY_RESPONSE = {"public_key": "GDA...U7PL"}

MINT_ASSET_MISSING_FIELDS_RESPONSE = {
    "issuer": ["This field is required."],
    "distributor": ["This field is required."],
    "asset_code": ["This field is required."],
    "amount": ["This field is required."],
}

BURN_ASSET_MISSING_FIELDS_RESPONSE = MINT_ASSET_MISSING_FIELDS_RESPONSE

PAYMENT_MISSING_FIELDS_RESPONSE = {
    "issuer": ["This field is required."],
    "distributor": ["This field is required."],
    "target": ["This field is required."],
    "asset_code": ["This field is required."],
    "amount": ["This field is required."],
}

MANAGE_DATA_MISSING_FIELDS_RESPONSE = {
    "public_key": ["This field is required."],
    "name": ["This field is required."],
}

CLAWBACK_MISSING_FIELDS_RESPONSE = {"issuer": ["This field is required."]}

CLAWBACK_TARGET_REQUEST = {
    "issuer": "GDA...U7PL",
    "target": "GPD...L2OA",
    "asset_code": "TKN",
    "amount": 10.34,
}

CLAWBACK_CLAIMABLE_REQUEST = {
    "issuer": "GDA...U7PL",
    "claimable_id": "00000000213...68c23c06a55",
}

UPDATE_AUTH_FLAG_MISSING_FIELDS_RESPONSE = {
    "issuer": ["This field is required."],
    "target": ["This field is required."],
    "asset_code": ["This field is required."],
}

SET_HOME_DOMAIN_MISSING_FIELDS_RESPONSE = {
    "public_key": ["This field is required."],
    "home_domain": ["This field is required."],
}

TOML_NOT_FOUND_RESPONSE = {"code": 20, "detail": "toml_not_found"}


SET_OPTIONS_MISSING_FIELDS_RESPONSE = {
    "public_key": ["This field is required."],
    "clawback": ["This field is required."],
    "freeze": ["This field is required."],
    "signers": ["This field is required."],
}
