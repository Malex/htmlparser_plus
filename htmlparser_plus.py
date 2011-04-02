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
	def tag_start(self) -> dict:
		return self._s_pos

	@property
	def tag_end(self) -> dict:
		return self._e_pos

	def handle_starttag(self,tag,attrs):
		if not tag in self.tag_start_pos.keys():
			self._s_pos[tag] = []
		self._s_pos[tag].append(self.getpos())

	def handle_startendtag(self,tag,attrs):
		self._empties.append(tag)

	def handle_endtag(self,tag):#,attrs):
		if not tag in self.tag_start.keys() or len(self.tag_start[tag])<=len(self.tag_end[tag]):
			raise ParserError("No matching start tag for {}".format(tag))
		else:
			if not tag in self.tag_end.keys():
				self._e_pos[tag]=[]
			self._e_pos[tag].append(self.getpos())

	def retrieve_text(self,tag :str) -> str: ##TODO: choose specific tag
		if not tag in self.tag_start.keys():
			if tag in self._empties:
				return ""
			else:
				raise ParserError("Tag {} not found".format(tag))
		else:
			lines = self._store.split('\n')
			st = self.tag_start[tag]
			end = self.tag_end[tag]
			sub = [st[0]:end[0]+1]
			sub[0] = sub[0][st[1]:]
			sub[-1] = sub[-1][:end[1]]
			return '\n'.join(sub)
