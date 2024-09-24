# total revenue
import datetime


class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # diplay purpose only
    WHITE = 4  # data is missing for this field

# This is a already written for your reference
def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.

    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the first financial entry where the "nature" key is equal to "STANDALONE".
    If no standalone financial entry is found, it returns 0.

    Parameters:
    - data (dict): A dictionary containing a list of financial entries under the "financials" key.

    Returns:
    - int: The index of the latest standalone financial entry or 0 if not found.
    """
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index: int):
    financials = data.get("financials", [])
    if financial_index < len(financials):
        pnl = financials[financial_index].get("pnl", {})
        revenue = pnl.get("lineItems", {}).get("netRevenue", 0)
        return revenue
    return 0


def total_borrowing(data: dict, financial_index: int):
    financials = data.get("financials", [])
    if financial_index < len(financials):
        bs = financials[financial_index].get("bs", {})
        long_term_borrowing = bs.get("longTermBorrowings", 0)
        short_term_borrowing = bs.get("shortTermBorrowings", 0)
        total_revenue_value = total_revenue(data, financial_index)
        if total_revenue_value > 0:
            return (long_term_borrowing + short_term_borrowing) / total_revenue_value
    return 0

def iscr_flag(data: dict, financial_index: int):
    iscr_value = iscr(data, financial_index)
    if iscr_value >= 2:
        return FLAGS.GREEN
    return FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index: int):
    total_revenue_value = total_revenue(data, financial_index)
    if total_revenue_value >= 50_000_000:  # 50 million
        return FLAGS.GREEN
    return FLAGS.RED


def iscr(data: dict, financial_index: int):
    financials = data.get("financials", [])
    if financial_index < len(financials):
        pnl = financials[financial_index].get("pnl", {})
        ebit = pnl.get("ebit", 0)
        interest_expenses = pnl.get("interestExpenses", 1)  # Adding 1 to avoid division by zero
        return (ebit + 1) / (interest_expenses + 1)
    return 0

def borrowing_to_revenue_flag(data: dict, financial_index: int):
    borrowing_ratio = total_borrowing(data, financial_index)
    if borrowing_ratio <= 0.25:
        return FLAGS.GREEN
    return FLAGS.AMBER


