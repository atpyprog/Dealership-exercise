from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

@dataclass(frozen=True)
class Vehicle:
    plate: str
    model: str
    color: str
    price: float


@dataclass(frozen=True)
class Seller:
    seller_id: str
    name: str


@dataclass
class Sale:
    vehicle_plate: str
    seller_id: str
    sold_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        when = self.sold_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"Sale(plate={self.vehicle_plate}, seller={self.seller_id}, at={when})"

class Dealership:
    """
    A very small dealership manager:
    - Keeps vehicles in memory
    - Keeps sellers in memory
    - Records sales
    - Computes available stock (unsold vehicles)
    """

    def __init__(self, vehicles: List[Vehicle], sellers: List[Seller]) -> None:
        self._vehicles: Dict[str, Vehicle] = {v.plate: v for v in vehicles}
        self._sellers: Dict[str, Seller] = {s.seller_id: s for s in sellers}
        self._sales: Dict[str, Sale] = {}  # key: vehicle plate

    def list_available_stock(self) -> List[Vehicle]:
        """Return vehicles that are not sold yet."""
        return [v for plate, v in self._vehicles.items() if plate not in self._sales]

    def list_sales(self) -> List[Sale]:
        """Return all recorded sales."""
        return list(self._sales.values())

    def sales_by_seller(self, seller_id: str) -> List[Sale]:
        """Return sales filtered by seller."""
        return [sale for sale in self._sales.values() if sale.seller_id == seller_id]

    def find_vehicle(self, plate: str) -> Optional[Vehicle]:
        return self._vehicles.get(plate)

    def find_seller(self, seller_id: str) -> Optional[Seller]:
        return self._sellers.get(seller_id)

    def record_sale(self, plate: str, seller_id: str) -> Sale:
        """
        Record a sale:
        - Validates vehicle exists and is not sold
        - Validates seller exists
        - Stores the sale with timestamp
        """
        if plate not in self._vehicles:
            raise ValueError(f"Vehicle with plate '{plate}' does not exist.")

        if plate in self._sales:
            raise ValueError(f"Vehicle '{plate}' is already sold.")

        if seller_id not in self._sellers:
            raise ValueError(f"Seller '{seller_id}' does not exist.")

        sale = Sale(vehicle_plate=plate, seller_id=seller_id, sold_at=datetime.now())
        self._sales[plate] = sale
        return sale


def euro(amount: float) -> str:
    return f"€ {amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

#Principal
if __name__ == "__main__":
    vehicles = [
        Vehicle(plate="AA-10-BB", model="Fiat Panda", color="White", price=7500.00),
        Vehicle(plate="CC-20-DD", model="VW Golf", color="Black", price=14500.00),
        Vehicle(plate="EE-30-FF", model="Renault Clio", color="Blue", price=9800.00),
    ]

    sellers = [
        Seller(seller_id="S001", name="Marina"),
        Seller(seller_id="S002", name="Carlos"),
    ]

    d = Dealership(vehicles=vehicles, sellers=sellers)

    print("\n=== INITIAL STOCK ===")
    for v in d.list_available_stock():
        print(f"{v.plate} | {v.model} | {v.color} | {euro(v.price)}")

    print("\n=== RECORDING SALE ===")
    sale = d.record_sale(plate="CC-20-DD", seller_id="S001")
    print(sale)

    print("\n=== STOCK AFTER SALE ===")
    for v in d.list_available_stock():
        print(f"{v.plate} | {v.model} | {v.color} | {euro(v.price)}")

    print("\n=== ALL SALES ===")
    for s in d.list_sales():
        v = d.find_vehicle(s.vehicle_plate)
        seller = d.find_seller(s.seller_id)
        print(f"{s.sold_at:%Y-%m-%d %H:%M:%S} | Plate: {s.vehicle_plate} ({v.model}) | Seller: {seller.name} ({s.seller_id})")

    print("\n=== SALES BY SELLER S001 ===")
    for s in d.sales_by_seller("S001"):
        v = d.find_vehicle(s.vehicle_plate)
        seller = d.find_seller(s.seller_id)
        print(f"{s.sold_at:%Y-%m-%d %H:%M:%S} | {seller.name} sold {v.model} ({v.plate}) for {euro(v.price)}")
