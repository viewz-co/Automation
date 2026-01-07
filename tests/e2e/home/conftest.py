"""
Conftest for Home Page tests
Provides logged_in_page fixture
"""

import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def logged_in_page(perform_login_with_entity):
    """Get a logged-in page with entity selected"""
    return perform_login_with_entity

