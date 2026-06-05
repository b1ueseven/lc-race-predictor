def predict_400(
    pr_100,
    pr_200,
    pr_400,
    recent_400,
    workout_300,
    fatigue,
    prediction_type
):
    estimates = []

    if pr_400 > 0:
        estimates.append(("400 PR", pr_400, 0.30))

    if recent_400 > 0:
        estimates.append(("Recent 400", recent_400, 0.35))

    if pr_200 > 0:
        estimates.append(("200 Speed Conversion", (pr_200 * 2) + 5.8, 0.20))

    if pr_100 > 0:
        estimates.append(("100 Speed Conversion", (pr_100 * 4) + 7.2, 0.10))

    if workout_300 > 0:
        estimates.append(("300 Workout Conversion", workout_300 + 12.5, 0.15))

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