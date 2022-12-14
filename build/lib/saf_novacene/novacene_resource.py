import requests
from dagster import resource, StringSource, IntSource
from dagster.builtins import String
import pandas as pd
from io import StringIO

class NovaceneAPIResource:
    def __init__(self, host, login, password):
        self._conn_host = host
        self._conn_login = login
        self._conn_password = password

        self._session = None
        self._base_url = None
    

    def get_conn(self):
        """
        Returns the connection used by the resource for querying data.
        Should in principle not be used directly.
        """

        if self._session is None:
            self._base_url = self._conn_host

            # Build our session instance, which we will use for any
            # requests to the API.
            self._session = requests.Session()

            self._session.auth = (self._conn_login, self._conn_password)

        return self._session, self._base_url


    def close(self):
        """Closes any active session."""
        if self._session:
            self._session.close()
        self._session = None
        self._base_url = None

    
    # API methods
    ######################
    def create_dataset(self, filename, df_upload):
        """
        Upload a dataset.
        """
        
        endpoint = "/dataset/"
        
        session, base_url = self.get_conn()
        url = base_url + endpoint
        
        payload = {
            "name": filename,
            "set_type": "file",
            "file_type": "csv"
        }

        files = [
            ('path',(filename, df_upload.to_csv(), 'csv'))
        ]
        
        response = session.post(
            url, data = payload, files = files
        )
        
        response.raise_for_status()
        response_json = response.json()
        
        return(response_json)
    

    def get_file(self, file_url):
        """
        Get file
        """
        
        session, base_url = self.get_conn()

        response = session.get(file_url)
        df_file = pd.read_csv(StringIO(response.text))
        
        return(df_file)



    def job_info(self, job_id):
        """
        Get job information.
        """
        
        endpoint = "/job/" + str(job_id) + "/"
        
        session, base_url = self.get_conn()
        url = base_url + endpoint

        response = session.get(url)
        
        response.raise_for_status()
        response_json = response.json()
        
        return(response_json)


    def enrich_dataset(self, dataset_id, model_id, column_id):
        """
        Enriches a dataset.
        """
        
        endpoint = "/studio/get_local_model_analysis/"
        
        session, base_url = self.get_conn()
        url = base_url + endpoint
        
        payload = {
            "datasetId": int(dataset_id),
            "methodIdx": model_id,
            "colIdx": column_id
        }

        response = session.get(
            url, params = payload
        )
        
        response.raise_for_status()
        response_json = response.json()
        
        return(response_json)
    

    def named_entity_recognition(self, dataset_id, column_id):
        """
        Enriches a dataset.
        """
        
        endpoint = "/studio/named_entity_recognition/"
        
        session, base_url = self.get_conn()
        url = base_url + endpoint
        
        payload = {
            "datasetId": int(dataset_id),
            "selectIdx": column_id
        }

        response = session.get(
            url, params = payload
        )
        
        response.raise_for_status()
        response_json = response.json()
        
        return(response_json)


@resource(
    config_schema={
        "resources": {
            "novacene_resource": {
                "config": {
                    "host": StringSource,
                    "login": StringSource,
                    "password": StringSource
                }
            }
        }
    },
    description="A Novacene API resource.",
)
def initiate_novacene_resource(context):
    return NovaceneAPIResource(
        host = context.resource_config["resources"]["novacene_resource"]["config"]["host"],
        login = context.resource_config["resources"]["novacene_resource"]["config"]["login"],
        password = context.resource_config["resources"]["novacene_resource"]["config"]["password"]
    )