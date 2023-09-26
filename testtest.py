import requests

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": {
		"past_user_inputs": ["Act as a guard robot protecting a restricted area. Your name is Hubert."],
		"generated_responses": ["Alright, I'm Hubert the guard robot."],
		"text": "hello"
	},
})

print(output['generated_text'])