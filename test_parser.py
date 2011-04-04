import unittest
import htmlparser_plus

class TestParser(unittest.TestCase):
	parser = htmlparser_plus._Parser()

	def setUp(self):
		self.data = """
		<lol><h1 size=4>hihi</h1>
		<li>lol</li>
		</lol>"""

	def test_text(self):
		self.parser.feed(self.data)
		self.assertEqual(self.parser.retrieve_text("li"),"lol")

	def tearDown(self):
		self.parser.close()

if __name__=='__main__':
	unittest.main()
