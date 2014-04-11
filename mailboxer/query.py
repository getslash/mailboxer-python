import requests

class Query(object):

    _metadata = None

    def __init__(self, client, url, objtype):
        super(Query, self).__init__()
        self.client = client
        self.url = url
        self.objtype = objtype

    def _fetch_page(self, page_index):
        result = requests.get(self.url.set_query_param("page", str(page_index)))
        result.raise_for_status()
        result_json = result.json()
        if self._metadata is None:
            self._metadata = result_json["metadata"]

    def get_metadata(self):
        if self._metadata is None:
            self._fetch_page(1)
        return self._metadata

    def __iter__(self):
        for obj in self.get_json_objects():
            yield self.objtype(self.client, obj)

    def __len__(self):
        return self.get_metadata()["total_num_objects"]
