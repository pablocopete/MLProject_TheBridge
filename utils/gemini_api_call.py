from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

def get_strategy(prediction, membership, feedback, age, avg_transaction_value, points_in_wallet):

    load_dotenv('.env')
    context_prompt = f""" START OF CONTEXT
    You are an AI assistant specializing in customer retention and marketing. Your task is to generate highly personalized and actionable strategies to prevent customer churn, leveraging provided customer data and their predicted churn risk.

    Given the following customer information and their predicted churn risk category, propose specific, tailored actions for retention. Focus on practical, implementable strategies that address the customer's unique profile and potential pain points. Consider the customer's demographics, membership details, website activity (duration, frequency), reported grievances, and feedback.
    We know the most important factors for customer retention are the membership type (the more basic the membership, the higher the churn rate), the amount of points they have in their wallet and the kind of feedback they leave

    Membership options: ['No Membership', 'Basic Membership', 'Premium Membership', 'Silver Membership', ' Gold Membership', 'Platinum Membership']
    Feedback options: ['No reason specified','Poor Customer Service','Poor Product Quality','Poor Website','Products always in Stock','Quality Customer Care','Reasonable Price', 'Too many ads', 'User Friendly Website']

    User information:[
    age: {age},
    membership: {membership},
    feedback: {feedback},
    avg_transaction_value: {avg_transaction_value},
    points_in_wallet: {points_in_wallet},
    churn_risk: {prediction}]

    **Output Format:**
    Provide brief paragraph with the proposed strategy

    END OF CONTEXT"""

    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=context_prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=100),
            max_output_tokens=500,
        ),
    )

    return response.text

def get_email(strategy, prediction, name, membership, feedback, age, avg_transaction_value, points_in_wallet):

    load_dotenv('.env')
    context_prompt = f""" START OF CONTEXT
    You are an AI assistant specializing in customer retention and marketing. Your task is to generate highly personalized and actionable emails to prevent customer churn, leveraging provided customer data and their predicted churn risk.

    Given the following customer information and the strategy to follow. Redact a personalaised brief email, implementing the strategy.
    We know the most important factors for customer retention are the membership type (the more basic the membership, the higher the churn rate), the amount of points they have in their wallet and the kind of feedback they leave

    Membership options: ['No Membership', 'Basic Membership', 'Premium Membership', 'Silver Membership', ' Gold Membership', 'Platinum Membership']
    Feedback options: ['No reason specified','Poor Customer Service','Poor Product Quality','Poor Website','Products always in Stock','Quality Customer Care','Reasonable Price', 'Too many ads', 'User Friendly Website']

    User information:[
    name: {name}
    age: {age},
    membership: {membership},
    feedback: {feedback},
    avg_transaction_value: {avg_transaction_value},
    points_in_wallet: {points_in_wallet},
    churn_risk: {prediction}]

    strategy: {strategy}
    company_name: Electro Verse

    **Output Format:**
    Provide brief paragraph with the email

    END OF CONTEXT"""

    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=context_prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=100),
            max_output_tokens=500,
        ),
    )

    return response.text

