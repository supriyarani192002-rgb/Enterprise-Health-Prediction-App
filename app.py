import streamlit as st
import pandas as pd
from datetime import datetime
import database
import ai_service
import re
import base64

# Initialize DB
database.init_db()

st.set_page_config(page_title="Health Prediction App", layout="wide")

def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as image_file_data:
            encoded_string = base64.b64encode(image_file_data.read())
        
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string.decode()}) !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
        .stForm {{ 
            background-color: rgba(25, 25, 30, 0.85) !important; 
            border-radius: 12px; 
            border: 1px solid rgba(255, 255, 255, 0.15); 
            padding: 25px; 
        }}
        
        /* 👇 NAYA CSS: Tabs ko Black Buttons banane ke liye 👇 */
        button[data-baseweb="tab"] {{
            background-color: black !important;
            color: white !important;
            border-radius: 8px !important;
            border: 1px solid #555 !important;
            padding: 8px 16px !important;
            margin-right: 15px !important;
        }}
        
        /* Jo tab active (selected) hoga, uspe white border aur thoda glow aayega */
        button[data-baseweb="tab"][aria-selected="true"] {{
            background-color: #1a1a1a !important; 
            border: 1px solid white !important;
            box-shadow: 0px 0px 8px rgba(255, 255, 255, 0.3) !important;
        }}
        
        /* Tab ke neeche ki default line ko gayab karne ke liye */
        div[data-baseweb="tab-list"] {{
            border-bottom: none !important;
        }}
        /* 👆 NAYA CSS YAHAN KHATAM 👆 */
        
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image file not found. Make sure 'bg_image.png' is in the exact same folder as app.py.")

def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as image_file_data:
            encoded_string = base64.b64encode(image_file_data.read())
        
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string.decode()}) !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
        .stForm {{ 
            background-color: rgba(25, 25, 30, 0.85) !important; 
            border-radius: 12px; 
            border: 1px solid rgba(255, 255, 255, 0.15); 
            padding: 25px; 
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image file not found. Make sure 'bg_image.png' is in the exact same folder as app.py.")

# Function call to load background image
add_bg_from_local('bg_image.png') 

# Centered Title
st.markdown("<h1 style='text-align: center;'>🏥 Enterprise Health Prediction Application</h1>", unsafe_allow_html=True)

st.subheader("1. Add New Patient")
with st.form("patient_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth", value=datetime.today(), min_value=datetime(1900, 1, 1).date(), max_value=datetime.today())
        email = st.text_input("Email Address")
        
    with col2:
        glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, format="%.1f")
        haemoglobin = st.number_input("Haemoglobin (g/dL)", min_value=0.0, format="%.1f")
        cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, format="%.1f")
        
    submit_button = st.form_submit_button("Generate Prediction & Save")

    if submit_button:
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        # DYNAMIC DUPLICATE CHECK LOGIC 
        existing_patients = database.get_all_patients()
        is_duplicate = False
        
        if existing_patients:
            for p in existing_patients:
                db_name = p[1].strip().lower()
                db_dob = str(p[2]).strip()
                db_email = p[3].strip().lower()
                
                # Check if Name, Email and DOB is same  OR  Name and Email matches (DOB can be different but if Name and Email matches, it's likely a duplicate)
                if (db_name == full_name.strip().lower() and db_email == email.strip().lower() and db_dob == str(dob).strip()) or \
                   (db_name == full_name.strip().lower() or db_email == email.strip().lower()):
                    is_duplicate = True
                    break

        if not full_name or not email:
            st.error("Please fill in the Name and Email.")
        elif not re.match(email_pattern, email):
            st.error("Please enter a valid email address.")
        elif dob >= datetime.today().date():
            st.error("Date of Birth cannot be today's date. Please select a valid past date.")
        elif is_duplicate:
            # Duplicate validation response
            st.error("❌ Duplicate record found! A patient with this Name and Email already exists in the system.")
        elif glucose == 0 or haemoglobin == 0 or cholesterol == 0:
            st.error("Blood test values cannot be zero.")
        else:
            with st.spinner("Analyzing vitals securely via AI API..."):
                ai_remark = ai_service.get_health_prediction(glucose, haemoglobin, cholesterol)
            
            database.add_patient(full_name, str(dob), email, glucose, haemoglobin, cholesterol, ai_remark)
            st.success(f"Record saved successfully! AI Prediction: {ai_remark}")
            st.rerun()

st.divider()

st.subheader("2. Patient Records Database")
patients = database.get_all_patients()

if patients:
    df = pd.DataFrame(patients, columns=["ID", "Name", "DOB", "Email", "Glucose", "Haemoglobin", "Cholesterol", "Remarks"])
    
    st.dataframe(df, width='stretch', hide_index=True)
    
    
    # For update and delete operations, we will use the patient ID as a reference
    st.write("### ⚙️ Manage Records (Update & Delete)")
    tab_update, tab_delete = st.tabs(["**✏️ Update Record**", "**🗑️ Delete Record**"])
    
    # --- UPDATE TAB ---
    with tab_update:
        update_id = st.number_input("Enter Patient ID to Update", min_value=1, step=1, key="upd_id")
        
        # Find existing patient data based on ID
        target_patient = next((p for p in patients if p[0] == update_id), None)
        
        if target_patient:
            st.success(f"Editing Record for: **{target_patient[1]}**")
            with st.form("update_form"):
                u_col1, u_col2 = st.columns(2)
                with u_col1:
                    new_name = st.text_input("Full Name", value=target_patient[1])
                    
                    # Safe Date Parsing
                    try:
                        parsed_date = datetime.strptime(str(target_patient[2]), "%Y-%m-%d").date()
                    except:
                        parsed_date = datetime.today().date()
                        
                    new_dob = st.date_input("Date of Birth", value=parsed_date, max_value=datetime.today())
                    new_email = st.text_input("Email Address", value=target_patient[3])
                    
                with u_col2:
                    new_glucose = st.number_input("Glucose (mg/dL)", value=float(target_patient[4]), format="%.1f")
                    new_haemo = st.number_input("Haemoglobin (g/dL)", value=float(target_patient[5]), format="%.1f")
                    new_chol = st.number_input("Cholesterol (mg/dL)", value=float(target_patient[6]), format="%.1f")
                    
                if st.form_submit_button("Update Record & Refresh AI Prediction"):
                    with st.spinner("Re-analyzing new vitals via AI API..."):
                        # Naye vitals par dobara AI prediction mangwana
                        new_ai_remark = ai_service.get_health_prediction(new_glucose, new_haemo, new_chol)
                    
                    # Database mein naya data save karna
                    database.update_patient(update_id, new_name, str(new_dob), new_email, new_glucose, new_haemo, new_chol, new_ai_remark)
                    st.success("Record updated successfully!")
                    st.rerun()
        else:
            st.info("Enter a valid ID above to load and edit patient data.")
            
    # --- DELETE TAB ---
    with tab_delete:
        delete_id = st.number_input("Enter ID to Delete", min_value=1, step=1, key="del_id")
        if st.button("Delete Record", type="primary"):
            # Check if ID exists before deleting
            if any(p[0] == delete_id for p in patients):
                database.delete_patient(delete_id)
                st.warning(f"Record ID {delete_id} has been permanently deleted.")
                st.rerun()
            else:
                st.error("ID not found in database.")
    # -----------------------------------------------------------------
else:
    st.info("No patient records found in the database. Add a patient above.")