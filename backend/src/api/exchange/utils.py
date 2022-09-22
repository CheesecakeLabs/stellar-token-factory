def get_network(request):
    return request.headers.get("network", "TESTNET").upper()
