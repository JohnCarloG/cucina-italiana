from decimal import Decimal

from app.core.config import settings
from app.models import Recipe, Wine


def calculate_recipe_price(recipe: Recipe, persone: int, vino: Wine | None = None) -> Decimal:
    if persone <= 0:
        raise ValueError("persone must be positive")
    base_porzione = recipe.prezzo_base_porzione()
    totale = base_porzione * Decimal(persone)
    totale += Decimal(settings.price_service_fee)
    if vino and vino.prezzo:
        totale += Decimal(vino.prezzo)
    return totale.quantize(Decimal("0.01"))
