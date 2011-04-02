import html.parser

class ParserError(Exception):
	pass

class _Parser(html.parser.HTMLParser):

	_s_pos = {}
	_e_pos = {}
	_empties = []

	def feed(self,data :str):
		self._store = data
		super().feed(self,data)

	@property
	def tag_start_pos(self) -> dict:
		return self._s_pos

	@property
	def tag_end_pos(self) -> dict:
		return self._e_pos

	def handle_starttag(self,tag,attrs):
		if not tag in self.tag_start_pos.keys():
			self._s_pos[tag] = []
		self._s_pos[tag].append(self.getpos())

	def handle_startendtag(self,tag,attrs):
		self._empties.append(tag)

	def handle_endtag(self,tag):#,attrs):
		if not tag in self.tag_start_pos.keys() or len(self.tag_start_pos[tag])<=len(self.tag_end_pos[tag]):
			raise ParserError("No matching start tag for {}".format(tag))
		else:
			if not tag in self.tag_end_pos.keys():
				self._e_pos[tag]=[]
			self._e_pos[tag].append(self.getpos())

	def retrieve_text(self,tag): ##TODO: choose specific tag
		if not tag in self.tag_start_pos.keys():
			if tag in self._empties:
				return ""
			else:
				raise ParserError("Tag {} not found".format(tag))
		else:
			t = self._store.split('\n')
			##TODO: to finish
