import json
import os
import unittest

from davidkhala.ai.agent.dify.console.knowledge.dataset import DocumentOperation
from davidkhala.ai.agent.dify.console.knowledge.pipeline import Datasource, Pipeline
from davidkhala.ai.agent.dify.console.plugin import ConsolePlugin
from davidkhala.ai.agent.dify.console.session import ConsoleUser
from davidkhala.ai.agent.dify.const import IndexingStatus
from davidkhala.ai.agent.dify.db.app import Studio
from davidkhala.ai.agent.dify.db.knowledge import Dataset, Document, Pipeline as DBPipeline
from davidkhala.ai.agent.dify.db.sys import Info
from davidkhala.ai.agent.dify.interface import IndexingError


class DBTest(unittest.TestCase):
    def setUp(self):
        connection_str = "postgresql://postgres:difyai123456@localhost:5432/dify"
        self.app = Studio(connection_str)
        self.ds = Dataset(connection_str)
        self.doc = Document(connection_str)
        self.info = Info(connection_str)

    def test_properties(self):
        print(self.app.apps)
        print(self.info.accounts)

    def test_user_feedbacks(self):
        print(self.app.get_dict(Studio.user_feedbacks_sql))

    def test_generate_conversation_opener(self):
        from davidkhala.llm.api.openrouter import OpenRouter
        # config
        app_id = '4f3c212a-0dc8-4405-97ca-22914c79a21e'
        question_size = 3
        api_key = os.environ.get('OPENROUTER_API_KEY')
        self.openrouter = OpenRouter(api_key)
        self.openrouter.as_chat('openrouter/free')
        config = self.app.app_config(app_id)
        self.assertIsNotNone(config)
        print('current suggested_questions', config.suggested_questions)
        new_questions = []
        for d in self.doc.hit_documents(question_size):
            dataset_id = d['dataset_id']
            content = d['content']
            questions = self.ds.dataset_queries(dataset_id)
            prompt = f"""
            Based on below knowledge base document content, generate single question that user may ask against the content. 
            Don't assume user have document content as prior knowledge.
            You should learn and follow language style from sample questions listed below. And you respond generated question text only

            sample questions:
            {questions}  

            document content is:
            {content}
            """
            choices = self.openrouter.chat(prompt)
            new_questions.append(choices[0].strip())
        config.suggested_questions = json.dumps(new_questions)
        self.app.update_app_config(config)


class ConsoleTest(unittest.TestCase):
    def setUp(self):
        self.console = ConsoleUser()
        self.console.login("david-khala@hotmail.com", "davidkhala2025")
        self.connection_str = "postgresql://postgres:difyai123456@localhost:5432/dify"
        dataset = "5be5a7b0-b725-40e7-a4e8-4ed953ef054e"
        self.console_ops = DocumentOperation(self.console, dataset)

    def test_user(self):
        print(self.console.me)
        print(self.console.workspace)

    def test_console_sync(self):

        doc_source = 'Home - Technological and Higher Education Institute of Hong Kong'

        db_doc = Document(self.connection_str)
        ids = db_doc.id_by(doc_source)
        assert len(ids) == 1
        document = ids[0]
        with self.assertRaisesRegex(IndexingError, 'no website import info found'):
            self.console_ops.website_sync(document)

    def test_console_rerun(self):

        doc_source = 'Home - Technological and Higher Education Institute of Hong Kong'
        dataset = "5be5a7b0-b725-40e7-a4e8-4ed953ef054e"
        db_doc = Document(self.connection_str)
        ids = db_doc.id_by(doc_source)

        returns = self.console_ops.rerun(dataset, *ids)
        print(returns)

    def test_pipeline(self):
        db_pipe = DBPipeline(self.connection_str)
        pipelines = db_pipe.pipelines
        for p in pipelines:
            for source in p['graph'].datasources:
                print(source.datasource_type)

    def test_console_pipeline(self):
        db_pipe = DBPipeline(self.connection_str)
        pipelines = db_pipe.pipelines
        db_ds = Dataset(self.connection_str)

        ids = db_ds.credential_id_by("public", "firecrawl")
        credential_id = str(ids[0])
        self.assertEqual(len(pipelines), 1)
        p = pipelines[0]
        nodes = p['graph'].datasources
        p_id = p['app_id']
        node = nodes[0]
        url= "https://thei.edu.hk/"

        load = Pipeline(self.console)

        datasource_info_list = [{
            'title': url,
            'credential_id': credential_id,
            'source_url': url
        }]


        run_r = load.async_run(p_id, node, inputs={
        }, datasource_info_list=datasource_info_list)
        console_ops = DocumentOperation(self.console, run_r.dataset.id)
        # wait until
        for document in run_r.documents:
            final = console_ops.wait_until(document.id,
                                           from_status=[IndexingStatus.WAITING, IndexingStatus.PARSING,
                                                        IndexingStatus.COMPLETED, IndexingStatus.FAILED])
            print(final)

    def test_plugin_get(self):
        pluginManage = ConsolePlugin(self.console)
        plugins = ["langgenius/azure_openai", "langgenius/siliconflow", 'notexist']
        r = pluginManage.get(*plugins)
        self.assertEqual(2, len(r))

        r = pluginManage.get('notexist')
        self.assertEqual(0, len(r))
        r = pluginManage.get('langgenius/deepseek')
        print(r)

    def test_plugin_list(self):
        pluginManage = ConsolePlugin(self.console)
        r = pluginManage.plugins()
        print(r)

    def test_plugin_install(self):
        pluginManage = ConsolePlugin(self.console)
        from davidkhala.ai.agent.dify.plugins.popular import Node
        r = pluginManage.upgrade(*Node.agent)

        pluginManage.uninstall_by(*Node.agent)
        current = pluginManage.get(*Node.agent)
        self.assertEqual(0, len(current))


if __name__ == '__main__':
    if not os.getenv('CI'):
        unittest.main()
