def calculate_base_roi(
    frequency,
    impact,
    stability,
    effort,
    dependencies,
):
    """
    Calculates the base automation ROI.

    Formula:
        (F * I * S) / (E * D)
    """
    if effort <= 0 or dependencies <= 0:
        raise ValueError(
            "Effort and dependencies must be greater than 0."
        )

    return (
        frequency
        * impact
        * stability
        / (effort * dependencies)
    )


def calculate_adjusted_roi(base_roi, reuse_count):
    """
    Adjusts the base ROI according to additional reuse opportunities.

    Formula:
        Base ROI * (1 + 0.2 * N)
    """
    if reuse_count < 0:
        raise ValueError(
            "Reuse count must be greater than or equal to 0."
        )

    return base_roi * (1 + 0.2 * reuse_count)