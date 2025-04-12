from unittest import TestCase

from graph_svc import invoke_graph


class Test(TestCase):
    def test_invoke_graph(self):
        user_prompt = "<insert here your test message>"
        graph_response = invoke_graph(user_prompt)
        self.assertIsNotNone(graph_response)
