# -*- coding: utf-8 -*-
import os
import requests

from dotenv import load_dotenv
load_dotenv()
from pprint import pprint

class Microsoft():
    def __init__(self, base_url, subscription_key):
        self.base_url = base_url
        self.sentiment_url = base_url + "sentiment"
        self.keyphrases_url = base_url + "keyPhrases"
        self.languages_url = base_url + "languages"
        self._key = subscription_key
        self._headers = {
            'Ocp-Apim-Subscription-Key': self._key
        }

        
    def _document_to_dict(self, document, id, lang):
        result = {
            "id": id,
            "text": document
        }
        if lang:
            result["language"] = lang

        return result

    
    def _build_payload(self, documents, lang=None):
        documents_json = [self._document_to_dict(document, id, lang)
                          for (id, document) in enumerate(documents)]

        return {
            "documents": documents_json
        }

    
    def detectSentiment(self, documents, lang="en"):
        """Calls the sentiment detection API and returns result as a json object.

        Parameters
        ----------
        documents: list
            a list where each element is a document
        lang: string
            optional language, default is "en"
        """
        
        response = requests.post(self.sentiment_url, headers=self._headers,
                                 json=self._build_payload(documents, lang))
        result = response.json()
        return result

    
    def detectKeyPhrases(self, documents, lang="en"):
        """Calls the key phrases detection API and returns result as a json object.

        Parameters
        ----------
        documents: list
            a list where each element is a document
        lang: string
            optional language, default is "en"
        """
        response = requests.post(self.keyphrases_url, headers=self._headers,
                                 json=self._build_payload(documents, lang))
        result = response.json()
        return result

    
    def detectLanguages(self, documents):
        """Calls the language detection API and returns result as a json object.

        Parameters
        ----------
        documents: list
            a list where each element is a document
        lang: string
            optional language, default is "en"
        """
        
        response = requests.post(self.languages_url, headers=self._headers,
                                 json=self._build_payload(documents))
        result = response.json()
        return result

    
    def detectEntities(self, documents):
        raise Exception("Not available")


if __name__ == '__main__':
    base_url = "https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/"
    subscription_key = os.getenv('MICROSOFT_SUBSCRIPTION_KEY')

    service = Microsoft(base_url, subscription_key)
    documents = [
        'I had a wonderful experience! The rooms were wonderful and the staff was helpful.',
        'I had a terrible time at the hotel. The staff was rude and the food was awful.',
    ]
    pprint(service.detectSentiment(documents))
    pprint(service.detectKeyPhrases(documents))
    pprint(service.detectLanguages(documents))

    documents = [
        '이 영화는 재미있다',
        '이 영화는 마음에 안들어요',
    ]
    pprint(service.detectLanguages(documents))
    