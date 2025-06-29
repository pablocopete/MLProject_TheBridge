import streamlit as st
from utils.prepare_data import create_dummy_data, load_user_data
from utils.models import load_model, make_prediction
from utils.gemini_api_call import get_strategy, get_email
from utils.logo_header import logo_header
import base64
from pathlib import Path

# Data columns
# age,joined_through_referral,days_since_last_login,avg_time_spent,avg_transaction_value,avg_frequency_login_days,
# points_in_wallet,used_special_discount,offer_application_preference,past_complaint,is_missing_avg_frequency_login_days,
# diff_avg_login_freq_last_login_days,days_since_joining,is_male,region_City,region_Missing,region_Town,
# region_Village,complaint_status_No Information Available,complaint_status_Not Applicable,
# complaint_status_Solved,complaint_status_Solved in Follow-up,complaint_status_Unsolved,
# feedback_No reason specified,feedback_Poor Customer Service,feedback_Poor Product Quality,
# feedback_Poor Website,feedback_Products always in Stock,feedback_Quality Customer Care,
# feedback_Reasonable Price,feedback_Too many ads,feedback_User Friendly Website,
# feedback_categroy_Negative,feedback_categroy_Neutral,feedback_categroy_Positive,
# membership_category_Basic Membership,membership_category_Gold Membership,
# membership_category_No Membership,membership_category_Platinum Membership,
# membership_category_Premium Membership,membership_category_Silver Membership

# Let´s see which categories are needed
# There are too many categories. We have seen with the feature importance analysis, which are the main categories for the prediction.
# We will let the user choose the main ones and the other will have a default value

# Features to define by user: name, age, points in wallet, feedback, average transaction value

model = load_model()
image_path = Path("app/static/resources/logo_dark.png")
st.set_page_config(layout='wide', page_title='Electro Verse - Customer churn risk', page_icon=str(image_path))

# Customized header ------------------------------------
import base64
from pathlib import Path

# Check if the image file exists
if not image_path.exists():
    st.error(f"Image not found at: {image_path}")
else:
    # Function to get base64 encoded image
    @st.cache_data # Cache the image data to avoid re-reading on every rerun
    def get_base64_image(img_path):
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Get the base64 string for your logo
    logo_base64 = get_base64_image(image_path)

    # Construct the data URL
    # Replace 'png' with 'jpeg' or 'gif' if your image is a different type
    data_url = f"data:image/png;base64,{logo_base64}"

    custom_header_html = f"""
    <style>
        .header-container {{
            display: flex;
            align-items: center;
            background-color: black;
            padding: 10px 20px;
            color: white; /* Default text color for the header */
            margin-bottom: 20px; /* Add some space below the header */
        }}
        .header-logo {{
            height: 60px; /* Adjust as needed */
            margin-right: 20px;
        }}
        .header-title {{
            font-size: 2.5em; /* Adjust font size as needed */
            font-weight: bold;
            display: flex;
            gap: 5px; /* Space between words */
        }}
        .header-title .electro {{
            color: white; /* "ELECTRO" in white */
        }}
        .header-title .verse {{
            color: #00A6D6; /* "VERSE" in the blue/cyan color */
        }}
    </style>
    <div class="header-container">
        <img src="{data_url}" class="header-logo">
        <div class="header-title">
            <span class="electro">ELECTRO</span><span class="verse">VERSE</span>
        </div>
    </div>
    """

    st.html(custom_header_html)
# -----------------------------------------------

st.title = "Customer churn risk"
is_valid=False

col1, col2 = st.columns((1,2))
with col1:
    st.subheader("Customer data: ")
    with st.form("Customer info: "): 

        name = st.text_input("Name")

        age = st.number_input(
            "Age", value=None, placeholder="Type a number...",
            min_value=0, max_value=100
        )

        membership = st.selectbox(
            "Membership",
            ("No Membership", "Basic Membership",  "Premium Membership", "Silver Membership", "Gold Membership",  "Platinum Membership"))

        feedback = st.selectbox(
            "Feedback",
            ("No reason specified", "Poor Product Quality", "Too many ads", "Poor Website", "Poor Customer Service", 
            "Reasonable Price", "User Friendly Website", "Products always in Stock", "Quality Customer Care")
        )


        points_in_wallet = st.number_input(
            "Points in wallet", value=None, placeholder="Type a number...",
            min_value=0, max_value=3000
        )


        avg_transaction_value = st.number_input(
            "Average transaction value", value=None, placeholder="Type a number...",
            min_value=0, max_value=100000
        )

        submitted = st.form_submit_button("Submit")


        # Check if all the fields were filled
        if submitted:
            is_valid = True
            if not name.strip(): 
                st.error("Please enter Name.")
                is_valid = False
            if age is None:
                st.error("Please enter Age.")
                is_valid = False
            if membership is None:
                st.error("Please enter Membership.")
                is_valid = False
            if points_in_wallet is None:
                st.error("Please enter Points in wallet.")
                is_valid = False
            if avg_transaction_value is None:
                st.error("Please enter Average transaction value.")
                is_valid = False

            # If all fields are valid, process the submission
            if is_valid == True:
                st.subheader("Submitted Information:")
                st.write(f"**Name:** {name}")
                st.write(f"**Age:** {age}") 
                st.write(f"**Feedback:** {feedback}")
                st.write(f"**Points in wallet:** {points_in_wallet}")
                st.write(f"**Average transaction value:** {avg_transaction_value}")

                st.success("Form submitted successfully!")
            else:
                st.warning("Please fill in all required fields to submit the form.")


with col2:
    if is_valid==True:
        # Pass data to model
        data = create_dummy_data()
        data = load_user_data(data, membership, feedback, age, avg_transaction_value, points_in_wallet)

        # Make prediction and show it
        prediction = make_prediction(model, data)
        st.subheader("Churn risk assessment")
        with st.container(border=True):
            if prediction == "High risk":
                st.error("❗ High churn risk detected! Immediate action recommended.")
            elif prediction == "Moderate_risk":
                st.warning("⚠️ Medium churn risk. Monitor closely and consider engagement.")
            else:
                st.success("✅ Low churn risk. Customer appears engaged.")

        # Decide strategy to follow
        strategy = get_strategy(prediction, membership, feedback, age, avg_transaction_value, points_in_wallet)
        st.subheader("Recommended retention strategy")
        with st.container(border=True):
            st.info(strategy)

        # Write a email we may send to the customer
        email = get_email(strategy, prediction, name,  membership, feedback, age, avg_transaction_value, points_in_wallet)
        st.subheader("Proposed email")
        with st.container(border=True):
            st.info(email)