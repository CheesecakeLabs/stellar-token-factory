from api.exchange.use_cases.tests.mocks.constants import TOML_LIST

CREATE_ASSET_FAIL_RESPONSES = (
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
        },
        {"distributor": ["This field is required."]},
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
        },
        {"issuer": ["This field is required."]},
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
        },
        {"asset_code": ["This field is required."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "limit": 20.9,
        },
        {
            "distributor": ["This field is required."],
            "asset_code": ["This field is required."],
        },
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
        },
        {
            "issuer": ["This field is required."],
            "asset_code": ["This field is required."],
        },
    ),
    (
        {
            "asset_code": "TKN",
        },
        {
            "issuer": ["This field is required."],
            "distributor": ["This field is required."],
        },
    ),
    (
        {},
        {
            "issuer": ["This field is required."],
            "distributor": ["This field is required."],
            "asset_code": ["This field is required."],
        },
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "LONGTOKENNAME",
            "limit": 10,
        },
        {"asset_code": ["Ensure this field has no more than 12 characters."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQL",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
        },
        {"issuer": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQL",
            "asset_code": "TKN",
            "limit": None,
        },
        {"distributor": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "limit": -10,
        },
        {"limit": ["Ensure this value is greater than 0."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "limit": 0,
        },
        {"limit": ["Ensure this value is greater than 0."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "limit": 922337203689,
        },
        {"limit": ["Ensure this value is less than or equal to 922337203685."]},
    ),
)

MINT_ASSET_FAIL_RESPONSES = (
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "amount": 20.9,
        },
        {"distributor": ["This field is required."]},
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "amount": 20.9,
        },
        {"issuer": ["This field is required."]},
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "amount": 20.9,
        },
        {"asset_code": ["This field is required."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "amount": 20.9,
        },
        {
            "distributor": ["This field is required."],
            "asset_code": ["This field is required."],
        },
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
        },
        {"amount": ["This field is required."]},
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "amount": 20.9,
        },
        {
            "issuer": ["This field is required."],
            "asset_code": ["This field is required."],
        },
    ),
    (
        {
            "asset_code": "TKN",
        },
        {
            "issuer": ["This field is required."],
            "distributor": ["This field is required."],
            "amount": ["This field is required."],
        },
    ),
    (
        {},
        {
            "issuer": ["This field is required."],
            "distributor": ["This field is required."],
            "asset_code": ["This field is required."],
            "amount": ["This field is required."],
        },
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "LONGTOKENNAME",
            "amount": 10,
        },
        {"asset_code": ["Ensure this field has no more than 12 characters."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQL",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "amount": 10,
        },
        {"issuer": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQL",
            "asset_code": "TKN",
            "amount": 10,
        },
        {"distributor": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "amount": -10,
        },
        {"amount": ["Ensure this value is greater than 0."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "amount": 0,
        },
        {"amount": ["Ensure this value is greater than 0."]},
    ),
)

BURN_ASSET_FAIL_RESPONSES = MINT_ASSET_FAIL_RESPONSES

CREATE_PAYMENT_FAIL_RESPONSES = (
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "asset_code": "TKN",
            "amount": 20.9,
        },
        {"distributor": ["This field is required."]},
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "asset_code": "TKN",
            "amount": 20.9,
        },
        {"issuer": ["This field is required."]},
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "asset_code": "TKN",
            "amount": 20.9,
        },
        {"target": ["This field is required."]},
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "amount": 20.9,
        },
        {"asset_code": ["This field is required."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "amount": 20.9,
        },
        {
            "distributor": ["This field is required."],
            "asset_code": ["This field is required."],
        },
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "amount": 20.9,
        },
        {
            "target": ["This field is required."],
            "asset_code": ["This field is required."],
        },
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
        },
        {"amount": ["This field is required."]},
    ),
    (
        {
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "amount": 20.9,
        },
        {
            "issuer": ["This field is required."],
            "asset_code": ["This field is required."],
        },
    ),
    (
        {
            "asset_code": "TKN",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
        },
        {
            "issuer": ["This field is required."],
            "distributor": ["This field is required."],
            "amount": ["This field is required."],
        },
    ),
    (
        {
            "asset_code": "TKN",
        },
        {
            "issuer": ["This field is required."],
            "distributor": ["This field is required."],
            "target": ["This field is required."],
            "amount": ["This field is required."],
        },
    ),
    (
        {},
        {
            "issuer": ["This field is required."],
            "distributor": ["This field is required."],
            "target": ["This field is required."],
            "asset_code": ["This field is required."],
            "amount": ["This field is required."],
        },
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "asset_code": "LONGTOKENNAME",
            "amount": 10,
        },
        {"asset_code": ["Ensure this field has no more than 12 characters."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQL",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "asset_code": "TKN",
            "amount": 10,
        },
        {"issuer": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQL",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "asset_code": "TKN",
            "amount": 10,
        },
        {"distributor": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "asset_code": "TKN",
            "amount": -10,
        },
        {"amount": ["Ensure this value is greater than 0."]},
    ),
    (
        {
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "distributor": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "asset_code": "TKN",
            "amount": 0,
        },
        {"amount": ["Ensure this value is greater than 0."]},
    ),
)


MANAGE_DATA_FAIL_RESPONSES = (
    (
        {},
        {
            "public_key": ["This field is required."],
            "name": ["This field is required."],
        },
    ),
    (
        {"value": "Some value"},
        {
            "public_key": ["This field is required."],
            "name": ["This field is required."],
        },
    ),
    (
        {"public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF"},
        {
            "name": ["This field is required."],
        },
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "name": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec rhoncus elit vel porttitor vehicula. Nullam consequat efficitur magna at rutrum",
            "value": "Some value",
        },
        {"name": ["Ensure this field has no more than 64 characters."]},
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QFH",
            "name": "Some name",
            "value": "Some value",
        },
        {"public_key": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "name": "Some name",
            "value": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec rhoncus elit vel porttitor vehicula. Nullam consequat efficitur magna at rutrum",
        },
        {"value": ["Ensure this field has no more than 64 characters."]},
    ),
)

CREATE_CLAWBACK_FAIL_RESPONSES = (
    ({}, {"issuer": ["This field is required."]}),
    (
        {"issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QFH"},
        {"issuer": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {"issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF"},
        {
            "target": ["This field is required when Claimable ID is null."],
            "claimable_id": ["This field is required when Target is null."],
        },
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "claimable_id": "0000000021397a7e40986f05e43ede59a47b00c3c9ffad75da5065be3a95868c23c06a55",
        },
        {
            "target": ["This field must not be filled when Claimable ID has value."],
            "claimable_id": ["This field must not be filled when Target has value"],
        },
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
        },
        {
            "asset_code": ["This field is required."],
            "amount": ["This field is required."],
        },
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "amount": 40.4,
        },
        {
            "asset_code": ["This field is required."],
        },
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
        },
        {
            "amount": ["This field is required."],
        },
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TOKENTOKENTOKEN",
            "amount": 40.4,
        },
        {"asset_code": ["Ensure this field has no more than 12 characters."]},
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "amount": 0,
        },
        {"amount": ["Ensure this value is greater than 0."]},
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "amount": -10,
        },
        {"amount": ["Ensure this value is greater than 0."]},
    ),
)

UPDATE_AUTH_FLAG_FAIL_RESPONSES = (
    (
        {},
        {
            "issuer": ["This field is required."],
            "asset_code": ["This field is required."],
            "target": ["This field is required."],
        },
    ),
    (
        {"issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF"},
        {
            "asset_code": ["This field is required."],
            "target": ["This field is required."],
        },
    ),
    (
        {"asset_code": "TKN"},
        {"issuer": ["This field is required."], "target": ["This field is required."]},
    ),
    (
        {"target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF"},
        {
            "issuer": ["This field is required."],
            "asset_code": ["This field is required."],
        },
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
        },
        {"asset_code": ["This field is required."]},
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "asset_code": "TKN",
        },
        {"target": ["This field is required."]},
    ),
    (
        {
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "asset_code": "TKN",
        },
        {"issuer": ["This field is required."]},
    ),
    (
        {
            "target": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QFA",
            "issuer": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
        },
        {"target": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QFA",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
        },
        {"issuer": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKNTKNTKNTKNTKNTKNTKNTKN",
            "memo_text": "Some memo",
        },
        {"asset_code": ["Ensure this field has no more than 12 characters."]},
    ),
    (
        {
            "issuer": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "target": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "asset_code": "TKN",
            "memo_text": "Some memo very very very very very very very long",
        },
        {"memo_text": ["Ensure this field has no more than 28 characters."]},
    ),
)


SET_HOME_DOMAIN_FAIL_RESPONSES = (
    (
        {},
        {
            "public_key": ["This field is required."],
            "home_domain": ["This field is required."],
        },
    ),
    (
        {"home_domain": "domain.com"},
        {
            "public_key": ["This field is required."],
        },
    ),
    (
        {"public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF"},
        {
            "home_domain": ["This field is required."],
        },
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "home_domain": "veryveryveryveryveryverylongdomain.com",
        },
        {"home_domain": ["Ensure this field has no more than 32 characters."]},
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QFH",
            "home_domain": "domain.com",
        },
        {"public_key": ["Ensure this field has no more than 56 characters."]},
    ),
)


GENERATE_TOML_SUCCESS_RESPONSES = (
    ({}, TOML_LIST[0]),
    (
        {
            "general_info": {
                "accounts": [
                    "GDBCIQ764FRXBKLR47Y3BYJ3ZJWZ663XO64LCSYNK3X27EW6NGMKOXJW"
                ],
            },
            "org_doc": {
                "name": "Org name",
                "dba": "Org dba",
                "url": "https://domain.org",
                "logo": "https://www.domain.org/images/logo-icon.png",
                "description": "Some organization description.",
                "physical_address": "P.O. Box 2681 Road Town, Tortola BVI",
                "twitter": "orgtwitter",
                "github": "orggithub",
                "official_email": "official@domain.org",
                "support_email": "support@domain.org",
            },
            "point_of_contact_doc": [
                {
                    "name": "John Doe",
                    "email": "john@domain.org",
                }
            ],
            "currency_doc": [
                {
                    "code": "TKN",
                    "issuer": "GDYSPBVZHPQTYMGSYNOHRZQNLB3ZWFVQ2F7EP7YBOLRGD42XIC3QUX5G",
                    "status": "live",
                    "name": "Token Name",
                    "description": "Token description",
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
        },
        TOML_LIST[2],
    ),
)

GENERATE_TOML_FAIL_RESPONSES = (
    (
        {
            "general_info": {
                "federation_server": "string",
                "auth_server": "string",
                "transfer_server": "string",
                "transfer_server_sep24": "string",
                "kyc_server": "string",
                "web_auth_endpoint": "string",
                "signing_key": "GDYSPBVZHPQTYMGSYNOHRZQNLB3ZWFVQ2F7EP7YBOLRGD42XIC3QUX5GB",
                "accounts": [
                    "GDYSPBVZHPQTYMGSYNOHRZQNLB3ZWFVQ2F7EP7YBOLRGD42XIC3QUX5GB"
                ],
                "horizon_url": "string",
                "uri_request_signing_key": "GDYSPBVZHPQTYMGSYNOHRZQNLB3ZWFVQ2F7EP7YBOLRGD42XIC3QUX5GB",
                "direct_payment_server": "string",
                "anchor_quote_server": "string",
            }
        },
        {
            "general_info": {
                "federation_server": [
                    "Only URLs with HTTPS are allowed.",
                    "Enter a valid URL.",
                ],
                "auth_server": [
                    "Only URLs with HTTPS are allowed.",
                    "Enter a valid URL.",
                ],
                "transfer_server": [
                    "Only URLs with HTTPS are allowed.",
                    "Enter a valid URL.",
                ],
                "transfer_server_sep24": [
                    "Only URLs with HTTPS are allowed.",
                    "Enter a valid URL.",
                ],
                "kyc_server": [
                    "Only URLs with HTTPS are allowed.",
                    "Enter a valid URL.",
                ],
                "web_auth_endpoint": [
                    "Only URLs with HTTPS are allowed.",
                    "Enter a valid URL.",
                ],
                "signing_key": ["Ensure this field has no more than 56 characters."],
                "horizon_url": ["Enter a valid URL."],
                "accounts": {
                    "0": ["Ensure this field has no more than 56 characters."]
                },
                "uri_request_signing_key": [
                    "Ensure this field has no more than 56 characters."
                ],
                "direct_payment_server": [
                    "Only URLs with HTTPS are allowed.",
                    "Enter a valid URL.",
                ],
                "anchor_quote_server": [
                    "Only URLs with HTTPS are allowed.",
                    "Enter a valid URL.",
                ],
            }
        },
    ),
    (
        {
            "org_doc": {
                "url": "string",
                "logo": "string",
                "physical_address_attestation": "string",
                "phone_number_attestation": "string",
            }
        },
        {
            "org_doc": {
                "url": ["Only URLs with HTTPS are allowed.", "Enter a valid URL."],
                "logo": ["Enter a valid URL."],
                "physical_address_attestation": [
                    "Only URLs with HTTPS are allowed.",
                    "Enter a valid URL.",
                ],
                "phone_number_attestation": [
                    "Only URLs with HTTPS are allowed.",
                    "Enter a valid URL.",
                ],
            }
        },
    ),
    (
        {
            "currency_doc": [
                {
                    "code": "TKNTKKNTKNTKNTKTN",
                    "code_template": "TKNTKKNTKNTKNTKTN",
                    "issuer": "GDYSPBVZHPQTYMGSYNOHRZQNLB3ZWFVQ2F7EP7YBOLRGD42XIC3QUX5GB",
                    "status": "invalid-status",
                    "display_decimals": 8,
                    "name": "GDYSPBVZHPQTYMGSYNOHRZQNLB3ZWFVQ2F7EP7YB",
                    "image": "string",
                    "anchor_asset_type": "invalid-type",
                    "attestation_of_reserve": "string",
                    "approval_server": "string",
                },
                {
                    "display_decimals": -1,
                },
            ]
        },
        {
            "currency_doc": [
                {
                    "code": ["Ensure this field has no more than 12 characters."],
                    "code_template": [
                        "Ensure this field has no more than 12 characters."
                    ],
                    "issuer": ["Ensure this field has no more than 56 characters."],
                    "status": ['"invalid-status" is not a valid choice.'],
                    "display_decimals": [
                        "Ensure this value is less than or equal to 7."
                    ],
                    "name": ["Ensure this field has no more than 20 characters."],
                    "image": ["Enter a valid URL."],
                    "anchor_asset_type": ['"invalid-type" is not a valid choice.'],
                    "attestation_of_reserve": ["Enter a valid URL."],
                    "approval_server": ["Enter a valid URL."],
                },
                {
                    "display_decimals": [
                        "Ensure this value is greater than or equal to 0."
                    ]
                },
            ]
        },
    ),
)

RETRIEVE_TOML_ENDPOINT_RESPONSE = {
    "general_info": {
        "federation_server": None,
        "auth_server": None,
        "transfer_server": "https://ultrastellar.com/sep6",
        "transfer_server_sep24": "https://ultrastellar.com/sep24",
        "kyc_server": None,
        "web_auth_endpoint": "https://ultrastellar.com/auth",
        "signing_key": "GA3UK3JHOYYD3TAUH5C7NDOUDWBRF5FC4MECXFA2VRPEHIDQUOJIVOAJ",
        "horizon_url": None,
        "accounts": [
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
        "uri_request_signing_key": None,
        "direct_payment_server": None,
        "anchor_quote_server": None,
    },
    "org_doc": {
        "name": "Ultra Stellar LLC",
        "dba": "Ultra Stellar",
        "url": "https://ultrastellar.com/",
        "logo": "https://ultrastellar.com/static/images/org_logo.png",
        "description": "Ultra Stellar is building the future of money on the Stellar network. Our products provide access to a new financial infrastructure that helps anyone in the world to achieve financial freedom.",
        "physical_address": "Tallinn, Estonia",
        "physical_address_attestation": None,
        "phone_number": None,
        "phone_number_attestation": None,
        "keybase": None,
        "twitter": "ultrastellarhq",
        "github": None,
        "official_email": "hello@ultrastellar.com",
        "support_email": "support@ultrastellar.com",
        "licensing_authority": None,
        "license_type": None,
        "license_number": None,
    },
    "point_of_contact_doc": [
        {
            "name": "Gleb Pitsevich",
            "email": "gleb@ultrastellar.com",
            "keybase": None,
            "telegram": None,
            "twitter": None,
            "github": None,
            "id_photo_hash": None,
            "verification_photo_hash": None,
        },
        {
            "name": "Dmitri Gmyza",
            "email": "dima@ultrastellar.com",
            "keybase": None,
            "telegram": None,
            "twitter": None,
            "github": None,
            "id_photo_hash": None,
            "verification_photo_hash": None,
        },
    ],
    "currency_doc": [
        {
            "code": "yUSDC",
            "code_template": None,
            "issuer": "GDGTVWSM4MGS4T7Z6W4RPWOCHE2I6RDFCIFZGS3DOA63LWQTRNZNTTFF",
            "status": "live",
            "display_decimals": None,
            "name": None,
            "description": "yUSDC is an interest earning USDC tethered token. Earn interest on your USDC by holding yUSDC. yUSDC are liquid tokens that you can trade, redeem or send at any time. 1 yUSDC is always redeemable for 1 USDC through Ultra Stellar anchor. SDEX trading is live on yUSDC/USDC pair.",
            "conditions": "The interest share is distributed daily to yUSDC holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "image": "https://ultrastellar.com/static/images/icons/yUSDC.png",
            "fixed_number": None,
            "max_number": None,
            "is_unlimited": None,
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "USDC",
            "attestation_of_reserve": None,
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "collateral_addresses": None,
            "collateral_address_messages": None,
            "collateral_address_signatures": None,
            "regulated": None,
            "approval_server": None,
            "approval_criteria": None,
        },
        {
            "code": "yXLM",
            "code_template": None,
            "issuer": "GARDNV3Q7YGT4AKSDF25LT32YSCCW4EV22Y2TV3I2PU2MMXJTEDL5T55",
            "status": "live",
            "display_decimals": None,
            "name": None,
            "description": "yXLM is an interest earning XLM tethered token. Earn interest on your XLM by holding yXLM. yXLM are liquid tokens that you can trade, redeem or send at any time. 1 yXLM is always redeemable for 1 XLM through Ultra Stellar anchor.",
            "conditions": "The interest share is distributed daily to yXLM holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "image": "https://ultrastellar.com/static/images/icons/yXLM.png",
            "fixed_number": None,
            "max_number": None,
            "is_unlimited": None,
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "XLM",
            "attestation_of_reserve": None,
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "collateral_addresses": None,
            "collateral_address_messages": None,
            "collateral_address_signatures": None,
            "regulated": None,
            "approval_server": None,
            "approval_criteria": None,
        },
        {
            "code": "yETH",
            "code_template": None,
            "issuer": "GDYQNEF2UWTK4L6HITMT53MZ6F5QWO3Q4UVE6SCGC4OMEQIZQQDERQFD",
            "status": "live",
            "display_decimals": None,
            "name": None,
            "description": "yETH is an interest earning ETH tethered token. Earn interest on your ETH by holding yETH. yETH are liquid tokens that you can trade, redeem or send at any time. 1 yETH is always redeemable for 1 ETH through Ultra Stellar anchor. SDEX trading is live on yETH/ETH (ultrastellar.com) pair.",
            "conditions": "The interest share is distributed daily to yETH holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "image": "https://ultrastellar.com/static/images/icons/yETH.png",
            "fixed_number": None,
            "max_number": None,
            "is_unlimited": None,
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "ETH",
            "attestation_of_reserve": None,
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "collateral_addresses": None,
            "collateral_address_messages": None,
            "collateral_address_signatures": None,
            "regulated": None,
            "approval_server": None,
            "approval_criteria": None,
        },
        {
            "code": "yBTC",
            "code_template": None,
            "issuer": "GBUVRNH4RW4VLHP4C5MOF46RRIRZLAVHYGX45MVSTKA2F6TMR7E7L6NW",
            "status": "live",
            "display_decimals": None,
            "name": None,
            "description": "yBTC is an interest earning BTC tethered token. Earn interest on your BTC by holding yBTC. yBTC are liquid tokens that you can trade, redeem or send at any time. 1 yBTC is always redeemable for 1 BTC through Ultra Stellar anchor. SDEX trading is live on yBTC/BTC (ultrastellar.com) pair.",
            "conditions": "The interest share is distributed daily to yBTC holders. The APY rates are published at ultrastellar.com/assets and may change depending on market conditions.",
            "image": "https://ultrastellar.com/static/images/icons/yBTC.png",
            "fixed_number": None,
            "max_number": None,
            "is_unlimited": None,
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "BTC",
            "attestation_of_reserve": None,
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "collateral_addresses": None,
            "collateral_address_messages": None,
            "collateral_address_signatures": None,
            "regulated": None,
            "approval_server": None,
            "approval_criteria": None,
        },
        {
            "code": "ETH",
            "code_template": None,
            "issuer": "GBFXOHVAS43OIWNIO7XLRJAHT3BICFEIKOJLZVXNT572MISM4CMGSOCC",
            "status": "live",
            "display_decimals": None,
            "name": None,
            "description": "This is a tethered ETH token issued by Ultra Stellar. For each ETH in circulation on Stellar, Ultra Stellar holds the same amount of Ether in reserves. SDEX trading is live on ETH/USDC pair.",
            "conditions": "To get a 1:1 conversion between ETH on Stellar and native Ether use Deposit / Withdraw functionality supported in most Stellar wallets.",
            "image": "https://ultrastellar.com/static/images/icons/ETH.png",
            "fixed_number": None,
            "max_number": None,
            "is_unlimited": None,
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "ETH",
            "attestation_of_reserve": None,
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "collateral_addresses": None,
            "collateral_address_messages": None,
            "collateral_address_signatures": None,
            "regulated": None,
            "approval_server": None,
            "approval_criteria": None,
        },
        {
            "code": "BTC",
            "code_template": None,
            "issuer": "GDPJALI4AZKUU2W426U5WKMAT6CN3AJRPIIRYR2YM54TL2GDWO5O2MZM",
            "status": "live",
            "display_decimals": None,
            "name": None,
            "description": "This is a tethered BTC token issued by Ultra Stellar. For each BTC in circulation on Stellar, Ultra Stellar holds the same amount of Bitcoin in reserves. SDEX trading is live on BTC/USDC pair.",
            "conditions": "To get a 1:1 conversion between BTC on Stellar and native Bitcoin use Deposit / Withdraw functionality supported in most Stellar wallets.",
            "image": "https://ultrastellar.com/static/images/icons/BTC.png",
            "fixed_number": None,
            "max_number": None,
            "is_unlimited": None,
            "is_asset_anchored": True,
            "anchor_asset_type": "crypto",
            "anchor_asset": "BTC",
            "attestation_of_reserve": None,
            "redemption_instructions": "Redeemable through any SEP-24 compliant Stellar wallet such as LOBSTR, StellarTerm or StellarX.",
            "collateral_addresses": None,
            "collateral_address_messages": None,
            "collateral_address_signatures": None,
            "regulated": None,
            "approval_server": None,
            "approval_criteria": None,
        },
    ],
}

SET_OPTIONS_FAIL_RESPONSES = (
    (
        {},
        {
            "public_key": ["This field is required."],
            "clawback": ["This field is required."],
            "freeze": ["This field is required."],
        },
    ),
    (
        {"public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF"},
        {
            "clawback": ["This field is required."],
            "freeze": ["This field is required."],
        },
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "clawback": True,
        },
        {
            "freeze": ["This field is required."],
        },
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "freeze": True,
        },
        {
            "clawback": ["This field is required."],
        },
    ),
    (
        {
            "freeze": True,
            "clawback": True,
        },
        {
            "public_key": ["This field is required."],
        },
    ),
    (
        {"freeze": True, "clawback": False, "signers": []},
        {
            "public_key": ["This field is required."],
        },
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "signers": ["GASRMD3E5IQUI655V2PWX6ZQI2AKO5ZG35NYDZKFGIBFL7GG6FZTLU3R"],
        },
        {
            "clawback": ["This field is required."],
            "freeze": ["This field is required."],
        },
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QFA",
            "freeze": False,
            "clawback": True,
            "signers": None,
        },
        {"public_key": ["Ensure this field has no more than 56 characters."]},
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "freeze": True,
            "clawback": True,
            "signers": ["GASRMD3E5IQUI655V2PWX6ZQI2AKO5ZG35NYDZKFGIBFL7GG6FZTLU3RA"],
        },
        {"signers": {"0": ["Ensure this field has no more than 56 characters."]}},
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "freeze": "str",
            "clawback": True,
            "signers": ["GASRMD3E5IQUI655V2PWX6ZQI2AKO5ZG35NYDZKFGIBFL7GG6FZTLU3R"],
        },
        {"freeze": ["Must be a valid boolean."]},
    ),
    (
        {
            "public_key": "GBRPP6LBZXSCBNBP2K2DRRVUKAWRBVMKZ2J27HT23VEFZP54WT7JY4QF",
            "freeze": False,
            "clawback": "str",
            "signers": ["GASRMD3E5IQUI655V2PWX6ZQI2AKO5ZG35NYDZKFGIBFL7GG6FZTLU3R"],
        },
        {"clawback": ["Must be a valid boolean."]},
    ),
)
