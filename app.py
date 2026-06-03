import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Hospital AI Demo",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 AI-Powered Cardiac Emergency Workflow")
st.markdown(
    """
    **Workflow:**  
    Casualty → Smart Triage → Doctor Consultation → ECG →
    Cardiologist Alert → ICU → Discharge →
    Insurance → Follow-Up
    """
)

# -----------------------------
# OPENAI CLIENT
# -----------------------------
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
    #api_key=""
)

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------

if "patient" not in st.session_state:
    st.session_state.patient = {}

if "triage_result" not in st.session_state:
    st.session_state.triage_result = ""

if "consultation_summary" not in st.session_state:
    st.session_state.consultation_summary = ""

if "ecg_result" not in st.session_state:
    st.session_state.ecg_result = ""

if "icu_medications" not in st.session_state:
    st.session_state.icu_medications = ""

if "discharge_summary" not in st.session_state:
    st.session_state.discharge_summary = ""

if "insurance_summary" not in st.session_state:
    st.session_state.insurance_summary = ""

if "followup_message" not in st.session_state:
    st.session_state.followup_message = ""

if "step_completed" not in st.session_state:
    st.session_state.step_completed = {
        "Casualty": False,
        "Smart Triage": False,
        "Doctor Consultation": False,
        "ECG": False,
        "Cardiologist Alert": False,
        "ICU": False,
        "Discharge": False,
        "Insurance": False,
        "Follow-Up": False
    }

# -----------------------------
# HELPER FUNCTION
# -----------------------------
def call_gpt(prompt):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a hospital AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# -----------------------------
# WORKFLOW STATUS TRACKER
# -----------------------------
st.subheader("Patient Journey Status")

workflow_steps = [
    "Casualty",
    "Smart Triage",
    "Doctor Consultation",
    "ECG",
    "Cardiologist Alert",
    "ICU",
    "Discharge",
    "Insurance",
    "Follow-Up"
]

completed_steps = [
    step
    for step, completed
    in st.session_state.step_completed.items()
    if completed
]

# ---------------------------------
# CLEAN STATUS BAR UI
# ---------------------------------

status_html = ""

for step in workflow_steps:

    if step in completed_steps:
        bg_color = "#d4edda"
        border_color = "#28a745"
    else:
        bg_color = "#e9ecef"
        border_color = "#adb5bd"

    status_html += f"""
    <div style="
        min-width:180px;
        padding:15px;
        margin-right:12px;
        border-radius:12px;
        border:2px solid {border_color};
        background-color:{bg_color};
        text-align:center;
        font-size:20px;
        font-weight:600;
        white-space: nowrap;
        display:inline-block;
    ">
        {step}
    </div>
    """

st.markdown(
    f"""
    <div style="
        overflow-x:auto;
        white-space: nowrap;
        padding-bottom:10px;
    ">
        {status_html}
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# =====================================================
# PART 2 — CASUALTY REGISTRATION
# =====================================================

st.header("Step 1: Casualty Registration")

with st.expander("Patient Registration", expanded=True):

    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input(
            "Patient Name"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=58
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        symptoms = st.multiselect(
            "Symptoms",
            [
                "Chest Pain",
                "Sweating",
                "Shortness of Breath",
                "Fever",
                "Cough",
                "Vomiting",
                "Weakness",
                "Dizziness",
                "Palpitations"
            ],
            default=[
                "Chest Pain",
                "Sweating",
                "Shortness of Breath"
            ]
        )

    with col2:

        bp = st.text_input(
            "Blood Pressure",
            value="170/100"
        )

        pulse = st.number_input(
            "Pulse Rate",
            min_value=30,
            max_value=200,
            value=110
        )

        oxygen = st.number_input(
            "Oxygen Saturation (%)",
            min_value=50,
            max_value=100,
            value=92
        )

        temperature = st.number_input(
            "Temperature (°F)",
            min_value=90.0,
            max_value=110.0,
            value=98.6
        )

        medical_history = st.multiselect(
            "Medical History",
            [
                "Diabetes",
                "Hypertension",
                "Heart Disease",
                "Kidney Disease",
                "Asthma"
            ],
            default=[
                "Diabetes"
            ]
        )

    register_button = st.button(
        "Register Patient"
    )

    if register_button:

        st.session_state.patient = {
            "patient_id":
                f"HSP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": patient_name,
            "age": age,
            "gender": gender,
            "symptoms": symptoms,
            "bp": bp,
            "pulse": pulse,
            "oxygen": oxygen,
            "temperature": temperature,
            "medical_history": medical_history,
            "registration_time":
                str(datetime.now())
        }

        st.session_state.step_completed["Casualty"] = True

        st.success(
            "Patient Registered Successfully!"
        )

# =====================================================
# DISPLAY PATIENT DETAILS
# =====================================================

if st.session_state.patient:

    st.subheader("Patient Details")

    patient = st.session_state.patient

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Patient ID",
            patient["patient_id"]
        )

        st.metric(
            "Patient Name",
            patient["name"]
        )

    with col2:
        st.metric(
            "Age",
            patient["age"]
        )

        st.metric(
            "Gender",
            patient["gender"]
        )

    with col3:
        st.metric(
            "Blood Pressure",
            patient["bp"]
        )

        st.metric(
            "Oxygen",
            f"{patient['oxygen']}%"
        )

    st.write("### Symptoms")
    st.info(", ".join(patient["symptoms"]))

    st.write("### Medical History")
    st.success(", ".join(patient["medical_history"]))

    st.divider()

# =====================================================
# PART 3 — SMART EMERGENCY TRIAGE
# =====================================================

st.header("Step 2: Smart Emergency Triage")

if st.session_state.patient:

    if st.button("Analyze Emergency Risk"):

        patient = st.session_state.patient

        symptoms = ", ".join(
            patient["symptoms"]
        )

        history = ", ".join(
            patient["medical_history"]
        )

        prompt = f"""
        You are an emergency triage assistant.

        Analyze the patient risk.

        Patient Details:

        Name:
        {patient['name']}

        Age:
        {patient['age']}

        Gender:
        {patient['gender']}

        Symptoms:
        {symptoms}

        Blood Pressure:
        {patient['bp']}

        Pulse:
        {patient['pulse']}

        Oxygen:
        {patient['oxygen']}

        Temperature:
        {patient['temperature']}

        Medical History:
        {history}

        Provide response in EXACT format:

        Risk Category:
        RED / YELLOW / GREEN

        Possible Concern:
        <short explanation>

        Recommended Immediate Action:
        <bullet points>

        Important:
        - Do NOT diagnose
        - Only triage
        - Be medically cautious
        """

        with st.spinner(
            "Analyzing emergency risk..."
        ):

            result = call_gpt(prompt)

            st.session_state.triage_result = result
            st.session_state.step_completed["Smart Triage"] = True

# =====================================================
# DISPLAY TRIAGE RESULT
# =====================================================

if st.session_state.triage_result:

    st.subheader("🚨 Triage Result")

    triage = st.session_state.triage_result

    triage_upper = triage.upper()

    if "RED" in triage_upper:
        st.error(triage)

    elif "YELLOW" in triage_upper:
        st.warning(triage)

    else:
        st.success(triage)

    st.divider()

# =====================================================
# PART 4 — DOCTOR CONSULTATION
# =====================================================

st.header("Step 3: Doctor Consultation")

if st.session_state.patient:

    st.write(
        "Doctor enters consultation details "
        "(for demo purpose)"
    )

    consultation_notes = st.text_area(
        "Doctor Consultation Notes",
        height=150,
        placeholder="""
Example:

Patient has chest pain since last 2 hours.
Sweating present.
Shortness of breath.
History of diabetes.
Cardiac risk suspected.
ECG recommended immediately.
        """
    )

    if st.button("Generate Consultation Summary"):

        patient = st.session_state.patient

        prompt = f"""
        You are a medical assistant helping
        doctors create structured consultation
        summaries.

        Patient Details:

        Name:
        {patient['name']}

        Age:
        {patient['age']}

        Gender:
        {patient['gender']}

        Symptoms:
        {", ".join(patient['symptoms'])}

        Medical History:
        {", ".join(patient['medical_history'])}

        Triage Result:
        {st.session_state.triage_result}

        Doctor Consultation Notes:
        {consultation_notes}

        Create a structured consultation summary
        in EXACT format:

        Symptoms:
        - bullet points

        Medical History:
        - bullet points

        Clinical Observation:
        - short summary

        Preliminary Assessment:
        - short summary

        Recommended Next Step:
        - bullet points

        Important:
        - Do not diagnose
        - Keep concise
        """

        with st.spinner(
            "Generating consultation summary..."
        ):

            result = call_gpt(prompt)

            st.session_state.consultation_summary = result
            st.session_state.step_completed["Doctor Consultation"] = True

# =====================================================
# DISPLAY CONSULTATION SUMMARY
# =====================================================

if st.session_state.consultation_summary:

    st.subheader(
        "🩺 Consultation Summary"
    )

    st.success(
        st.session_state.consultation_summary
    )

    st.divider()

# =====================================================
# PART 5 — ECG ANALYSIS + CARDIOLOGIST ALERT
# =====================================================

st.header("Step 4 & 5: ECG Analysis & Cardiologist Alert")

if st.session_state.consultation_summary:

    st.write(
        "Upload ECG image/report (optional for demo)"
    )

    ecg_file = st.file_uploader(
        "Upload ECG Image",
        type=["png", "jpg", "jpeg"]
    )

    # Demo ECG findings dropdown
    ecg_finding = st.selectbox(
        "Select ECG Finding (Demo)",
        [
            "Normal Sinus Rhythm",
            "ST Elevation (Possible STEMI)",
            "Arrhythmia Detected",
            "Tachycardia",
            "Abnormal ECG"
        ]
    )

    if st.button("Analyze ECG"):

        patient = st.session_state.patient

        prompt = f"""
        You are an AI ECG assistant.

        Patient Details:

        Name:
        {patient['name']}

        Age:
        {patient['age']}

        Symptoms:
        {", ".join(patient['symptoms'])}

        Triage Result:
        {st.session_state.triage_result}

        Consultation Summary:
        {st.session_state.consultation_summary}

        ECG Finding:
        {ecg_finding}

        Provide response in EXACT format:

        ECG Assessment:
        <short explanation>

        Risk Level:
        LOW / MODERATE / HIGH

        Recommended Action:
        - bullet points

        Important:
        - Do NOT diagnose
        - Only provide supportive interpretation
        """

        with st.spinner(
            "Analyzing ECG..."
        ):

            result = call_gpt(prompt)

            st.session_state.ecg_result = result
            st.session_state.step_completed["ECG"] = True
            st.session_state.step_completed["Cardiologist Alert"] = True

# =====================================================
# DISPLAY ECG RESULT
# =====================================================

if st.session_state.ecg_result:

    st.subheader("📈 ECG Analysis Result")

    ecg_result = st.session_state.ecg_result

    ecg_upper = ecg_result.upper()

    if "HIGH" in ecg_upper:
        st.error(ecg_result)

    elif "MODERATE" in ecg_upper:
        st.warning(ecg_result)

    else:
        st.success(ecg_result)

    st.divider()

    # =================================================
    # CARDIOLOGIST ALERT
    # =================================================

    st.subheader("📩 Cardiologist Alert")

    patient = st.session_state.patient

    cardiologist_alert = f"""
🚨 URGENT CARDIOLOGY ALERT

Patient ID:
{patient['patient_id']}

Patient Name:
{patient['name']}

Age:
{patient['age']}

Symptoms:
{", ".join(patient['symptoms'])}

Triage Status:
High Cardiac Risk

ECG Summary:
{st.session_state.ecg_result}

Action:
Immediate cardiology review recommended.
"""

    st.info(cardiologist_alert)

    st.divider()

# =====================================================
# PART 6 — ICU MEDICATION SAFETY CHECK
# =====================================================

st.header("Step 6: ICU Medication Safety")

if st.session_state.ecg_result:

    st.write(
        "Enter medicines prescribed in ICU"
    )

    medications = st.text_area(
        "ICU Medicines",
        height=150,
        placeholder="""
Example:

Aspirin
Heparin
Nitroglycerin
Atorvastatin
Metoprolol
        """
    )

    allergies = st.text_input(
        "Known Allergies (optional)",
        placeholder="Example: Penicillin"
    )

    if st.button("Check Medication Safety"):

        patient = st.session_state.patient

        prompt = f"""
        You are a hospital ICU medication
        safety assistant.

        Patient Details:

        Name:
        {patient['name']}

        Age:
        {patient['age']}

        Medical History:
        {", ".join(patient['medical_history'])}

        Symptoms:
        {", ".join(patient['symptoms'])}

        ECG Summary:
        {st.session_state.ecg_result}

        Allergies:
        {allergies}

        Medicines:
        {medications}

        Analyze medication safety.

        Provide response in EXACT format:

        Medication Review:
        <short summary>

        Safety Status:
        SAFE / CAUTION / HIGH RISK

        Potential Concerns:
        - bullet points

        Recommendation:
        - bullet points

        Important:
        - Do NOT prescribe
        - Only safety review
        - Be medically cautious
        """

        with st.spinner(
            "Checking medication safety..."
        ):

            result = call_gpt(prompt)

            st.session_state.icu_medications = result
            st.session_state.step_completed["ICU"] = True

# =====================================================
# DISPLAY ICU MEDICATION RESULT
# =====================================================

if st.session_state.icu_medications:

    st.subheader(
        "💊 ICU Medication Safety Result"
    )

    icu_result = (
        st.session_state.icu_medications
    )

    icu_upper = icu_result.upper()

    if "HIGH RISK" in icu_upper:
        st.error(icu_result)

    elif "CAUTION" in icu_upper:
        st.warning(icu_result)

    else:
        st.success(icu_result)

    st.divider()

# =====================================================
# PART 7 — DISCHARGE SUMMARY GENERATOR
# =====================================================

st.header("Step 7: AI Discharge Summary")

if st.session_state.icu_medications:

    st.write(
        "Generate discharge summary for patient"
    )

    hospital_stay = st.number_input(
        "Hospital Stay (Days)",
        min_value=1,
        max_value=60,
        value=4
    )

    final_diagnosis = st.text_input(
        "Final Diagnosis",
        value="Acute Cardiac Event"
    )

    discharge_notes = st.text_area(
        "Doctor Discharge Notes",
        height=120,
        placeholder="""
Example:

Patient stabilized after ICU care.
No chest pain currently.
Vitals stable.
Recommend cardiac follow-up.
        """
    )

    if st.button("Generate Discharge Summary"):

        patient = st.session_state.patient

        prompt = f"""
        You are a hospital discharge
        summary assistant.

        Create a professional discharge
        summary.

        Patient Details:

        Name:
        {patient['name']}

        Age:
        {patient['age']}

        Gender:
        {patient['gender']}

        Symptoms:
        {", ".join(patient['symptoms'])}

        Medical History:
        {", ".join(patient['medical_history'])}

        Triage Summary:
        {st.session_state.triage_result}

        Consultation Summary:
        {st.session_state.consultation_summary}

        ECG Summary:
        {st.session_state.ecg_result}

        ICU Medication Review:
        {st.session_state.icu_medications}

        Hospital Stay:
        {hospital_stay} days

        Final Diagnosis:
        {final_diagnosis}

        Doctor Notes:
        {discharge_notes}

        Generate in EXACT format:

        DISCHARGE SUMMARY

        Patient Information:
        - details

        Admission Reason:
        - short summary

        Treatment Provided:
        - bullet points

        Final Diagnosis:
        - diagnosis

        Discharge Medicines:
        - common medication categories only

        Home Care Advice:
        - bullet points

        Follow-Up Recommendation:
        - bullet points

        Keep concise and professional.
        """

        with st.spinner(
            "Generating discharge summary..."
        ):

            result = call_gpt(prompt)

            st.session_state.discharge_summary = result
            st.session_state.step_completed["Discharge"] = True

# =====================================================
# DISPLAY DISCHARGE SUMMARY
# =====================================================

if st.session_state.discharge_summary:

    st.subheader(
        "📄 Discharge Summary"
    )

    st.success(
        st.session_state.discharge_summary
    )

    # Download Option
    st.download_button(
        label="Download Discharge Summary",
        data=st.session_state.discharge_summary,
        file_name="discharge_summary.txt",
        mime="text/plain"
    )

    st.divider()

# =====================================================
# PART 8 — INSURANCE / BILLING SUMMARY
# =====================================================

st.header("Step 8: Insurance / Billing")

if st.session_state.discharge_summary:

    st.write(
        "Generate billing and insurance summary"
    )

    col1, col2 = st.columns(2)

    with col1:

        consultation_charge = st.number_input(
            "Doctor Consultation Charges (₹)",
            min_value=0,
            value=1500
        )

        ecg_charge = st.number_input(
            "ECG Charges (₹)",
            min_value=0,
            value=2500
        )

        icu_charge = st.number_input(
            "ICU Charges (₹)",
            min_value=0,
            value=50000
        )

    with col2:

        medicine_charge = st.number_input(
            "Medicine Charges (₹)",
            min_value=0,
            value=12000
        )

        miscellaneous_charge = st.number_input(
            "Miscellaneous Charges (₹)",
            min_value=0,
            value=5000
        )

        insurance_provider = st.text_input(
            "Insurance Provider",
            value="Star Health Insurance"
        )

    if st.button(
        "Generate Insurance & Billing Summary"
    ):

        patient = st.session_state.patient

        total_bill = (
            consultation_charge
            + ecg_charge
            + icu_charge
            + medicine_charge
            + miscellaneous_charge
        )

        prompt = f"""
        You are a hospital billing and
        insurance assistant.

        Generate a professional
        billing and insurance summary.

        Patient Details:

        Name:
        {patient['name']}

        Patient ID:
        {patient['patient_id']}

        Final Discharge Summary:
        {st.session_state.discharge_summary}

        Billing Details:

        Consultation Charges:
        ₹{consultation_charge}

        ECG Charges:
        ₹{ecg_charge}

        ICU Charges:
        ₹{icu_charge}

        Medicine Charges:
        ₹{medicine_charge}

        Miscellaneous Charges:
        ₹{miscellaneous_charge}

        Total Bill:
        ₹{total_bill}

        Insurance Provider:
        {insurance_provider}

        Generate response in EXACT format:

        INSURANCE CLAIM SUMMARY

        Patient Details:
        - details

        Treatment Summary:
        - short summary

        Billing Breakdown:
        - consultation
        - ECG
        - ICU
        - medicines
        - misc

        Total Amount:
        ₹ amount

        Insurance Status:
        Eligible for claim review

        Required Documents:
        - bullet points

        Keep concise and professional.
        """

        with st.spinner(
            "Generating insurance summary..."
        ):

            result = call_gpt(prompt)

            st.session_state.insurance_summary = result
            st.session_state.step_completed["Insurance"] = True

# =====================================================
# DISPLAY INSURANCE SUMMARY
# =====================================================

if st.session_state.insurance_summary:

    st.subheader(
        "💳 Insurance / Billing Summary"
    )

    st.success(
        st.session_state.insurance_summary
    )

    st.download_button(
        label="Download Billing Summary",
        data=st.session_state.insurance_summary,
        file_name="insurance_summary.txt",
        mime="text/plain"
    )

    st.divider()

# =====================================================
# PART 9 — FOLLOW-UP ASSISTANT
# =====================================================

st.header("Step 9: Follow-Up Assistant")

if st.session_state.insurance_summary:

    st.write(
        "Simulate post-discharge patient follow-up"
    )

    patient_response = st.selectbox(
        "Patient Current Status",
        [
            "Feeling Better",
            "Mild Chest Pain",
            "Severe Chest Pain",
            "Breathing Difficulty",
            "Missed Medication"
        ]
    )

    medication_taken = st.radio(
        "Medicine Taken?",
        ["Yes", "No"]
    )

    followup_day = st.selectbox(
        "Follow-Up Day",
        [
            "Day 1",
            "Day 3",
            "Day 7",
            "Day 15"
        ]
    )

    if st.button(
        "Generate Follow-Up Response"
    ):

        patient = st.session_state.patient

        prompt = f"""
        You are a hospital follow-up assistant.

        Patient Details:

        Name:
        {patient['name']}

        Age:
        {patient['age']}

        Final Discharge Summary:
        {st.session_state.discharge_summary}

        Follow-Up Day:
        {followup_day}

        Patient Status:
        {patient_response}

        Medication Taken:
        {medication_taken}

        Generate response in EXACT format:

        FOLLOW-UP STATUS

        Patient Condition:
        <short summary>

        Risk Level:
        LOW / MODERATE / HIGH

        Recommended Action:
        - bullet points

        Follow-Up Message:
        <short WhatsApp style message>

        Important:
        - Do not diagnose
        - Escalate if symptoms are severe
        - Be medically cautious
        """

        with st.spinner(
            "Generating follow-up..."
        ):

            result = call_gpt(prompt)

            st.session_state.followup_message = result
            st.session_state.step_completed["Follow-Up"] = True

# =====================================================
# DISPLAY FOLLOW-UP RESULT
# =====================================================

if st.session_state.followup_message:

    st.subheader(
        "📲 Follow-Up Result"
    )

    followup = (
        st.session_state.followup_message
    )

    followup_upper = followup.upper()

    if "HIGH" in followup_upper:
        st.error(followup)

    elif "MODERATE" in followup_upper:
        st.warning(followup)

    else:
        st.success(followup)

    st.divider()

    # =================================================
    # HOSPITAL AI WORKFLOW COMPLETE
    # =================================================

    st.balloons()

    st.success(
        "✅ Cardiac Emergency Workflow Completed Successfully!"
    )

    st.markdown(
        """
        ### End-to-End AI Workflow Completed

        ✔ Casualty Registration  
        ✔ Smart Emergency Triage  
        ✔ Doctor Consultation  
        ✔ ECG Analysis  
        ✔ Cardiologist Alert  
        ✔ ICU Medication Safety  
        ✔ Discharge Summary  
        ✔ Insurance/Billing  
        ✔ Follow-Up Assistant
        """
    )
