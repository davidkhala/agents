import os
import unittest

from davidkhala.ai.agent.dify.api.knowledge.dataset import Dataset, Instance
from davidkhala.ai.agent.dify.api.knowledge.document import Document
from davidkhala.ai.agent.dify.console.knowledge.dataset import DocumentMetadata
from davidkhala.ai.agent.dify.const import IndexingStatus
from tests.util import prepare_logger


class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('KB_API_KEY')
        dataset_id = '8bae26cb-a2be-4487-8492-04554a4f7b8b'
        self.client = Dataset.Instance(Dataset(self.api_key), dataset_id)
        self.logger = prepare_logger('py/tests/dify/cloud_doc.log')

    def test_del_pending(self):
        for doc in self.client.list_documents():
            # doc has content, can be lengthy
            if doc['indexing_status'] == IndexingStatus.WAITING:
                print(doc)
                self.logger.warning(doc)


class ConsoleTestCase(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('KB_API_KEY')

        from davidkhala.ai.agent.dify.console.session import ConsoleUser
        self.console = ConsoleUser(base_url='https://cloud.dify.ai')

        self.console.set_tokens(
            csrf='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzI0NjE2MjcsInN1YiI6IjQ1YmRjODY1LTZkNzEtNDBhYi04ODkyLWFmNTM5MDYzNjJmYSJ9.pV0PY4MebZqcWWtGU4UqfuSdPi99vBtP1Mt5g6GOVZA',
            access='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDViZGM4NjUtNmQ3MS00MGFiLTg4OTItYWY1MzkwNjM2MmZhIiwiZXhwIjoxNzcyNDYxNjI3LCJpc3MiOiJDTE9VRCIsInN1YiI6IkNvbnNvbGUgQVBJIFBhc3Nwb3J0In0.keHWorgFW2b0bz8zhvxTheddmaCaVpbO-qYyIJVxdD4',
        )
        self.metadata = DocumentMetadata(self.console, '8bae26cb-a2be-4487-8492-04554a4f7b8b')  # Thei one details

    def test_list_metadata(self):
        r = self.metadata.list()
        print(r)

    def test_set_metadata(self):

        documents = [
            'e97a986b-9613-4f09-a8b2-d069f94bd1f9',
            "d30300cf-a11c-4018-8b3c-07820bec11c0",
            "38eb6e0c-ca99-40f9-a3d0-96890ef3d16b",
            "4e1738a6-0a8c-4953-9c72-135139302665",
            "704c0765-d524-4817-8cf3-5a8366c38907"
        ]  # master
        metadata = {
            'level': 'postgraduate'
        }
        self.metadata.set(*documents, metadata=metadata)
        # ensure
        self.client = Instance(Dataset(self.api_key), self.metadata.dataset)
        for doc_id in documents:
            doc = Document(self.client, doc_id)
            metadata_r = doc.get('only').custom_metadata
            assert len(metadata_r) == 1

            self.assertDictEqual(metadata_r[0], metadata)

    def test_pipeline(self):
        # pre-requisite: prepare cookie and api_key first
        dataset_id = '34a72f60-c9ab-4067-abc1-34cb951e7239'
        firecrawl_key_name = 'key'
        from davidkhala.ai.agent.dify.console.knowledge.pipeline import Pipeline
        console_pipeline = Pipeline(self.console)
        url = "https://thei.edu.hk/"
        ds = Instance(Dataset(self.api_key), dataset_id)
        rs = console_pipeline.filecrawl(url, ds, firecrawl_key_name)
        print(rs)



if __name__ == '__main__':
    unittest.main()
