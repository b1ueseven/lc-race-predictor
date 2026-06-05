import streamlit as st
from predictor import predict_400

st.title("Lewis & Clark 400m Predictor")

name = st.text_input("Athlete Name")



pr_100 = st.number_input("100m PR", min_value=0.0, step=0.01)
pr_200 = st.number_input("200m PR", min_value=0.0, step=0.01)
pr_400 = st.number_input("Current 400m PR", min_value=0.0, step=0.01)

recent_400 = st.number_input("Most Recent 400m", min_value=0.0, step=0.01)
relay_400_split = st.number_input(
    "Recent 4x400 Relay Split",
    min_value=0.0,
    step=0.01
)
special_distance = st.selectbox(
    "Recent Special Endurance Distance",
    [150, 200, 300]
)

special_time = st.number_input(
    "Recent Special Endurance Time",
    min_value=0.0,
    step=0.01
)
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
        relay_400_split,
        special_distance,
        special_time,
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
        st.metric("Most Likely Race Time for 400m", f"{prediction:.2f}")
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

            gap = prediction - goal_400

            suggested_200 = None
            suggested_300 = None

            if pr_200 > 0:
                if gap <= 0.75:
                    suggested_200 = pr_200 - 0.10
                elif gap <= 1.5:
                    suggested_200 = pr_200 - 0.20
                else:
                    suggested_200 = pr_200 - 0.35
            else:
                suggested_200 = (goal_400 - 5.8) / 2

            if special_distance == 300 and special_time > 0:
                if gap <= 0.75:
                    suggested_300 = special_time - 0.40
                elif gap <= 1.5:
                    suggested_300 = special_time - 0.80
                else:
                    suggested_300 = special_time - 1.20
            else:
                suggested_300 = goal_400 - 12.5

            st.write(f"To target **{goal_400:.2f}**, the most useful supporting marks are likely:")

            st.write(f"200m speed: around **{suggested_200:.2f}**")
            st.write(f"300m special endurance: around **{suggested_300:.2f}**")

            st.caption(
                "These are development targets based on the athlete's current profile, not strict requirements."
            )

            if gap <= 0:
                st.success("This goal is within or below the current projection range.")
            elif gap <= 0.75:
                st.info("This goal is close. It likely requires a strong race, good competition, and clean execution.")
            elif gap <= 1.5:
                st.warning("This goal is aggressive. It may require improvement in speed, speed endurance, or race execution.")
            else:
                st.error("This goal is a longer-term target based on the current profile.")