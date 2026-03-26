import requests
from config import COMICVINE_API_KEY, COMICVINE_BASE_URL, REQUEST_TIMEOUT


class ComicVineClient:
    def __init__(self):
        self.api_key = COMICVINE_API_KEY
        self.base_url = COMICVINE_BASE_URL
        self.headers = {
            "User-Agent": "comic-catalog-project/1.0",
            "Accept": "application/json"
        }

    def _get(self, endpoint, params=None):
        if not self.api_key:
            raise ValueError("No se encontró COMICVINE_API_KEY en el archivo .env")

        base_params = {
            "api_key": self.api_key,
            "format": "json"
        }

        if params:
            base_params.update(params)

        url = f"{self.base_url}/{endpoint.strip('/')}/"

        response = requests.get(
            url,
            params=base_params,
            headers=self.headers,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        data = response.json()

        if data.get("status_code") != 1:
            raise ValueError(f"Error Comic Vine: {data.get('error', 'Error desconocido')}")

        return data

    def search_characters(self, query, limit=10, offset=0):
        params = {
            "query": query,
            "resources": "character",
            "limit": limit,
            "offset": offset
        }
        return self._get("search", params)

    def list_issues(self, limit=10, offset=0):
        params = {
            "limit": limit,
            "offset": offset,
            "sort": "date_last_updated:desc",
            "field_list": "id,name,issue_number,deck,description,store_date,cover_date,image,volume,site_detail_url"
        }
        return self._get("issues", params)

    def get_volume_detail(self, volume_id):
        params = {
            "field_list": "id,name,publisher"
        }
        return self._get(f"volume/4050-{volume_id}", params)

    def get_issue_detail(self, issue_id):
        params = {
            "field_list": (
                "id,name,issue_number,deck,description,store_date,cover_date,image,"
                "volume,site_detail_url,person_credits"
            )
        }
        return self._get(f"issue/4000-{issue_id}", params)