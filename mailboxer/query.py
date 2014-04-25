import requests

class Query(object):

    _metadata = None

    def __init__(self, client, url, objtype, page_size=100):
        super(Query, self).__init__()
        self.client = client
        self.url = url.set_query_param("page_size", str(page_size))
        self.objtype = objtype
        self.page_size = page_size
        self._objects = None

    def _fetch_page(self, page_index):
        assert page_index > 0
        result = requests.get(self.url.set_query_param("page", str(page_index)))
        result.raise_for_status()
        result_json = result.json()
        if self._objects is None:
            self._objects = [None] * int(result_json["metadata"]["total_num_objects"])
        for index, obj in enumerate(result_json["result"]):
            self._objects[index + ((page_index - 1) * self.page_size)] = obj

    def __iter__(self):
        for obj in self.get_json_objects():
            yield self.objtype.from_query_json(self.client, obj)

    def get_json_objects(self):
        for i in range(len(self)):
            obj = self._objects[i]
            if self._objects[i] is None:
                self._fetch_page((i // self.page_size) + 1)
            assert self._objects[i] is not None
            yield self._objects[i]

    def __len__(self):
        if self._objects is None:
            self._fetch_page(1)
        return len(self._objects)
