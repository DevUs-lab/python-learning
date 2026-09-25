"""
Expense Tracker - Professional Version
A CLI app to track daily expenses with validation and JSON persistence.

Features:
    - Add / view / edit / delete expenses
    - Categories, search, totals, monthly + category reports
    - Validated input, crash-safe menu, auto-save/load from JSON
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import List

DATA_FILE = Path(__file__).with_name("expenses.json")
DATE_FORMAT = "%Y-%m-%d"
DEFAULT_CATEGORY = "General"
EXIT_CHOICE = 8


@dataclass
class Expense:
    """Represents a single expense record."""

    date: str
    item: str
    description: str
    price: float
    category: str = DEFAULT_CATEGORY

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("Price cannot be negative.")
        # Normalise empty category from old / manual data.
        if not self.category or not self.category.strip():
            self.category = DEFAULT_CATEGORY
        else:
            self.category = self.category.strip().title()


def load_expenses(path: Path = DATA_FILE) -> List[Expense]:
    """Load expenses from JSON. Returns [] if missing/corrupt. Handles old files."""
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            raw_data = json.load(f)
        expenses: List[Expense] = []
        for entry in raw_data:
            if not isinstance(entry, dict):
                continue
            expenses.append(
                Expense(
                    date=str(entry.get("date", "")),
                    item=str(entry.get("item", "")),
                    description=str(entry.get("description", "")),
                    price=float(entry.get("price", 0)),
                    category=str(entry.get("category", DEFAULT_CATEGORY)),
                )
            )
        return expenses
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"Warning: could not load '{path.name}': {exc}. Starting fresh.")
        return []


def save_expenses(expenses: List[Expense], path: Path = DATA_FILE) -> None:
    """Persist expenses to a JSON file."""
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump([asdict(e) for e in expenses], f, indent=4)
    except OSError as exc:
        print(f"Error: could not save expenses: {exc}")


# ---------- input helpers ----------

def get_non_empty_input(prompt: str) -> str:
    """Prompt until the user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_valid_date(prompt: str) -> str:
    """Prompt until the user enters a valid date (YYYY-MM-DD)."""
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, DATE_FORMAT)
            return value
        except ValueError:
            print(f"Invalid date. Use format YYYY-MM-DD (e.g. 2026-09-24).")


def get_valid_price(prompt: str) -> float:
    """Prompt until the user enters a valid non-negative number."""
    while True:
        value = input(prompt).strip()
        try:
            price = float(value)
            if price < 0:
                print("Price cannot be negative. Please try again.")
                continue
            return price
        except ValueError:
            print("Invalid price. Enter a number (e.g. 250.50).")


def get_category(prompt: str = "Enter category [General]: ") -> str:
    """Prompt for a category; empty input returns the default."""
    value = input(prompt).strip()
    return value.title() if value else DEFAULT_CATEGORY


def get_menu_choice(first: int = 1, last: int = EXIT_CHOICE) -> int:
    """Prompt for a menu choice in range, crash-safe."""
    valid = {str(n) for n in range(first, last + 1)}
    while True:
        raw = input(f"Please enter your choice ({first}-{last}): ").strip()
        if raw in valid:
            return int(raw)
        print(f"Invalid choice. Enter a number between {first} and {last}.")


def get_expense_number(expenses: List[Expense], action: str) -> int:
    """Prompt for a valid 1-based expense number, return 0-based index."""
    while True:
        raw = input(f"Enter expense No. to {action} (1-{len(expenses)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(expenses):
            return int(raw) - 1
        print("Invalid number. Please try again.")


# ---------- core actions ----------

def display_menu() -> None:
    """Print the main menu."""
    print("\n====== Expense Tracker ======")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Show Total Spent")
    print("4. Search Expenses")
    print("5. Edit Expense")
    print("6. Delete Expense")
    print("7. Monthly / Category Report")
    print(f"{EXIT_CHOICE}. Exit")


def add_expense(expenses: List[Expense]) -> None:
    """Collect validated input and append a new expense."""
    print("\n--- Add New Expense ---")
    date = get_valid_date(f"Enter date [{DATE_FORMAT}]: ")
    item = get_non_empty_input("Enter item name: ")
    category = get_category()
    description = input("Enter description (optional): ").strip()
    price = get_valid_price("Enter price: ")

    expenses.append(
        Expense(date=date, item=item, description=description, price=price, category=category)
    )
    save_expenses(expenses)
    print("Expense added successfully.")


def list_expenses(expenses: List[Expense]) -> None:
    """Display all expenses in a readable table."""
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n====== Your Expenses ======")
    print(f"{'No.':<5} {'Date':<12} {'Item':<15} {'Category':<13} {'Price':>10}  Description")
    print("-" * 80)
    for index, e in enumerate(expenses, start=1):
        print(
            f"{index:<5} {e.date:<12} {e.item:<15} {e.category:<13} "
            f"{e.price:>10.2f}  {e.description}"
        )


def show_total(expenses: List[Expense]) -> None:
    """Show grand total plus a per-category breakdown."""
    if not expenses:
        print("No expenses recorded yet.")
        return
    total = sum(e.price for e in expenses)
    print(f"\nTotal spent on {len(expenses)} item(s): {total:.2f}/-")

    by_category: dict[str, float] = defaultdict(float)
    for e in expenses:
        by_category[e.category] += e.price
    print("\n--- By Category ---")
    for cat in sorted(by_category):
        print(f"  {cat:<15}: {by_category[cat]:>10.2f}")


def search_expenses(expenses: List[Expense]) -> None:
    """Search by keyword across item, description and category."""
    if not expenses:
        print("No expenses recorded yet.")
        return
    keyword = input("Enter search keyword: ").strip().lower()
    if not keyword:
        print("Search cancelled (empty keyword).")
        return

    matches = [
        (i, e)
        for i, e in enumerate(expenses, start=1)
        if keyword in e.item.lower()
        or keyword in e.description.lower()
        or keyword in e.category.lower()
    ]
    if not matches:
        print(f"No expenses matching '{keyword}'.")
        return

    print(f"\nFound {len(matches)} match(es):")
    print(f"{'No.':<5} {'Date':<12} {'Item':<15} {'Category':<13} {'Price':>10}  Description")
    print("-" * 80)
    for i, e in matches:
        print(
            f"{i:<5} {e.date:<12} {e.item:<15} {e.category:<13} "
            f"{e.price:>10.2f}  {e.description}"
        )


def edit_expense(expenses: List[Expense]) -> None:
    """Edit one expense in place. Press Enter to keep the current value."""
    if not expenses:
        print("No expenses recorded yet.")
        return
    list_expenses(expenses)
    idx = get_expense_number(expenses, "edit")
    current = expenses[idx]
    print(f"\n--- Editing expense #{idx + 1} (Enter to keep current) ---")

    # Date (optional, validated if changed)
    while True:
        raw = input(f"Date [{current.date}]: ").strip()
        if not raw:
            new_date = current.date
            break
        try:
            datetime.strptime(raw, DATE_FORMAT)
            new_date = raw
            break
        except ValueError:
            print(f"Invalid date. Use {DATE_FORMAT} or press Enter to keep.")

    new_item = input(f"Item [{current.item}]: ").strip() or current.item
    new_category = input(f"Category [{current.category}]: ").strip() or current.category
    raw_desc = input(f"Description [{current.description}] (Enter=keep, 'clear'=empty): ").strip()
    if raw_desc.lower() == "clear":
        new_description = ""
    else:
        new_description = raw_desc or current.description

    while True:
        raw = input(f"Price [{current.price:.2f}]: ").strip()
        if not raw:
            new_price = current.price
            break
        try:
            new_price = float(raw)
            if new_price < 0:
                print("Price cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid price. Enter a number or press Enter to keep.")

    expenses[idx] = Expense(
        date=new_date,
        item=new_item,
        description=new_description,
        price=new_price,
        category=new_category,
    )
    save_expenses(expenses)
    print("Expense updated successfully.")


def delete_expense(expenses: List[Expense]) -> None:
    """Delete one expense after confirmation."""
    if not expenses:
        print("No expenses recorded yet.")
        return
    list_expenses(expenses)
    idx = get_expense_number(expenses, "delete")
    target = expenses[idx]
    confirm = input(
        f"Delete #{idx + 1} '{target.item}' ({target.price:.2f})? (y/N): "
    ).strip().lower()
    if confirm != "y":
        print("Delete cancelled.")
        return
    del expenses[idx]
    save_expenses(expenses)
    print("Expense deleted successfully.")


def monthly_report(expenses: List[Expense]) -> None:
    """Group totals by month (YYYY-MM) with per-category lines."""
    if not expenses:
        print("No expenses recorded yet.")
        return

    monthly: dict[str, list[Expense]] = defaultdict(list)
    for e in expenses:
        try:
            key = datetime.strptime(e.date, DATE_FORMAT).strftime("%Y-%m")
        except ValueError:
            key = "Unknown"
        monthly[key].append(e)

    print("\n====== Monthly Report ======")
    for month in sorted(monthly):
        items = monthly[month]
        total = sum(e.price for e in items)
        print(f"\n{month} — {len(items)} item(s), total: {total:.2f}/-")
        by_cat: dict[str, float] = defaultdict(float)
        for e in items:
            by_cat[e.category] += e.price
        for cat in sorted(by_cat):
            print(f"    {cat:<15}: {by_cat[cat]:>10.2f}")


def main() -> None:
    """Application entry point - main menu loop."""
    expenses = load_expenses()
    actions = {
        1: add_expense,
        2: list_expenses,
        3: show_total,
        4: search_expenses,
        5: edit_expense,
        6: delete_expense,
        7: monthly_report,
    }

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == EXIT_CHOICE:
            print("Thanks for using Expense Tracker. Goodbye!")
            break

        try:
            actions[choice](expenses)
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as exc:  # safeguard: never crash the menu loop
            print(f"An unexpected error occurred: {exc}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
