from decimal import Decimal

import pytest

from app.models import Ingredient, Recipe, RecipeIngredient
from app.services import calculate_recipe_price


def test_calculate_recipe_price_with_fee():
    recipe = Recipe(titolo="Test", porzioni_default=2)
    ingredient = Ingredient(nome="Farina", unita_base="g", prezzo_per_unita=Decimal("0.01"))
    item = RecipeIngredient(
        ingrediente=ingredient,
        ricetta=recipe,
        quantita_per_persona=Decimal("100"),
        unita_misura="g",
    )
    recipe.ingredienti = [item]
    price = calculate_recipe_price(recipe, persone=2, vino=None)
    assert price == Decimal("3.50")


@pytest.mark.parametrize(
    ("persone"),
    [0, -1],
)

def test_calculate_recipe_price_invalid_people(persone):
    recipe = Recipe(titolo="Test", porzioni_default=2)
    with pytest.raises(ValueError):
        calculate_recipe_price(recipe, persone=persone, vino=None)
