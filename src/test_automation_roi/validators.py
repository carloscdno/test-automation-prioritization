def validate_non_negative_integer(value):
    if not value:
        return "Please answer this question"
    try:
        numeric = int(value)
    except ValueError:
        return "Please enter an integer greater than or equal to 0"
    if numeric < 0:
        return "Please enter an integer greater than or equal to 0"
    return True
