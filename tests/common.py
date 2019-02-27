"""Test the helper method for writing tests."""
from pathlib import Path
import tempfile

from hass_nabucasa.client import CloudClient


def mock_coro(return_value=None, exception=None):
    """Return a coro that returns a value or raise an exception."""
    return mock_coro_func(return_value, exception)()


def mock_coro_func(return_value=None, exception=None):
    """Return a method to create a coro function that returns a value."""

    async def coro(*args, **kwargs):
        """Fake coroutine."""
        if exception:
            raise exception
        return return_value

    return coro


class TestClient(CloudClient):
    """Interface class for Home Assistant."""

    def __init__(self, loop, websession):
        """Initialize TestClient."""
        self._loop = loop
        self._websession = websession
        self._cloudhooks = {}

        self.mock_user = []
        self.mock_alexa = []
        self.mock_google = []
        self.mock_webhooks = []

        self.mock_return = []

    @property
    def base_path(self):
        """Return path to base dir."""
        return Path(tempfile.gettempdir())

    @property
    def loop(self):
        """Return client loop."""
        return self._loop

    @property
    def websession(self):
        """Return client session for aiohttp."""
        raise self._websession

    @property
    def app(self):
        """Return client webinterface aiohttp application."""
        raise NotImplementedError()

    @property
    def cloudhooks(self):
        """Return list of cloudhooks."""
        return self._cloudhooks

    async def async_user_message(
        self, identifier: str, title: str, message: str
    ) -> None:
        """Create a message for user to UI."""
        self.mock_user.append((identifier, title, message))

    async def async_alexa_message(self, payload):
        """process cloud alexa message to client."""
        self.mock_alexa.append(payload)
        return self.mock_return.pop()

    async def async_google_message(self, payload):
        """Process cloud google message to client."""
        self.mock_google.append(payload)
        return self.mock_return.pop()

    async def async_webhook_message(self, payload):
        """Process cloud webhook message to client."""
        self.mock_webhooks.append(payload)
        return self.mock_return.pop()

    async def async_cloudhooks_update(self, data):
        """Update internal cloudhooks data."""
        self._cloudhooks = data