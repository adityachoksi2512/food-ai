RESTAURANT_NAME = "Bella Italia"

# Dietary tags:
#   V  = Vegetarian (no meat or fish)
#   VG = Vegan (no animal products)
#   GF = Gluten-Free

MENU = {
    "Starters": [
        {"name": "Garlic Bread",    "price": 4.99, "description": "Toasted bread with garlic butter",                         "tags": ["V"]},
        {"name": "Bruschetta",       "price": 6.99, "description": "Toasted bread with tomatoes, basil, and olive oil",        "tags": ["V", "VG"]},
        {"name": "Soup of the Day",  "price": 5.99, "description": "Ask your server for today's selection",                    "tags": []},
        {"name": "Caesar Salad",     "price": 8.99, "description": "Romaine lettuce, croutons, parmesan, Caesar dressing",    "tags": ["V", "GF"]},
    ],
    "Mains": [
        {"name": "Margherita Pizza",    "price": 13.99, "description": "Tomato sauce, mozzarella, fresh basil",                       "tags": ["V"]},
        {"name": "Pepperoni Pizza",     "price": 15.99, "description": "Tomato sauce, mozzarella, pepperoni",                         "tags": []},
        {"name": "Spaghetti Bolognese", "price": 14.99, "description": "Spaghetti with rich meat sauce",                             "tags": []},
        {"name": "Penne Arrabbiata",    "price": 12.99, "description": "Penne in spicy tomato sauce",                                "tags": ["V", "VG"]},
        {"name": "Chicken Parmesan",    "price": 17.99, "description": "Breaded chicken, marinara sauce, melted cheese",             "tags": []},
        {"name": "Grilled Salmon",      "price": 19.99, "description": "With lemon butter sauce and seasonal vegetables",            "tags": ["GF"]},
        {"name": "Mushroom Risotto",    "price": 13.99, "description": "Creamy risotto with mixed mushrooms",                        "tags": ["V", "GF"]},
    ],
    "Desserts": [
        {"name": "Tiramisu",            "price": 6.99, "description": "Classic Italian dessert with espresso and mascarpone", "tags": ["V"]},
        {"name": "Panna Cotta",         "price": 5.99, "description": "Creamy Italian dessert with berry coulis",            "tags": ["V", "GF"]},
        {"name": "Chocolate Lava Cake", "price": 7.99, "description": "Warm chocolate cake with a molten center",           "tags": ["V"]},
        {"name": "Gelato (2 scoops)",   "price": 4.99, "description": "Choice of vanilla, chocolate, or strawberry",        "tags": ["V", "GF"]},
    ],
    "Drinks": [
        {"name": "Soft Drink",         "price": 2.99, "description": "Coke, Diet Coke, Sprite, or Fanta", "tags": ["V", "VG", "GF"]},
        {"name": "Fresh Orange Juice", "price": 3.99, "description": "Freshly squeezed",                  "tags": ["V", "VG", "GF"]},
        {"name": "Sparkling Water",    "price": 2.49, "description": "500ml bottle",                      "tags": ["V", "VG", "GF"]},
        {"name": "Still Water",        "price": 1.99, "description": "500ml bottle",                      "tags": ["V", "VG", "GF"]},
        {"name": "House Wine (glass)", "price": 6.99, "description": "Red or white",                      "tags": ["V", "VG", "GF"]},
        {"name": "Italian Beer",       "price": 4.99, "description": "Peroni or Moretti",                 "tags": ["V", "VG"]},
        {"name": "Espresso",           "price": 2.49, "description": "Single shot",                       "tags": ["V", "VG", "GF"]},
        {"name": "Cappuccino",         "price": 3.49, "description": "Espresso with steamed milk",        "tags": ["V", "GF"]},
    ],
}


def get_menu_text():
    """Return the menu as a formatted string for the AI prompt."""
    lines = [
        f"=== {RESTAURANT_NAME} Menu ===",
        "",
        "Dietary tag key:",
        "  V  = Vegetarian",
        "  VG = Vegan",
        "  GF = Gluten-Free",
        "",
        "IMPORTANT FORMATTING RULE: Whenever you display menu items in a table,",
        "always use exactly these four columns in this order:",
        "  Item | Price | Description | Tags",
        "The Tags column must be the LAST column and must show the dietary symbols",
        "(e.g. V  VG  GF) separated by spaces. If an item has no tags, leave the cell blank.",
        "Never merge the tags into the Item or Description column.",
        "",
        "When a customer asks for vegetarian options, show only items whose tags include V or VG.",
        "When a customer asks for vegan options, show only items whose tags include VG.",
        "When a customer asks for gluten-free options, show only items whose tags include GF.",
        "",
    ]
    for category, items in MENU.items():
        lines.append(f"{category}:")
        for item in items:
            tag_str = "  ".join(item["tags"]) if item["tags"] else "—"
            lines.append(
                f"  - {item['name']}: ${item['price']:.2f} | {item['description']} | Tags: {tag_str}"
            )
        lines.append("")
    return "\n".join(lines)
