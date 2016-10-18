def find_element_by_id(target_list, code):
	try:
		return filter(lambda x: x.code == code, target_list)[0]
	except:
		raise Exception('target list has no element of id {}'.format(code))

def get_name_from_id(target_list, code):
	target = find_element_by_id(target_list, code)
	return target.name

def add_element(target_list, element):
	if element not in target_list:
		target_list.append(element)
	else:
		raise Exception("id {} already exists".format(element.code))

def delete_element(target_list, element_or_code):
	if type(element_or_code) == int:
		element = filter(lambda x: x.code == element_or_code)[0]
	else:
		element = element_or_code

	try:
		target_list.remove(element)
	except:
		raise Exception("id {} does not exist".format(element.code))

def check_name_and_code(target_list, code, name):
	element = find_element_by_id(target_list, code)
	if element.name != name:
		raise Exception("Entity id {} has name {}, not {}".format(code, element.name, name))
