import streamlit as st
from predictor import predict_400

st.title("Lewis & Clark 400m Predictor")

name = st.text_input("Athlete Name")



pr_100 = st.number_input("100m PR", min_value=0.0, step=0.01)
pr_200 = st.number_input("200m PR", min_value=0.0, step=0.01)
pr_400 = st.number_input("Current 400m PR", min_value=0.0, step=0.01)

recent_400 = st.number_input("Most Recent 400m", min_value=0.0, step=0.01)
workout_300 = st.number_input("Best Recent 300m Workout", min_value=0.0, step=0.01)
goal_400 = st.number_input("Goal 400m Time", min_value=0.0, step=0.01)
fatigue = st.slider("Fatigue Level", 1, 5, 3)
prediction_type = st.selectbox(
    "Prediction Type",
    [
        "Current Fitness",
        "Championship/Tapered",
        "Long-Term Potential"
    ]
)

if st.button("Predict 400m"):

    result = predict_400(
        pr_100,
        pr_200,
        pr_400,
        recent_400,
        workout_300,
        fatigue,
        prediction_type
    )

    if result is None:
        st.warning("Enter at least one mark to predict.")
    else:
        prediction = result["prediction"]
        confidence = result["confidence"]
        estimates = result["estimates"]
        limiter = result["limiter"]
        confidence = min(95, len(estimates) * 20)

        st.subheader(f"Prediction for {name}")
        st.metric("Projected 400m", f"{prediction:.2f}")
        st.metric("Confidence", f"{confidence}%")
        st.metric("Primary Limiter", limiter)
        st.write(f"Prediction Type: {prediction_type}")
        st.write(f"Likely range: **{prediction - 0.35:.2f} - {prediction + 0.35:.2f}**")
        st.caption("This is an estimate based on available marks, not a guarantee. Use it as a coaching reference point.")

        st.subheader("Inputs Used")

        for label, value, weight in estimates:
            st.write(f"{label}: {value:.2f} (weight {weight:.0%})")
        if goal_400 > 0:
            st.subheader("Goal Time Targets")

            goal_200 = (goal_400 - 5.8) / 2
            goal_100 = (goal_400 - 7.2) / 4
            goal_300 = goal_400 - 12.5

            st.write(f"To target **{goal_400:.2f}**, rough supporting marks could be:")

            st.write(f"100m speed: around **{goal_100:.2f}**")
            st.write(f"200m speed: around **{goal_200:.2f}**")
            st.write(f"300m workout: around **{goal_300:.2f}**")

            gap = prediction - goal_400

            if gap <= 0:
                st.success("This goal is within or below the current projection range.")
            elif gap <= 0.75:
                st.info("This goal is close. It likely requires a strong race, good competition, and clean execution.")
            elif gap <= 1.5:
                st.warning("This goal is aggressive. It may require improvement in speed, speed endurance, or race execution.")
            else:
                st.error("This goal is a longer-term target based on the current profile.")