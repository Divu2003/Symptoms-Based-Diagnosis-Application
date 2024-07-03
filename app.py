import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import pyttsx3

# Ensure PyArrow is installed
try:
    import pyarrow
except ImportError:
    st.error("PyArrow is not installed. Please install it by running `pip install pyarrow`.")

# Initialize text-to-speech engine
engine = None

def initialize_engine():
    global engine
    if not engine:
        engine = pyttsx3.init()

def speak_recommendations(recommendations):
    initialize_engine()
    for rec in recommendations:
        engine.say(rec)
    engine.runAndWait()

def highlight_symptoms(symptoms, confidence_scores):
    highlighted_symptoms = []
    for symptom, score in zip(symptoms, confidence_scores):
        if score > 0.5:
            highlighted_symptoms.append(f"<span style='color: red; font-weight: bold;'>{symptom} (Confidence: {score:.2f})</span>")
        else:
            highlighted_symptoms.append(f"{symptom} (Confidence: {score:.2f})")
    return highlighted_symptoms

# Loading the saved models
def load_models():
    with open(r'F:\G7\Final Code\multiple disease prediction streamlit\saved models\diabetes_model.sav', 'rb') as file:
        diabetes_model = pickle.load(file)

    with open(r'F:\G7\Final Code\multiple disease prediction streamlit\saved models\heart_disease_model.sav', 'rb') as file:
         heart_disease_model = pickle.load(file)

    with open(r'multiple disease prediction streamlit/saved models/parkinsons_model.sav', 'rb') as file:
        parkinsons_model = pickle.load(file)

    return diabetes_model, heart_disease_model, parkinsons_model

diabetes_model, heart_disease_model, parkinsons_model = load_models()

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        'Types of Diseases',
        ['Diabetes Prediction', 'Heart Disease Prediction', "Parkinson's Prediction"],
        icons=['activity', 'heart', 'person'],
        default_index=0
    )

st.title("Symptoms Based Diagnosis Application")

def display_recommendations(diagnosis, recommendations):
    if diagnosis:
        st.subheader("Recommendations")
        st.markdown(f"<div style='padding: 1rem; border: 1px solid #ccc; border-radius: 5px; background-color: #f9f9f9;'><b>{diagnosis}</b></div>", unsafe_allow_html=True)
        for rec in recommendations:
            st.markdown(f"<div style='padding: 0.5rem; border: 1px solid #ccc; border-radius: 5px; background-color: #fff; margin-top: 0.5rem;'>{rec}</div>", unsafe_allow_html=True)
        speak_recommendations(recommendations)

def diabetes_prediction_page():
    st.subheader('Diabetes Prediction')
    gender = st.selectbox('Gender', options=['Female', 'Male'])
    
    col1, col2, col3 = st.columns(3)
    if gender == 'Female':
        with col1:
            Pregnancies = st.number_input('Number of Pregnancies', min_value=0, max_value=20, value=0)
    with col2:
        Glucose = st.number_input('Glucose Level', min_value=0, max_value=200, value=0)
    with col3:
        BloodPressure = st.number_input('Blood Pressure value', min_value=0, max_value=150, value=0)
    with col1:
        SkinThickness = st.number_input('Skin Thickness value', min_value=0, max_value=100, value=0)
    with col2:
        Insulin = st.number_input('Insulin Level', min_value=0, max_value=900, value=0)
    with col3:
        BMI = st.number_input('BMI value', min_value=0.0, max_value=100.0, value=0.0)
    with col1:
        DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function value', min_value=0.0, max_value=2.5, value=0.0)
    with col2:
        Age = st.number_input('Age of the Person', min_value=0, max_value=120, value=0)

    input_data = [[Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]
    symptoms = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    if gender == 'Female':
        input_data[0].insert(0, Pregnancies)
        symptoms.insert(0, 'Pregnancies')

    if st.button('Diabetes Test Result'):
        try:
            diab_prediction = diabetes_model.predict(input_data)
            diab_confidence = diabetes_model.predict_proba(input_data)[0]
            diab_confidence_score = diab_confidence[1]

            highlighted_symptoms = highlight_symptoms(symptoms, diab_confidence)
            if diab_prediction[0] == 1:
                diagnosis = f'The person is diabetic (Confidence: {diab_confidence_score:.2f})'
                recommendations = [
                    "Maintain a balanced diet rich in vegetables, fruits, and lean proteins.",
                    "Exercise regularly to maintain a healthy weight and lower blood sugar levels.",
                    "Monitor blood sugar levels regularly.",
                    "Take prescribed medications as directed by your healthcare provider.",
                    "Stay hydrated and manage stress effectively."
                ]
            else:
                diagnosis = f'The person is not diabetic (Confidence: {1 - diab_confidence_score:.2f})'
                recommendations = ["You are fit. Continue with your healthy lifestyle."]
            st.success(diagnosis)
            display_recommendations(diagnosis, recommendations)
            st.markdown("### Symptom Analysis")
            for symptom in highlighted_symptoms:
                st.markdown(symptom, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")

def heart_disease_prediction_page():
    st.subheader('Heart Disease Prediction')
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input('Age', min_value=0, max_value=120, value=0)
    with col2:
        sex = st.selectbox('Sex', options=['Male', 'Female'])
    with col3:
        cp = st.number_input('Chest Pain types', min_value=0, max_value=3, value=0)
    with col1:
        trestbps = st.number_input('Resting Blood Pressure', min_value=0, max_value=200, value=0)
    with col2:
        chol = st.number_input('Serum Cholestoral in mg/dl', min_value=0, max_value=600, value=0)
    with col3:
        fbs = st.number_input('Fasting Blood Sugar > 120 mg/dl', min_value=0, max_value=1, value=0)
    with col1:
        restecg = st.number_input('Resting Electrocardiographic results', min_value=0, max_value=2, value=0)
    with col2:
        thalach = st.number_input('Maximum Heart Rate achieved', min_value=0, max_value=220, value=0)
    with col3:
        exang = st.number_input('Exercise Induced Angina', min_value=0, max_value=1, value=0)
    with col1:
        oldpeak = st.number_input('ST depression induced by exercise', min_value=0.0, max_value=6.0, value=0.0)
    with col2:
        slope = st.number_input('Slope of the peak exercise ST segment', min_value=0, max_value=2, value=0)
    with col3:
        ca = st.number_input('Major vessels colored by flourosopy', min_value=0, max_value=3, value=0)
    with col1:
        thal = st.number_input('Thal: 0 = normal; 1 = fixed defect; 2 = reversable defect', min_value=0, max_value=2, value=0)

    input_data = [[age, 1 if sex == 'Male' else 0, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
    symptoms = ['Age', 'Sex', 'Chest Pain types', 'Resting Blood Pressure', 'Serum Cholestoral', 'Fasting Blood Sugar', 'Resting Electrocardiographic results', 'Maximum Heart Rate achieved', 'Exercise Induced Angina', 'ST depression induced by exercise', 'Slope of the peak exercise ST segment', 'Major vessels colored by flourosopy', 'Thal']

    if st.button('Heart Disease Test Result'):
        try:
            heart_prediction = heart_disease_model.predict(input_data)
            heart_confidence = heart_disease_model.predict_proba(input_data)[0]
            heart_confidence_score = heart_confidence[1]

            highlighted_symptoms = highlight_symptoms(symptoms, heart_confidence)
            if heart_prediction[0] == 1:
                diagnosis = f'The person has heart disease (Confidence: {heart_confidence_score:.2f})'
                recommendations = [
                    "Adopt a heart-healthy diet low in saturated fats, trans fats, and cholesterol.",
                    "Engage in regular physical activity to strengthen the heart.",
                    "Monitor blood pressure and cholesterol levels regularly.",
                    "Avoid smoking and limit alcohol consumption.",
                    "Manage stress through relaxation techniques like yoga and meditation."
                ]
            else:
                diagnosis = f'The person does not have heart disease (Confidence: {1 - heart_confidence_score:.2f})'
                recommendations = ["Maintain a healthy lifestyle to keep your heart healthy."]
            st.success(diagnosis)
            display_recommendations(diagnosis, recommendations)
            st.markdown("### Symptom Analysis")
            for symptom in highlighted_symptoms:
                st.markdown(symptom, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")

def parkinsons_prediction_page():
    st.subheader("Parkinson's Disease Prediction")
    col1, col2, col3 = st.columns(3)
    with col1:
        fo = st.number_input('MDVP:Fo(Hz)', min_value=0.0, max_value=500.0, value=0.0)
    with col2:
        fhi = st.number_input('MDVP:Fhi(Hz)', min_value=0.0, max_value=500.0, value=0.0)
    with col3:
        flo = st.number_input('MDVP:Flo(Hz)', min_value=0.0, max_value=500.0, value=0.0)
    with col1:
        Jitter_percent = st.number_input('MDVP:Jitter(%)', min_value=0.0, max_value=1.0, value=0.0)
    with col2:
        Jitter_Abs = st.number_input('MDVP:Jitter(Abs)', min_value=0.0, max_value=0.1, value=0.0)
    with col3:
        RAP = st.number_input('MDVP:RAP', min_value=0.0, max_value=1.0, value=0.0)
    with col1:
        PPQ = st.number_input('MDVP:PPQ', min_value=0.0, max_value=1.0, value=0.0)
    with col2:
        DDP = st.number_input('Jitter:DDP', min_value=0.0, max_value=1.0, value=0.0)
    with col3:
        Shimmer = st.number_input('MDVP:Shimmer', min_value=0.0, max_value=1.0, value=0.0)
    with col1:
        Shimmer_dB = st.number_input('MDVP:Shimmer(dB)', min_value=0.0, max_value=10.0, value=0.0)
    with col2:
        APQ3 = st.number_input('Shimmer:APQ3', min_value=0.0, max_value=1.0, value=0.0)
    with col3:
        APQ5 = st.number_input('Shimmer:APQ5', min_value=0.0, max_value=1.0, value=0.0)
    with col1:
        APQ = st.number_input('MDVP:APQ', min_value=0.0, max_value=1.0, value=0.0)
    with col2:
        DDA = st.number_input('Shimmer:DDA', min_value=0.0, max_value=1.0, value=0.0)
    with col3:
        NHR = st.number_input('NHR', min_value=0.0, max_value=1.0, value=0.0)
    with col1:
        HNR = st.number_input('HNR', min_value=0.0, max_value=100.0, value=0.0)
    with col2:
        RPDE = st.number_input('RPDE', min_value=0.0, max_value=1.0, value=0.0)
    with col3:
        DFA = st.number_input('DFA', min_value=0.0, max_value=2.0, value=0.0)
    with col1:
        spread1 = st.number_input('spread1', min_value=-10.0, max_value=0.0, value=0.0)
    with col2:
        spread2 = st.number_input('spread2', min_value=0.0, max_value=1.0, value=0.0)
    with col3:
        D2 = st.number_input('D2', min_value=0.0, max_value=10.0, value=0.0)
    with col1:
        PPE = st.number_input('PPE', min_value=0.0, max_value=1.0, value=0.0)

    input_data = [[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]]
    symptoms = ['MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE']

    if st.button("Parkinson's Test Result"):
        try:
            parkinsons_prediction = parkinsons_model.predict(input_data)
            parkinsons_confidence = parkinsons_model.predict_proba(input_data)[0]
            parkinsons_confidence_score = parkinsons_confidence[1]

            highlighted_symptoms = highlight_symptoms(symptoms, parkinsons_confidence)
            if parkinsons_prediction[0] == 1:
                diagnosis = f'The person has Parkinson\'s disease (Confidence: {parkinsons_confidence_score:.2f})'
                recommendations = [
                    "Consult a neurologist for a detailed diagnosis and treatment plan.",
                    "Engage in regular physical activity to maintain muscle strength and flexibility.",
                    "Consider speech therapy to improve communication skills.",
                    "Adopt a balanced diet rich in fruits, vegetables, and whole grains.",
                    "Stay socially active and seek support from family and friends."
                ]
            else:
                diagnosis = f'The person does not have Parkinson\'s disease (Confidence: {1 - parkinsons_confidence_score:.2f})'
                recommendations = ["No signs of Parkinson's disease. Maintain a healthy lifestyle."]
            st.success(diagnosis)
            display_recommendations(diagnosis, recommendations)
            st.markdown("### Symptom Analysis")
            for symptom in highlighted_symptoms:
                st.markdown(symptom, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")

# Navigation
if selected == 'Diabetes Prediction':
    diabetes_prediction_page()
elif selected == 'Heart Disease Prediction':
    heart_disease_prediction_page()
elif selected == "Parkinson's Prediction":
    parkinsons_prediction_page()


# def set_bg_from_url(url, opacity=1):
    
#     footer = """
#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
#     <footer>
#         <div style='visibility: visible;margin-top:7rem;justify-content:center;display:flex;'>
#             <p style="font-size:1.1rem;">
#                 &nbsp;
#     </footer>
# """
#     st.markdown(footer, unsafe_allow_html=True)
    
    
#     # Set background image using HTML and CSS
#     st.markdown(
#         f"""
#         <style>
#             body {{
#                 background: url('{url}') no-repeat center center fixed;
#                 background-size: cover;
#                 opacity: {opacity};
#             }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # Set background image from URL
# set_bg_from_url("https://images.everydayhealth.com/homepage/health-topics-2.jpg?w=768", opacity=0.875)
            

