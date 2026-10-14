def calculate_base_roi(
    frequency, 
    impact, 
    stability,
    effort,
    dependencies):
    base_roi = (frequency * impact * stability) / (effort * dependencies)
    return base_roi

def calculate_adjusted_roi(base_roi, reuse_factor):
    adjusted_roi = base_roi + (1 * 0.2 * reuse_factor)
    return adjusted_roi