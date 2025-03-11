import unittest
from agents.agent import Agent

class TestAgent(unittest.TestCase):
    def test_agent_initialization(self):
        agent = Agent("dummy_api_key")
        self.assertIsNotNone(agent)

if __name__ == "__main__":
    unittest.main()