class Controller:
    def __init__(self, actions):
        self.actions = actions
        self.api_websocket_state = {}

    async def __call__(self, data):
        event = data.get('event')
        try:
            if event in ['info', 'subscribed', 'unsubscribed', 'error', 'logger_in']:
                self.api_websocket_state[event] = data
            elif event in ['snapshot', 'update']:
                topic = data.get('topic')
                if topic == 'spot/user_trades':
                    return await self.actions.handle_user_trades(data)
                elif topic.startswith('spot/trades:'):
                    return await self.actions.handle_trades(data)
                elif topic.startswith('spot/ticker:'):
                    return await self.actions.handle_ticker(data)
                elif topic.startswith('spot/wallet'):
                    return await self.actions.handle_wallet(data)
                elif topic.startswith('spot/orders'):
                    return await self.actions.handle_orders(data)
                elif topic.startswith('spot/order_book_snapshots:'):
                    return await self.actions.handle_order_book_snapshots(data)
                elif topic.startswith('spot/order_book_updates:'):
                    return await self.actions.handle_order_book_updates(data)
                else:
                    raise ValueError(f"Unrecognized data received: {topic}")
            else:
                raise ValueError(f"Unrecognized data received: {event}")
        except NameError:
            raise ValueError(f"Class not found")
