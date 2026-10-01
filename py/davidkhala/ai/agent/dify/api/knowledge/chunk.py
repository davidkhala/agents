from davidkhala.ai.agent.dify.api import API
from davidkhala.ai.agent.dify.api.knowledge.document import Document


class Chunk(API):
    def __init__(self, d: Document, segment_id: str):
        super().__init__(d.api_key, f"{d.base_url}/segments/{segment_id}")

    def get(self):
        r = self.request(self.base_url, "GET")
        assert r['doc_form']  # optional value text_model
        return r['data']
