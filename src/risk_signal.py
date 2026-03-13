def generate_risk_score(delta_h, std_baseline):
    """
    Generates a risk score based on the ΔH and the standard deviation of the baseline entropy.
    """
    z_score = delta_h / std_baseline
    
    if z_score < 2:
        return 0  # Normal
    elif 2 <= z_score < 3:
        return 1  # Warning
    else:
        return 2  # Critical

def format_risk_message(level):
    messages = {
        0: "STATUS: OK",
        1: "STATUS: WARNING",
        2: "STATUS: CRITICAL"
    }
    return messages.get(level, "Unknown")