from django.urls import path

from . import views

urlpatterns = [
    path(
        "wallets/<str:public_key>/issuer-info",
        views.get_issuer_info,
        name="get-issuer-info",
    ),
    path(
        "wallets/<str:public_key>/account-options",
        views.get_account_options,
        name="get-account-options",
    ),
    path("wallets/set-auth-flag", views.set_authorized_flag, name="set-auth-flag"),
    path(
        "wallets/clear-auth-flag", views.clear_authorized_flag, name="clear-auth-flag"
    ),
    path("wallets/set-home-domain", views.set_home_domain, name="set-home-domain"),
    path(
        "wallets/set-options",
        views.set_account_options,
        name="set-options",
    ),
    path(
        "assets/<str:asset_code>/<str:asset_issuer>/distributor",
        views.get_asset_distributor,
        name="get-asset-distributor",
    ),
    path("assets/mint", views.mint_asset, name="mint-asset"),
    path("assets/burn", views.burn_asset, name="burn-asset"),
    path("assets/generate-toml", views.generate_toml, name="generate-toml"),
    path(
        "assets/retrieve-toml/<str:asset_issuer>",
        views.retrieve_toml,
        name="retrieve-toml",
    ),
    path("assets", views.create_asset, name="create-asset"),
    path("transactions/manage-data", views.manage_data, name="manage-data"),
    path("transactions/payment", views.create_payment, name="create-payment"),
    path("transactions/clawback", views.create_clawback, name="create-clawback"),
    path("transactions/submit", views.submit_envelope, name="submit-envelope"),
]
