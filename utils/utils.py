def addThreePeriods(str: str, max: int):
    if len(str) > max:
        return str[0 : max - 3] + "..."
    return str
