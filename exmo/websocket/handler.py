from abc import ABC, abstractmethod


class AbstractResponseHandler(ABC):
    @abstractmethod
    def __init__(self, data):
        print(data)


class InfoResponseHandler(AbstractResponseHandler):
    def __init__(self, data):
        print(data)


class SubscribedResponseHandler(AbstractResponseHandler):
    def __init__(self, data):
        print(data)


class ErrorResponseHandler(AbstractResponseHandler):
    def __init__(self, data):
        print(data)


class UnsubscribedResponseHandler(AbstractResponseHandler):
    def __init__(self, data):
        print(data)


class UserTradesResponseHandler(AbstractResponseHandler):
    def __init__(self, data):
        print(data)


class TradesResponseHandler(AbstractResponseHandler):
    def __init__(self, data):
        print(data)


class TickerResponseHandler(AbstractResponseHandler):
    def __init__(self, data):
        print(data)


class WalletResponseHandler(AbstractResponseHandler):
    def __init__(self, data):
        print(data)


class OrdersResponseHandler(AbstractResponseHandler):
    def __init__(self, data):
        print(data)


class OrderBookResponseHandler(AbstractResponseHandler):
    def __init__(self, data):
        print(data)


class ResponseHandlerFactory:
    @staticmethod
    def __call__(data):
        event = data.get('event')
        try:
            if event == 'info':
                return InfoResponseHandler(data)
            elif event == 'subscribed':
                return SubscribedResponseHandler(data)
            elif event == 'error':
                return ErrorResponseHandler(data)
            elif event == 'unsubscribed':
                return UnsubscribedResponseHandler(data)
            elif event in ['snapshot', 'update']:
                topic = data.get('topic')
                if topic == 'spot/user_trades':
                    return UserTradesResponseHandler(data)
                elif topic.startswith('spot/trades:'):
                    return TradesResponseHandler(data)
                elif topic.startswith('spot/ticker:'):
                    return TickerResponseHandler(data)
                elif topic.startswith('spot/wallet'):
                    return WalletResponseHandler(data)
                elif topic.startswith('spot/orders'):
                    return OrdersResponseHandler(data)
                elif topic.startswith('spot/order_book_snapshots:') or topic.startswith('spot/order_book_updates:'):
                    return OrderBookResponseHandler(data)
                else:
                    raise ValueError(f"Unrecognized data received: {topic}")
            else:
                raise ValueError(f"Unrecognized data received: {event}")
        except NameError:
            raise ValueError(f"Class not found")
