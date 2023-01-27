CREATE_PATH_PAYMENT_FAIL_RESPONSES = (
    (
        {
            "destination_public_key": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQA",
            "receive_amount": 1000,
            "user_id": "user1",
        },
        {
            "destination_public_key": [
                "Ensure this field has no more than 56 characters."
            ]
        },
    ),
    (
        {"receive_amount": 1000, "user_id": "user1"},
        {"destination_public_key": ["This field is required."]},
    ),
    (
        {
            "destination_public_key": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "user_id": "user1",
        },
        {"receive_amount": ["This field is required."]},
    ),
    (
        {
            "destination_public_key": "GDRE45CHJRRDU47BI3IAUHDL6V5WEVJLE57IXYAGJIAWETLPTSTHUVIQ",
            "receive_amount": 1000,
        },
        {"user_id": ["This field is required."]},
    ),
)
