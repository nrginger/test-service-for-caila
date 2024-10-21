import re
import requests
from mlp_sdk.abstract import Task
from mlp_sdk.hosting.host import host_mlp_cloud
from mlp_sdk.transport.MlpServiceSDK import MlpServiceSDK
from pydantic import BaseModel
from typing import List

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    person_names: List[str]

def preprocess_text(text):
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    text = ' '.join(lines)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_person_names_from_results(results):
    person_names = []
    for entity in results:
        if entity['entity_group'] == 'PER':
            person_names.append(entity['word'])
    return person_names

class PersonNameExtractor(Task):
    API_URL = "https://api-inference.huggingface.co/models/flair/ner-english-fast"
    API_TOKEN = '_______'  #add your API token
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def __init__(self, config: BaseModel = None, service_sdk: MlpServiceSDK = None) -> None:
        super().__init__(config, service_sdk)

    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def predict(self, data: PredictRequest, config: BaseModel = None) -> PredictResponse:
        if len(data.text) > 1000:
            return PredictResponse(person_names=["Error: Text exceeds maximum length of 1000 characters."])
        
        preprocessed_text = preprocess_text(data.text)
        try:
            results = self.query({"inputs": preprocessed_text})
            person_names = extract_person_names_from_results(results)
            return PredictResponse(person_names=person_names)
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return PredictResponse(person_names=["Error processing request."])

if __name__ == "__main__":
    host_mlp_cloud(PersonNameExtractor, BaseModel())
