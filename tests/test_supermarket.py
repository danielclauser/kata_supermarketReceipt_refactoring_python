import pytest

from supermarket_receipt.model_objects import Product, ProductUnit, SpecialOfferType
from supermarket_receipt.shopping_cart import ShoppingCart
from supermarket_receipt.teller import Teller
from tests.fake_catalog import FakeCatalog


def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert pytest.approx(receipt.total_price(), 0.01) == 4.975
    assert receipt.discounts == []
    assert len(receipt.items) == 1
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert receipt_item.price == 1.99
    assert pytest.approx(receipt_item.total_price, 0.01) == 2.5 * 1.99
    assert receipt_item.quantity == 2.5
