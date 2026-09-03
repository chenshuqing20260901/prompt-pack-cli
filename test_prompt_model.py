import unittest
from prompt_model import Prompt
class TestPromptModel(unittest.TestCase):
    def setUp(self):
        self.test_prompt = Prompt(
            id=1,
            title="Customer Avatar Builder",
            category="Marketing",
            content="You are a market research analyst.My business is [BUSINESS TYPE],targeting [AUDIENCE] in [LOCATION].Build a detailed customer avatar including demographics,top 3 pain points,and where they spend time online.",
            tier="free_sample"
        )
    def test_preview(self):
        result = self.test_prompt.preview(50)
        self.assertIn("Customer Avatar Builder", result)
    def test_validate(self):
        self.assertTrue(self.test_prompt.validate())
        self.test_prompt.title = ""
        self.assertFalse(self.test_prompt.validate())
    def test_update(self):
        self.test_prompt.update(title="New title")
        self.assertEqual(self.test_prompt.title, "New title")
if __name__ == '__main__':
    unittest.main()

