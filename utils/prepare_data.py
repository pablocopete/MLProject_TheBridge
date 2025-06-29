import pandas as pd
import pickle

def create_dummy_data():
    age = 18
    transaction = 10
    points = 10

    df_input = pd.DataFrame({
        'age': [age],
        'joined_through_referral': [0],
        'days_since_last_login': [12],
        'avg_time_spent': [161.765],
        'avg_transaction_value': [transaction],
        'avg_frequency_login_days': [17],
        'points_in_wallet': [points],
        'used_special_discount': [0],
        'offer_application_preference': [0],
        'past_complaint': [0],
        'is_missing_avg_frequency_login_days': [0],
        'diff_avg_login_freq_last_login_days': [5],
        'days_since_joining': [544],
        'is_male': [1],
        'region_City': [0],
        'region_Missing': [0],
        'region_Town': [1],
        'region_Village': [0],
        'complaint_status_No Information Available': [0],
        'complaint_status_Not Applicable': [1],
        'complaint_status_Solved': [0],
        'complaint_status_Solved in Follow-up': [0],
        'complaint_status_Unsolved': [0],
        'feedback_No reason specified': [0],
        'feedback_Poor Customer Service': [0],
        'feedback_Poor Product Quality': [0],
        'feedback_Poor Website': [0],
        'feedback_Products always in Stock': [0],
        'feedback_Quality Customer Care': [0],
        'feedback_Reasonable Price': [0], 
        'feedback_Too many ads': [0],
        'feedback_User Friendly Website': [0], 
        'feedback_categroy_Negative': [0],
        'feedback_categroy_Neutral': [0],
        'feedback_categroy_Positive': [0],
        'membership_category_Basic Membership': [0],
        'membership_category_Gold Membership': [0],
        'membership_category_No Membership': [0],
        'membership_category_Platinum Membership': [0],
        'membership_category_Premium Membership': [0],
        'membership_category_Silver Membership': [0]
    })
    return df_input

def load_user_data(df_input, membership, feedback, age, avg_transaction_value, points_in_wallet):

    df_input['age'] = age
    df_input['avg_transaction_value'] = avg_transaction_value
    df_input['points_in_wallet'] = points_in_wallet

    # Set to 1 the membership and feedback category columns 
    df_input.loc[0, "membership_category_" + membership] = 1
    df_input.loc[0, "feedback_" + feedback] = 1

    positive_feedback_list = ['Products always in Stock', 'Quality Customer Care', 'Reasonable Price', 'User Friendly Website']
    negative_feedback_list = ['Poor Customer Service', 'Poor Product Quality', 'Too many ads', 'Poor Website']
    neutral_feedback_list = ['No reason specified']

    if feedback in positive_feedback_list:
        df_input.loc[0, 'feedback_categroy_Positive'] = 1
    elif feedback in negative_feedback_list:
        df_input.loc[0, 'feedback_categroy_Negative'] = 1
    else:
        df_input.loc[0, 'feedback_categroy_Neutral'] = 1
        

    # Normalise using the same scaler used in training
    with open('data/column_transformer/column_transformer.pkl', 'rb') as file:
        my_column_transformer = pickle.load(file)
    
    numerical_columns = ['age', 'days_since_last_login', 'avg_time_spent', 'avg_transaction_value', 'avg_frequency_login_days', 
                     'points_in_wallet', 'diff_avg_login_freq_last_login_days', 'days_since_joining']
    
    df_input[numerical_columns] = my_column_transformer.transform(df_input)

    return df_input