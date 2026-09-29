def allocate_budget(planner: str, budget: float) -> dict:
    if planner == "home":
        return {
            "Furniture": round(budget * 0.35, 2),
            "Lighting": round(budget * 0.15, 2),
            "Fans & Appliances": round(budget * 0.20, 2),
            "Decor": round(budget * 0.15, 2),
            "Reserve": round(budget * 0.15, 2),
        }

    if planner == "party":
        return {
            "Catering": round(budget * 0.45, 2),
            "Decoration": round(budget * 0.20, 2),
            "Entertainment": round(budget * 0.15, 2),
            "Venue/Stay": round(budget * 0.10, 2),
            "Reserve": round(budget * 0.10, 2),
        }

    return {
        "Jewelry": round(budget * 0.75, 2),
        "Accessories": round(budget * 0.10, 2),
        "Packaging/Delivery": round(budget * 0.05, 2),
        "Reserve": round(budget * 0.10, 2),
    }


def demo_recommendations(planner: str, budget: float, details: dict):
    allocation = allocate_budget(planner, budget)

    if planner == "home":
        items = [
            ("Furniture", "Compact modular furniture set", "₹" + f"{allocation['Furniture']:,.0f}", "IKEA / Amazon", "Balances usability and available budget."),
            ("Lighting", "Warm LED ceiling and ambient lights", "₹" + f"{allocation['Lighting']:,.0f}", "Amazon", "Low-energy lighting can reduce running cost."),
            ("Fans & Appliances", "Energy-efficient ceiling fan and basic appliances", "₹" + f"{allocation['Fans & Appliances']:,.0f}", "Amazon / Flipkart", "Keeps essential appliances within the planned limit."),
            ("Decor", "Minimal wall and table decor package", "₹" + f"{allocation['Decor']:,.0f}", "IKEA / Amazon", "Adds style without consuming the main furniture budget."),
        ]
        tips = ["Measure rooms before buying furniture.", "Keep the reserve amount for delivery or unexpected costs.", "Compare specifications and warranty before purchase."]

    elif planner == "party":
        items = [
            ("Catering", "Budget-friendly menu with per-person cost target", "₹" + f"{allocation['Catering']:,.0f}", "Swiggy / Zomato", "Food usually forms a major part of event spending."),
            ("Decoration", "Theme-based balloons, backdrop and table setup", "₹" + f"{allocation['Decoration']:,.0f}", "Local vendors / online stores", "Creates a consistent event theme."),
            ("Entertainment", "Playlist + simple games or compact entertainment setup", "₹" + f"{allocation['Entertainment']:,.0f}", "Local vendors", "Keeps entertainment within a controlled allocation."),
            ("Venue/Stay", "Compare venue or accommodation options", "₹" + f"{allocation['Venue/Stay']:,.0f}", "OYO / local venues", "Allows the planner to compare location and budget."),
        ]
        tips = ["Confirm guest count before finalizing food.", "Keep a small reserve for last-minute purchases.", "Check vendor cancellation and delivery terms."]

    else:
        items = [
            ("Jewelry", "Occasion-appropriate minimal jewelry set", "₹" + f"{allocation['Jewelry']:,.0f}", "Amazon / Flipkart", "Designed around the stated budget and occasion."),
            ("Accessories", "Matching accessory option", "₹" + f"{allocation['Accessories']:,.0f}", "Online marketplace", "Adds coordination without using the core jewelry budget."),
            ("Packaging/Delivery", "Delivery and gift packaging allowance", "₹" + f"{allocation['Packaging/Delivery']:,.0f}", "Marketplace", "Keeps additional charges visible."),
        ]
        tips = ["Check material, size and return policy.", "For an outfit image, use color/style as guidance rather than relying only on appearance.", "Keep a reserve for delivery or size adjustments."]

    return items, tips, allocation
