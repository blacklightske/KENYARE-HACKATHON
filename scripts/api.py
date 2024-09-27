import requests

def process_claim(claim_data):
    # Simulate processing a claim
    print(f"Processing claim: {claim_data}")

def test_api():
    # Test the API by sending a request
    try:
        response = requests.get(QD7AAgHNR7ad6dhg2z1JKl5k_sqakyjkPc_43gKOnjD4T)  # Replace with your actual API endpoint
        if response.status_code == 200:
            print("API is working.")
            return True
        else:
            print(f"API returned an error: {response.status_code}")
            return False
    except Exception as e:
        print(f"API test failed: {str(e)}")
        return False
