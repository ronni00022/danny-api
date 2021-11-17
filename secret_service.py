from configparser import ConfigParser
from elasticsearch import Elasticsearch
from secrets_model import SecretModel


class SecretService():
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
        user = self.config["Elastic"]["username"]
        password = self.config["Elastic"]["password"]
        self.elasticSearch = Elasticsearch(
            ['https://example-233e93.es.us-central1.gcp.cloud.es.io:9243'],
            http_auth=(f'{user}', f'{password}')
        )
        self.index = "secretos"
    
    def getSecrets(self):
        try:
            response = self.elasticSearch.search(index=self.index)
            if response["hits"]["total"]["value"] == 0:
                return None
            return response["hits"]["hits"]
        except:
            return None
    
    def createSecrets(self, model: SecretModel):
        if model is None:
            return None
        response = self.elasticSearch.index(index=self.index,document=model.__dict__)
        return response
    
    def getById(self,id):
        if not id: 
            return None
        try:
            response = self.elasticSearch.get(index=self.index, id=id)
            return response
        except:
            return None
    
    def deleteAll(self):
        response = self.elasticSearch.indices.delete(index=self.index)
        return response        

