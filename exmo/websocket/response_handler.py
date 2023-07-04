class ResponseHandler:
    def __init__(self, actions):
        self.actions = actions

    async def __call__(self, data):
        event = data.get('event')
        try:
            if event == 'info':
                return await self.actions.handle_info(data)
            elif event == 'subscribed':
                return await self.actions.handle_subscribed(data)
            elif event == 'error':
                return await self.actions.handle_error(data)
            elif event == 'unsubscribed':
                return await self.actions.handle_unsubscribed(data)
            elif event == 'logged_in':
                return await self.actions.handle_logged_in(data)
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
