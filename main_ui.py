
import streamlit as st
import json
from inference_engine import CarProblemEngine

# Load knowledge base
with open("knowledge_base.json") as f:
    knowledge_base = json.load(f)

engine = CarProblemEngine(knowledge_base)

# Streamlit App
def main():
    st.title("🚗 Garage Service Center Assistant")
    st.subheader("Answer questions to diagnose your vehicle's problem.")
    
    issue = st.selectbox("Select Issue:", [""] + list(knowledge_base["issues"].keys()))
    symptoms = knowledge_base["issues"].get(issue, [])
    symptom = st.selectbox("Select Symptom:", [""] + symptoms)

    if issue and symptom:
        st.write("### Answer the following questions:")
        answers = {}
        for rule in knowledge_base["rules"]:
            if rule["issue"] == issue and rule["symptom"] == symptom:
                for q in rule["questions"]:
                    answer = st.radio(q["question"], ["", "Yes", "No"], key=q["question"])
                    answers[q["question"]] = answer
                break

        if st.button("Diagnose"):
            if all(answers.values()):  # Ensure all questions are answered
                result = engine.diagnose(issue, symptom, answers)
                st.success("🔧 Diagnosis Result:")
                st.text(f"Solution: {result['solution']}")
                st.info(f"📄 Explanation: {result['explanation']}")
                st.warning(f"🔄 Alternative: {result['alternative']}")
            else:
                # Handle missing or mismatched answers
                st.warning("⚠️ Some answers didn't match the expectations. Here's the most likely solution:")
                result = engine.diagnose(issue, symptom, answers)
                st.text(f"Solution: {result['solution']}")
                st.info(f"📄 Explanation: {result['explanation']}")
                st.warning(f"🔄 Alternative: {result['alternative']}")

# Run app
if __name__ == "__main__":
    main()

