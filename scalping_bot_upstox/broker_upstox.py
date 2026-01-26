from upstox_api.api import Upstox

class UpstoxBroker:
    def __init__(self, api_key, access_token):
        self.u = Upstox(api_key, access_token)
        self.u.get_master_contract('NSE_EQ')

    def place_order(self, symbol, side, qty):
        return self.u.place_order(
            transaction_type=side,
            instrument=self.u.get_instrument_by_symbol('NSE_EQ', symbol),
            quantity=qty,
            order_type='MARKET',
            product='MIS',
            duration='DAY'
        )
