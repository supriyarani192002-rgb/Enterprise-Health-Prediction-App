import json
import requests


API_KEY = "AQ.Ab8RN6KGl15uaBWLAc7UApR8IDbOmreve9O10ske5LPUJDouPA" # Replace with your actual Gemini API key

def get_health_prediction(glucose, haemoglobin, cholesterol):
    prompt = f"""
    You are a medical analysis AI. Based purely on these standard blood test metrics:
    - Glucose: {glucose} mg/dL
    - Haemoglobin: {haemoglobin} g/dL
    - Cholesterol: {cholesterol} mg/dL
    
    Provide a single, short sentence predicting a possible health condition or disease risk. 
    Keep it under 15 words. Be direct.
    """
    
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        # Direct HTTP POST request sending to stable endpoint
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()
        
        # Checking stable API response structure
        if "candidates" in result:
            ai_remark = result["candidates"][0]["content"]["parts"][0]["text"]
            return ai_remark.strip()
        else:
            print(f"API Error Response: {result}")
            return "System Warning: Unexpected API response."
            
    except Exception as e:
        print(f"Error calling Direct REST API: {e}")
        return "System Warning: Unable to connect."