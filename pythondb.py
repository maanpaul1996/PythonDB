import json

class PythonDB:

	db = {}

	def __init__(self):
		return None

	def addTable(self, table_name):
		self.db[table_name] = []

	def insert(self, table_name, values):
		if values == None or table_name == None:
			"Error : Table name or Values is missing"
		elif table_name not in self.db.keys():
			print "Error : Table '%s' doesn't exist" %(table_name)
		else:
			self.db[table_name].append(values)


	def select(self, table_name, condition=None, structure=None, allow=False, result=[]):

		if len(result) > 0 :
			result = []

		if table_name == None:
			"Error : Table name is missing"
		elif table_name not in self.db.keys():
			print "Error : Table '%s' doesn't exist" %(table_name)
		else:
			if condition  == None or not condition:
				for row in self.db[table_name]:
					result.append(row)
			else:
				for row in self.db[table_name]:
					for key, value in condition.items():
						allow = self.dict_ittrate(key=key, value=value, row=row)
						if not allow:
							break
					if allow:
						result.append(row)
					allow=False
		
		if structure==None or not structure:
			return result
		else : 
			result,temp =self.structure(result=result, structure=structure)
			return	result

	def structure(self, structure=None, result=None, overload_result=None, universal_break=False, overload_break=False):
		
		temp_result = []
		if overload_result!=None:
			t_result = overload_result
		else:
			t_result = {}

		for row in result:
			for key, value in structure.items():
				if isinstance(value, dict):
					if key in t_result and overload_break:
						temp, overload_break = self.structure(structure=value, result=[row[key]],overload_result=t_result[key], universal_break=overload_break)
					else:
						temp,overload_break = self.structure(structure=value, result=[row[key]])
					t_result[key] = temp[0]
				elif len(value.split(":")) == 1:
					t_result[key]=row[key]
				elif len(value.split(":")) > 1:
					if value.split(":")[0].lower() == "group_concat":
						if universal_break==True:
							t_result[key]= t_result[key]+ ', ' + row[key]
						else:
							t_result[key]=row[key]

						universal_break=True
				else:
					exit("unknowe condition in structure!!!")

			if universal_break==False and overload_break==False:
				temp_result.append(t_result)
				t_result = {}

		if universal_break!=False or overload_break!=False:
			temp_result.append(t_result)

		return temp_result, universal_break

	def update(self, values, condition=None, table_name=None, sub_db=None):
		
		if condition==None:

			for row in self.db[table_name]:
				self.update_org(values=values, db=row)

		else:
			for row in self.db[table_name]:
				for key, value in condition.items():
					allow = self.dict_ittrate(key=key, value=value, row=row)
					if not allow:
						break
				if allow:
					self.update_org(values=values, db=row)
	
	def update_org(self, values, db):
		for key,value in values.items():
			if isinstance(value, dict):
				db[key] = self.update_org(values=value, db=db[key])
			else:
				db[key] = value
		return db

	def dict_ittrate(self, key, value, row, allow=False):
		if key.lower() == 'or' and isinstance(value, dict):
			for int_key, int_value in value.items():
				allow =  self.search(key=int_key, value=int_value, data=row)
				if allow:
					break
		elif key.lower() == 'and' and isinstance(value, dict):
			for int_key, int_value in value.items():
				allow =  self.search(key=int_key, value=int_value, data=row)
				if not allow:
					break
		else:
			allow =  self.search(key=key, value=value, data=row)

		return allow

	def search(self, key, value, data, allow=False):
		if key.lower() in data.keys():
			if isinstance(value, dict):
				for int_key, int_value in value.items():
					allow=self.dict_ittrate(key=int_key, value=int_value, row=data[key])
					if not allow:
						break
			else:
				if isinstance(data[key], list):
					if value in data[key]:
						allow=True
				elif isinstance(value, list):
					if data[key] in value:
						allow=True
				elif len(value.split(':')) > 1:
					temp_value = value.split(':')
					if temp_value[0].lower() == "=":
						if (data[key].lower().lower() if isinstance(data[key].lower(), str) else data[key].lower()) == (temp_value[1].lower() if isinstance(temp_value[1], str) else temp_value[1]):
							allow=True
					elif temp_value[0].lower() == ">":
						if (data[key].lower() if isinstance(data[key].lower(), int) else int(data[key].lower())) > (temp_value[1] if isinstance(temp_value[1], int) else int(temp_value[1])):
							allow=True
					elif temp_value[0].lower() == "<":
						if (data[key].lower() if isinstance(data[key].lower(), int) else int(data[key].lower())) < (temp_value[1] if isinstance(temp_value[1], int) else int(temp_value[1])):
							allow=True
					elif temp_value[0].lower() == ">=":
						if (data[key].lower() if isinstance(data[key].lower(), int) else data[key].lower()) >= (temp_value[1] if isinstance(temp_value[1], int) else temp_value[1]):
							allow=True
					elif temp_value[0].lower() == "<=":
						if (data[key].lower() if isinstance(data[key].lower(), int) else data[key].lower()) <= (temp_value[1] if isinstance(temp_value[1], int) else temp_value[1]):
							allow=True
					elif temp_value[0].lower() == "<>":
						if (data[key].lower() if isinstance(data[key].lower(), int) else data[key].lower()) <> (temp_value[1] if isinstance(temp_value[1], int) else temp_value[1]):
							allow=True
				elif (data[key].lower() if isinstance(data[key], str) else data[key]) == (value.lower() if isinstance(value, str) else value):
					allow=True

		return allow
