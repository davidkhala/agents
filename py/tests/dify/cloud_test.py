import os
import unittest
from datetime import datetime

from davidkhala.utils.syntax.path import resolve
from requests import HTTPError

from davidkhala.ai.agent.dify.api.app import Feedbacks, Conversation
from davidkhala.ai.agent.dify.api.knowledge.chunk import Chunk
from davidkhala.ai.agent.dify.api.knowledge.dataset import Dataset
from davidkhala.ai.agent.dify.api.knowledge.document import Document
from davidkhala.ai.agent.dify.api.knowledge.metadata import Metadata


class CloudTest(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('KB_API_KEY')


class DatasetTest(CloudTest):

    def setUp(self):
        super().setUp()
        self.client = Dataset(self.api_key)

    def test_list(self):
        for dataset in self.client.list_datasets('Thei'):
            print(dataset)

    def test_list_ids(self):
        for _id in self.client.ids:
            print(_id)

    def test_get(self):
        _id = '8bae26cb-a2be-4487-8492-04554a4f7b8b'
        instance = Dataset.Instance(self.client, _id).get()
        print(instance)
        self.assertEqual('8de9da97-a36a-4ad8-a316-0d521d043c29', instance.pipeline_id)


class DocumentTest(CloudTest):
    def setUp(self):
        super().setUp()
        dataset_id = '8bae26cb-a2be-4487-8492-04554a4f7b8b'
        self.client = Dataset.Instance(Dataset(self.api_key), dataset_id)

    def test_upload_readme(self):
        r = self.client.upload(None, path=resolve(__file__, "../../README.md"))
        print(r)
        url = 'https://raw.githubusercontent.com/davidkhala/AI/refs/heads/main/py/README.md'
        r = self.client.upload(None, url=url)
        print(r)
        # update will be 400
        # doc_id = r['id']
        # r = self.client.upload(None, url=url,document_id=doc_id)
        # print(r)

        composite_file = f"{datetime.now().strftime("%Y%m%d_%H%M%S")}.README.md"
        r = self.client.upload(composite_file, url=url)

    def test_upload_pdf(self):
        pdf_path = resolve(__file__, '../fixtures/empty.pdf')
        self.client.upload(None, path=pdf_path)

    def test_unsupported_upload(self):
        # png is not supported
        img_url = 'https://media.goodschool.hk/images/ulogo/thei.png'
        with self.assertRaises(HTTPError) as context:
            self.client.upload(None, url=img_url)
        self.assertEqual(context.exception.response.status_code, 400)
        # HTML should be supported
        html_path = resolve(__file__,
                            "../fixtures/About THEi - Technological and Higher Education Institute of Hong Kong.html")
        with self.assertRaises(HTTPError) as context:
            self.client.upload(None, path=html_path)
        self.assertEqual(context.exception.response.status_code, 403)

    def test_get(self):
        doc_id = 'e97a986b-9613-4f09-a8b2-d069f94bd1f9'
        doc = Document(self.client, doc_id)
        doc.get('without')
        doc.get('only')
        it = doc.get('all')

        print(it.custom_metadata)

    def test_list(self):
        for doc in self.client.list_documents():
            # doc has content, can be lengthy
            print(doc.name)

    def test_has(self):
        name = 'Admission - Technological and Higher Education Institute of Hong Kong.html'
        self.assertTrue(self.client.has_document(name))
        self.assertFalse(self.client.has_document('README'))

    def test_exist(self):
        doc_id = '3568dd90-fe30-4df3-8cc3-9f8a1cb9ee06'
        doc = Document(self.client, doc_id)
        self.assertTrue(doc.exist())
        doc_id = doc_id + '1'
        doc = Document(self.client, doc_id)
        self.assertFalse(doc.exist())

    def test_chunks(self):
        doc_id = 'e97a986b-9613-4f09-a8b2-d069f94bd1f9'
        doc = Document(self.client, doc_id)
        for chunk in doc.list_chunks():
            print(chunk['sign_content'])

    def test_chunk_get(self):
        doc_id = 'a9aff11c-f7e5-42fe-84e0-f21b522a68f9'
        doc = Document(self.client, doc_id)
        chunk_id = 'aa05539b-052e-4ec2-b8af-2067295423a2'
        chunk = Chunk(doc, chunk_id)
        chunk_data = chunk.get()
        self.assertIn('[![](', chunk_data['content'])  # how image, link are stored

    def test_del(self):
        doc_id = '6006f9db-4e7b-4760-a5b5-b8894ac8914c'
        doc = Document(self.client, doc_id)
        doc.delete()


class ChatAppTest(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('APP_API_KEY')

    def test_list_feedback(self):
        f = Feedbacks(self.api_key)
        for feedback in f.list_feedbacks():
            print(feedback['content'])

    def test_messages(self):
        c = Conversation(self.api_key, '999196d8-0842-4617-adcf-aa46e0808404')
        with self.assertRaises(HTTPError) as context:
            c.paginate_messages('f96b5cfc-7006-4afe-b8fe-e0e04374d40f')
        self.assertEqual(context.exception.response.status_code, 404)  # security isolation

    def test_agent_chat(self):
        me = '45bdc865-6d71-40ab-8892-af53906362fa'
        api_key = os.getenv('AGENT_API_KEY')

        c = Conversation(api_key, me)
        r = c.agent_chat("What are the specs of the iPhone 13 Pro Max?")
        print(r['answer'] in r['thought'], r['answer'])

    def test_bot_chat(self):
        me = '45bdc865-6d71-40ab-8892-af53906362fa'
        api_key = os.getenv('BOT_API_KEY')
        c = Conversation(api_key, me)
        r = c.bot_chat("What are the specs of the iPhone 13 Pro Max?")
        print(r)


class MetadataTest(CloudTest):
    def setUp(self):
        super().setUp()
        dataset_id = '8bae26cb-a2be-4487-8492-04554a4f7b8b'
        client = Dataset.Instance(Dataset(self.api_key), dataset_id)
        self.m = Metadata(client)

    def test_list_dataset_metadata(self):
        print(self.m.list())
        id = 'f56f6184-ae86-469c-b132-5402b64dd0c9'
        r = self.m.rename(id, 'intStr')
        print(r)
        r = self.m.rename(id, 'int')
        print(r)

    def test_document_metadata_get(self):
        doc_id = 'e97a986b-9613-4f09-a8b2-d069f94bd1f9'
        r = self.m.of_document(doc_id)
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
        self.m.set(*documents, metadata=metadata)
        # ensure
        for doc_id in documents:
            r = self.m.of_document(doc_id)
            metadata_r = r.custom_metadata
            assert len(metadata_r) == 1

            self.assertDictEqual(metadata_r[0], metadata)

if __name__ == '__main__':
    unittest.main()
