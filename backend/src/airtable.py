from dataclasses import dataclass
import requests


# Going to make this into a Class. Why? ...
# NOTE Using dataclass we don't have to def __init__
# NOTE This class is basically a basic airtable_client! Neat!
@dataclass()
class Airtable:
    base_id:str
    api_key:str
    table_name:str


    # NOTE Need to add self arg
    # NOTE email:str = None works with "user_email": email in fields
    # Changing to data dict param to make more robust
    def create_records(self, data:dict) -> bool:
        # if email is None:
        #     return False
        if len(data.keys()) == 0:
            return False

        endpoint = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "records": [
                {
                    # Using data dict:
                    "fields": data
                    # Using single email field:
                    # "fields": {
                    #     # Column names in your Airtable table
                    #     "user_email": data
                    # }
                }
            ]
        }

        # Now make the actual request
        response = requests.post(url=endpoint, json=data, headers=headers)
        print("Airtable::endpoint: ", endpoint, "type(response): ", type(response))  # Works!
        # NOTE This means that my airtable_client in main.py is reading my ENV vars correctly
        # <class'requests.models.Response'>


        return response.status_code == 200 or response.status_code == 201

