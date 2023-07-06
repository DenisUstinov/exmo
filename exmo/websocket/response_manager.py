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
        event = data.get("event")
        try:
            if event in ["info", "subscribed", "unsubscribed", "error", "logger_in"]:
                handler_method = f"handle_{event}"
                return await self._invoke_handler(handler_method, data)
            elif event in ["snapshot", "update"]:
                topic = data.get("topic")
                topic_prefix = topic.split(":")[0].split("/")[1]
                handler_method = f"handle_{topic_prefix}"
                return await self._invoke_handler(handler_method, data)
            else:
                raise ValueError(f"Unrecognized event received: {event}")
        except AttributeError as e:
            raise ValueError(str(e)) from None

    async def _invoke_handler(self, handler_method, data):
        """
        Invokes the specified handler method if it exists.

        Args:
            handler_method: The name of the handler method to invoke.
            data: The data to be passed to the handler method.

        Returns:
            The result of invoking the handler method.

        Raises:
            AttributeError: If the handler method does not exist.
        """
        if hasattr(self.actions, handler_method):
            return await getattr(self.actions, handler_method)(data)
        else:
            raise AttributeError(f"Handler method not found: {handler_method}")
