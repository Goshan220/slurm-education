from enum import Enum

import pytest

import swagger_client
from swagger_client import Pet


class PetStatus(Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"


@pytest.mark.parametrize("id, status", [(1, PetStatus.AVAILABLE), (2, PetStatus.PENDING), (3, PetStatus.SOLD)])
@pytest.mark.positive
def test_pet_creation(pet_api, id, status, tags, category):
    pet = Pet(id=id, name="Barsik", category=category, photo_urls=["http://url1.com"], tags=tags, status=status.value)
    pet_api.add_pet(**pet.to_dict())

    actual_pet = pet_api.get_pet_by_id(id)
    assert pet.id == actual_pet.id, "Получен неверный ID"
    assert pet.name == actual_pet.name, "Получено неверное имя"
    assert pet.status == actual_pet.status, "Получен неверный статус"


@pytest.mark.negative
def test_photo_urls_negative(tags, category):
    with pytest.raises(ValueError):
        pet = Pet(id=1, name="Barsik", category=category, photo_urls=None, tags=tags, status=PetStatus.AVAILABLE.value)
