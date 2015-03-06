from website.server import LiveSite
from web_mock_shop import TEST_SHOP

s = LiveSite(TEST_SHOP)
s.start()
