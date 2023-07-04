class ResponseManager:
    def __init__(self, actions):
        """
        Initializes a ResponseManager instance.

        Args:
            actions: An instance of the Actions class.
        """
        self.actions = actions

    async def __call__(self, data):
        """
        Handles the response data.

        Args:
            data: The response data to be handled.

        Returns:
            The result of handling the response data.
        """
        event = data.get('event')
        try:
            if event in ['info', 'subscribed', 'unsubscribed', 'error', 'logger_in']:
                return await getattr(self.actions, f'handle_{event}')(data)
            elif event in ['snapshot', 'update']:
                topic = data.get('topic')
                topic_prefix = topic.split(':')[0]
                handler_method = f'handle_{topic_prefix.replace("/", "_")}'
                if hasattr(self.actions, handler_method):
                    return await getattr(self.actions, handler_method)(data)
                else:
                    raise ValueError(f"Unrecognized data received: {topic}")
            else:
                raise ValueError(f"Unrecognized event received: {event}")
        except NameError:
            raise ValueError("Class not found")

