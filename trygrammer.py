class Test1:
	def __init__(self, name):
		self.x = 1
		self.obj = Test2(name, self)

class Test2:
	def __init__(self, name, p_self):
		self.name = name
		self.p_self = p_self

	def test_function(self):
		print(self.p_self.x)


class Test4:
	def __init__(self, x):
		self.x = x

class Test3:
	def __init__(self):
		self.x = []

	def append(self, ele: Test4):
		self.x.append(ele)

class MyList(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        self.append('FirstMen')
        self.name = 'Westeros'

if __name__ == "__main__":
	"""
		t1 = Test1("hi")
		t1.obj.test_function()
	"""

	t3 = Test3()
	t3.append(1)

	t5 = MyList()
	t5.append("dt5")
	print(t5)