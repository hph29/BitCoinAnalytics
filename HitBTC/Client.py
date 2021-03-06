import uuid
import time

import requests
from decimal import *

class Client(object):
    def __init__(self, secret_key, public_key):

        self.url = "https://api.hitbtc.com/api/2"
        self.session = requests.session()
        self.session.auth = (public_key, secret_key)

    def get_all_symbols(self):
        return self.session.get("%s/public/symbol" % self.url).json()

    def get_symbol(self, symbol_code):
        """Get symbol."""
        return self.session.get("%s/public/symbol/%s" % (self.url, symbol_code)).json()

    def get_candles(self, symbol_code, time_window, limit):
        """Get candle."""
        return self.session.get("%s/public/candles/%s?period=%s&limit=%s" % (self.url, symbol_code, time_window, limit)).json()

    def get_orderbook(self, symbol_code):
        """Get orderbook. """
        return self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()

    def get_address(self, currency_code):
        """Get address for deposit."""
        return self.session.get("%s/account/crypto/address/%s" % (self.url, currency_code)).json()

    def get_account_balance(self):
        """Get main balance."""
        return self.session.get("%s/account/balance" % self.url).json()

    def get_trading_balance(self):
        """Get trading balance."""
        return self.session.get("%s/trading/balance" % self.url).json()

    def transfer(self, currency_code, amount, to_exchange):
        return self.session.post("%s/account/transfer" % self.url, data={
            'currency': currency_code, 'amount': amount,
            'type': 'bankToExchange' if to_exchange else 'exchangeToBank'
        }).json()

    def new_order(self, client_order_id, symbol_code, side, quantity, price=None):
        """Place an order."""
        data = {'symbol': symbol_code, 'side': side, 'quantity': quantity}

        if price is not None:
            data['price'] = price

        return self.session.put("%s/order/%s" % (self.url, client_order_id), data=data).json()

    def get_order(self, client_order_id, wait=None):
        """Get order info."""
        data = {'wait': wait} if wait is not None else {}

        return self.session.get("%s/order/%s" % (self.url, client_order_id), params=data).json()

    def cancel_order(self, client_order_id):
        """Cancel order."""
        return self.session.delete("%s/order/%s" % (self.url, client_order_id)).json()

    def withdraw(self, currency_code, amount, address, network_fee=None):
        """Withdraw."""
        data = {'currency': currency_code, 'amount': amount, 'address': address}

        if network_fee is not None:
            data['networkfee'] = network_fee

        return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()

    def get_transaction(self, transaction_id):
        """Get transaction info."""
        return self.session.get("%s/account/transactions/%s" % (self.url, transaction_id)).json()


if __name__ == "__main__":
    public_key = "99e7e4c9c54de4fb9573c1567abaf6de"
    secret = "8ba4c30616651ff0fba08f7faaae0119"

    btc_address = "1ANJ18KJiL55adwzvNhRimnQcShR4iMvCe"

    client = Client()
    print(client.get_all_symbols())

    #print(client.get_candles('ETHBTC'))
