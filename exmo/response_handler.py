class ResponseHandler:
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