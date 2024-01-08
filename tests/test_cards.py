import pytest

from alice_types import cards
import dataset


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.BIG_IMAGE_CARD["ERROR"]],
        *[data.values() for data in dataset.BIG_IMAGE_CARD["NOT_EMPTY"]],
    ]
)
def test_big_image_card(value, expected, raise_handler):
    with raise_handler:
        big_image = cards.BigImage.model_validate_json(value.string)
        assert big_image.model_dump_json().encode() == expected


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.ITEMS_LIST_CARD["ERROR"]],
        *[data.values() for data in dataset.ITEMS_LIST_CARD["NOT_EMPTY"]],
    ]
)
def test_items_list_card(value, expected, raise_handler):
    with raise_handler:
        items_list = cards.ItemsList.model_validate_json(value.string)
        assert items_list.model_dump_json().encode() == expected


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.IMAGE_GALLERY_CARD["ERROR"]],
        *[data.values() for data in dataset.IMAGE_GALLERY_CARD["NOT_EMPTY"]],
    ]
)
def test_image_gallery_card(value, expected, raise_handler):
    with raise_handler:
        image_gallery = cards.ImageGallery.model_validate_json(value.string)
        assert image_gallery.model_dump_json().encode() == expected
