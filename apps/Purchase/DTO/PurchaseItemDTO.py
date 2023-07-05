from typing import List
from Purchase.models import PurchaseItem

class PurchaseItemDTO():
    products: List[PurchaseItem] = []
    login_failed = False
    total_spends_current = 0.0
    total_spends_last_referred = 0.0
    show_spends = False
        

  