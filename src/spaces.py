from dataclasses import dataclass
from random import randint
from typing import Optional


@dataclass
class Meta:
    name: str
    color: Optional[str] = None
    buying_price: int = 0
    building_price: int = 0
    rent: int = 0
    rent_with_one_house: int = 0
    rent_with_two_houses: int = 0
    rent_with_three_houses: int = 0
    rent_with_four_houses: int = 0
    rent_with_hotel: int = 0


@dataclass
class Space:
    meta: Meta
    houses: int = 0
    hotel: bool = False
    owned_by: Optional[int] = None
    mortgaged: bool = False


_meta = [
    Meta(
        name="Go",
    ),
    Meta(
        name="Mediterranean Avenue",
        color="Brown",
        buying_price=60,
        building_price=50,
        rent=2,
        rent_with_one_house=10,
        rent_with_two_houses=30,
        rent_with_three_houses=90,
        rent_with_four_houses=160,
        rent_with_hotel=250,
    ),
    Meta(
        name="Community Chest",
    ),
    Meta(
        name="Baltic Avenue",
        color="Brown",
        buying_price=60,
        building_price=50,
        rent=4,
        rent_with_one_house=20,
        rent_with_two_houses=60,
        rent_with_three_houses=180,
        rent_with_four_houses=320,
        rent_with_hotel=450,
    ),
    Meta(
        name="Income Tax",
    ),
    Meta(
        name="Reading Railroad",
        buying_price=200,
    ),
    Meta(
        name="Oriental Avenue",
        color="Light Blue",
        buying_price=100,
        building_price=50,
        rent=6,
        rent_with_one_house=30,
        rent_with_two_houses=90,
        rent_with_three_houses=270,
        rent_with_four_houses=400,
        rent_with_hotel=550,
    ),
    Meta(
        name="Chance",
    ),
    Meta(
        name="Vermont Avenue",
        color="Light Blue",
        buying_price=100,
        building_price=50,
        rent=6,
        rent_with_one_house=30,
        rent_with_two_houses=90,
        rent_with_three_houses=270,
        rent_with_four_houses=400,
        rent_with_hotel=550,
    ),
    Meta(
        name="Connecticut Avenue",
        color="Light Blue",
        buying_price=120,
        building_price=50,
        rent=8,
        rent_with_one_house=40,
        rent_with_two_houses=100,
        rent_with_three_houses=300,
        rent_with_four_houses=450,
        rent_with_hotel=600,
    ),
    Meta(
        name="Jail / Just Visiting",
    ),
    Meta(
        name="St. Charles Place",
        color="Pink",
        buying_price=140,
        building_price=100,
        rent=10,
        rent_with_one_house=50,
        rent_with_two_houses=150,
        rent_with_three_houses=450,
        rent_with_four_houses=625,
        rent_with_hotel=750,
    ),
    Meta(
        name="Electric Company",
        buying_price=150,
    ),
    Meta(
        name="States Avenue",
        color="Pink",
        buying_price=140,
        building_price=100,
        rent=10,
        rent_with_one_house=50,
        rent_with_two_houses=150,
        rent_with_three_houses=450,
        rent_with_four_houses=625,
        rent_with_hotel=750,
    ),
    Meta(
        name="Virginia Avenue",
        color="Pink",
        buying_price=160,
        building_price=100,
        rent=12,
        rent_with_one_house=60,
        rent_with_two_houses=180,
        rent_with_three_houses=500,
        rent_with_four_houses=700,
        rent_with_hotel=900,
    ),
    Meta(
        name="Pennsylvania Railroad",
        buying_price=200,
    ),
    Meta(
        name="St. James Place",
        color="Orange",
        buying_price=180,
        building_price=100,
        rent=14,
        rent_with_one_house=70,
        rent_with_two_houses=200,
        rent_with_three_houses=550,
        rent_with_four_houses=750,
        rent_with_hotel=950,
    ),
    Meta(
        name="Community Chest",
    ),
    Meta(
        name="Tennessee Avenue",
        color="Orange",
        buying_price=180,
        building_price=100,
        rent=14,
        rent_with_one_house=70,
        rent_with_two_houses=200,
        rent_with_three_houses=550,
        rent_with_four_houses=750,
        rent_with_hotel=950,
    ),
    Meta(
        name="New York Avenue",
        color="Orange",
        buying_price=200,
        building_price=100,
        rent=16,
        rent_with_one_house=80,
        rent_with_two_houses=220,
        rent_with_three_houses=600,
        rent_with_four_houses=800,
        rent_with_hotel=1000,
    ),
    Meta(
        name="Free Parking",
    ),
    Meta(
        name="Kentucky Avenue",
        color="Red",
        buying_price=220,
        building_price=150,
        rent=18,
        rent_with_one_house=90,
        rent_with_two_houses=250,
        rent_with_three_houses=700,
        rent_with_four_houses=875,
        rent_with_hotel=1050,
    ),
    Meta(
        name="Chance",
    ),
    Meta(
        name="Indiana Avenue",
        color="Red",
        buying_price=220,
        building_price=150,
        rent=18,
        rent_with_one_house=90,
        rent_with_two_houses=250,
        rent_with_three_houses=700,
        rent_with_four_houses=875,
        rent_with_hotel=1050,
    ),
    Meta(
        name="Illinois Avenue",
        color="Red",
        buying_price=240,
        building_price=150,
        rent=20,
        rent_with_one_house=100,
        rent_with_two_houses=300,
        rent_with_three_houses=750,
        rent_with_four_houses=925,
        rent_with_hotel=1100,
    ),
    Meta(
        name="B. & O. Railroad",
        buying_price=200,
    ),
    Meta(
        name="Atlantic Avenue",
        color="Yellow",
        buying_price=260,
        building_price=150,
        rent=22,
        rent_with_one_house=110,
        rent_with_two_houses=330,
        rent_with_three_houses=800,
        rent_with_four_houses=975,
        rent_with_hotel=1150,
    ),
    Meta(
        name="Ventnor Avenue",
        color="Yellow",
        buying_price=260,
        building_price=150,
        rent=22,
        rent_with_one_house=110,
        rent_with_two_houses=330,
        rent_with_three_houses=800,
        rent_with_four_houses=975,
        rent_with_hotel=1150,
    ),
    Meta(
        name="Waterworks",
        buying_price=150,
    ),
    Meta(
        name="Marvin Gardens",
        color="Yellow",
        buying_price=280,
        building_price=200,
        rent=24,
        rent_with_one_house=120,
        rent_with_two_houses=360,
        rent_with_three_houses=850,
        rent_with_four_houses=1025,
        rent_with_hotel=1200,
    ),
    Meta(
        name="Go To Jail",
    ),
    Meta(
        name="Pacific Avenue",
        color="Green",
        buying_price=300,
        building_price=200,
        rent=26,
        rent_with_one_house=130,
        rent_with_two_houses=390,
        rent_with_three_houses=900,
        rent_with_four_houses=1100,
        rent_with_hotel=1275,
    ),
    Meta(
        name="North Carolina Avenue",
        color="Green",
        buying_price=300,
        building_price=200,
        rent=26,
        rent_with_one_house=130,
        rent_with_two_houses=390,
        rent_with_three_houses=900,
        rent_with_four_houses=1100,
        rent_with_hotel=1275,
    ),
    Meta(
        name="Community Chest",
    ),
    Meta(
        name="Pennsylvania Avenue",
        color="Green",
        buying_price=320,
        building_price=200,
        rent=28,
        rent_with_one_house=150,
        rent_with_two_houses=450,
        rent_with_three_houses=1000,
        rent_with_four_houses=1200,
        rent_with_hotel=1400,
    ),
    Meta(
        name="Short Line",
        buying_price=200,
    ),
    Meta(
        name="Chance",
    ),
    Meta(
        name="Park Place",
        color="Dark Blue",
        buying_price=350,
        building_price=200,
        rent=35,
        rent_with_one_house=175,
        rent_with_two_houses=500,
        rent_with_three_houses=1100,
        rent_with_four_houses=1300,
        rent_with_hotel=1500,
    ),
    Meta(
        name="Luxury Tax",
    ),
    Meta(
        name="Boardwalk",
        color="Dark Blue",
        buying_price=400,
        building_price=200,
        rent=50,
        rent_with_one_house=200,
        rent_with_two_houses=600,
        rent_with_three_houses=1400,
        rent_with_four_houses=1700,
        rent_with_hotel=2000,
    ),
]

# Individual spaces
GO = 0
JAIL = next(i for i, s in enumerate(_meta) if s.name == "Jail / Just Visiting")
GO_TO_JAIL = next(i for i, s in enumerate(_meta) if s.name == "Go To Jail")
FREE_PARKING = next(i for i, s in enumerate(_meta) if s.name == "Free Parking")
INCOME_TAX = next(i for i, s in enumerate(_meta) if s.name == "Income Tax")
LUXURY_TAX = next(i for i, s in enumerate(_meta) if s.name == "Luxury Tax")
BOARDWALK = next(i for i, s in enumerate(_meta) if s.name == "Boardwalk")
ILLINOIS_AVENUE = next(i for i, s in enumerate(_meta) if s.name == "Illinois Avenue")
ST_CHARLES_PLACE = next(i for i, s in enumerate(_meta) if s.name == "St. Charles Place")
READING_RAILROAD = next(i for i, s in enumerate(_meta) if s.name == "Reading Railroad")

# Groups
CHANCES = list(i for i, s in enumerate(_meta) if s.name == "Chance")
RAILROADS = list(
    i
    for i, s in enumerate(_meta)
    if s.name.endswith("Railroad") or s.name == "Short Line"
)
COMMUNITY_CHESTS = list(i for i, s in enumerate(_meta) if s.name == "Community Chest")
UTILITIES = list(
    i
    for i, s in enumerate(_meta)
    if s.name == "Electric Company" or s.name == "Waterworks"
)

def _space_name(space: int) -> str:
    return _meta[space].name

def rent_value(board: list[Space], space: Space) -> int:
    assert space.owned_by is not None
    if space.meta.name in map(_space_name, RAILROADS):
        owned_count = len(
            list(
                s
                for s in board
                if s.meta.name in map(_space_name, RAILROADS)
                and s.owned_by == space.owned_by
            )
        )
        match owned_count:
            case 1:
                return 25
            case 2:
                return 50
            case 3:
                return 100
            case 4:
                return 200
            case _:
                raise AssertionError(f"invalid railroad count {owned_count}")
    if space.meta.name in map(_space_name, UTILITIES):
        owned_count = len(
            list(
                s
                for s in board
                if s.meta.name in map(_space_name, UTILITIES)
                and s.owned_by == space.owned_by
            )
        )
        assert 0 < owned_count <= 2, f"invalid utility count {owned_count}"
        roll = randint(1, 6) * randint(1, 6)
        return 4 * roll if owned_count == 1 else 10 * roll
    assert space.meta.color is not None, f"unexpected space {space.meta.name}"
    match space.houses:
        case 0:
            rent = space.meta.rent
        case 1:
            rent = space.meta.rent_with_one_house
        case 2:
            rent = space.meta.rent_with_two_houses
        case 3:
            rent = space.meta.rent_with_three_houses
        case 4:
            rent = space.meta.rent_with_four_houses
        case _:
            raise AssertionError(
                f"invalid number of houses on {space.meta.name}: {space.houses}"
            )
    if space.hotel:  # overwrites 0 houses case
        rent = space.meta.rent_with_hotel
    return (
        rent * 2
        if player_owns_all_color(board, space.meta.color, space.owned_by)
        else rent
    )

def board() -> list[Space]:
    return [Space(m) for m in _meta]


def next_railroad(start: int) -> int:
    return next(i for i in RAILROADS if start > i or RAILROADS[0])


def next_utility(start: int) -> int:
    return next(i for i in UTILITIES if start > i or UTILITIES[0])

def player_owns_all_color(board: list[Space], color: str, player_id: int) -> bool:
    color_count = len(list(s for s in board if s.meta.color == color))
    owned_count = len(
        list(
            s
            for s in board
            if s.meta.color == color and s.owned_by == player_id
        )
    )
    return color_count == owned_count

