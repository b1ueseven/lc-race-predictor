def predict_400(
    pr_100,
    pr_200,
    pr_400,
    recent_400,
    relay_400_split,
    special_distance,
    special_time,
    fatigue,
    prediction_type
):
    estimates = []

    if pr_400 > 0:
        estimates.append(("400 PR", pr_400, 0.35))

    if recent_400 > 0:
        estimates.append(("Recent 400", recent_400, 0.40))

    if relay_400_split > 0:
        relay_estimate = relay_400_split + 0.40

        estimates.append(
            (
                "4x400 Relay Split Conversion",
                relay_estimate,
                0.25
            )
        )    

    if pr_200 > 0:
        estimates.append(("200 Speed Conversion", (pr_200 * 2) + 5.8, 0.10))

    if pr_100 > 0:
        estimates.append(("100 Speed Conversion", (pr_100 * 4) + 7.2, 0.05))

    if special_time > 0:

        if special_distance == 150:
            special_estimate = (special_time * 2.75) + 4.5
            special_label = "150m Special Endurance Conversion"
            special_weight = 0.08

        elif special_distance == 200:
            special_estimate = (special_time * 2) + 5.8
            special_label = "200m Special Endurance Conversion"
            special_weight = 0.12

        elif special_distance == 300:
            special_estimate = special_time + 12.5
            special_label = "300m Special Endurance Conversion"
            special_weight = 0.18

        estimates.append((special_label, special_estimate, special_weight))

    if not estimates:
        return None

    weighted_total = sum(value * weight for label, value, weight in estimates)
    weight_total = sum(weight for label, value, weight in estimates)

    prediction = weighted_total / weight_total

    fatigue_adjustment = (fatigue - 3) * 0.25
    prediction += fatigue_adjustment

    if prediction_type == "Championship/Tapered":
        prediction -= 0.30
    elif prediction_type == "Long-Term Potential":
        prediction -= 0.75

    confidence = min(95, len(estimates) * 20)

    limiter = "Balanced"

    if pr_200 > 0 and pr_400 > 0:

        speed_projection = (pr_200 * 2) + 5.8

        difference = pr_400 - speed_projection

        if difference > 1.0:
            limiter = "Speed Endurance"

        elif difference < -0.5:
            limiter = "Top-End Speed/Max Velocity"

        else:
            limiter = "Balanced"

    return {
        "prediction": prediction,
        "confidence": confidence,
        "estimates": estimates,
        "range_low": prediction - 0.35,
        "range_high": prediction + 0.35,
        "limiter": limiter
    }