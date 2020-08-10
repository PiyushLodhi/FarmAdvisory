import io
import json
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

def main():
	#kg from unstructured data
	f = open('unstructured_text_book_input_pea.txt')
	lines = f.readlines()
	input_lines = []
	for line in lines:
		# print('here1: '+str(line))
		words =  line.split(' ')
		in_line = []
		for word in words:
			if word=='and' or word==',' or word=='but':
				input_lines.append(in_line)
				in_line = []
				in_line.append('pea')
			else:
				in_line.append(word)
		if in_line!=[]:
			input_lines.append(in_line)
	f.close()
	f = open('input.txt','w+')
	for line in input_lines:
		# print('here2: '+str(line))
		for word in line:
			f.write(word+' ')
		f.write('\n')
	f.close()

	engine = SnipsNLUEngine(config = CONFIG_EN)
	with io.open("dataset1.json") as f:
		dataset = json.load(f)

	engine.fit(dataset)
	_dict = {}
	_dict['pea']={}
	in_file = open('input.txt', 'r')
	lines = in_file.readlines()
	for line in lines:
		if len(line)<=2:
			print('hi')
			continue
		print('line: '+str(line))
		parsing = engine.parse(line)
		print('parsing results: ')
		print(parsing)
		relation = parsing['intent']['intentName']
		prob = float(parsing['intent']['probability'])
		print('prob: '+str(prob))
		print('relation: '+str(relation))
		if relation!='None' and prob>=0.3:
			# print('here')
			slots = parsing['slots']
			for slot in slots:
				if slot['entity']!='crop':
					if relation not in _dict['pea'].keys():
						# print('case1: ')
						# print('relation: '+str(relation))
						_dict['pea'][relation] = slot['rawValue']
					else:
						# print('case2: ')
						# print('relation: '+str(relation))
						_dict['pea'][relation] += (','+slot['rawValue']) 
	print('_dict:-')
	print(_dict)
	#_dict_json = json.dumps(_dict)
	in_file.close()
	with open("output_kg_pea.json", "w") as outfile:
		json.dump(_dict, outfile)
	# with open('output_kg_pea.json', 'r') as openfile:
	# 	json_object = json.load(openfile)
	# print(json_object) 
	#reading and including structured data on disease management in knowledge graph
	# f = open('structured_pea_disease.txt','r')
	# lines = f.readlines()
	# f.close()
	# diseases_list = []
	# flag=0
	# diseaseName =''
	# dict_2_insert={}
	# cnt =0
	# for line in lines:
	# 	line = line[:-1]
	# 	if line=='##':
	# 		cnt=1
	# 	else:
	# 		if cnt==1:
	# 			cnt = 2
	# 			if len(dict_2_insert.keys())>0:
	# 				diseases_list.append(dict_2_insert)
	# 			diseaseName = line
	# 			dict_2_insert[diseaseName] = {}
	# 		elif cnt==2:
	# 			dict_2_insert[diseaseName]['symptom'] = line
	# 			cnt=3
	# 		else:
	# 			if 'management' not in dict_2_insert[diseaseName].keys():
	# 				dict_2_insert[diseaseName]['management'] = line
	# 			else:
	# 				dict_2_insert[diseaseName]['management'] += (':: '+line)
	# print(diseases_list)
	# json_object['diseases']=diseases_list
	# with open("output_kg_pea.json", "w+") as outfile:
	# 	json.dump(json_object, outfile)
	#reading and including structured data on disease management in knowledge graph
	# with open('output_kg_pea.json', 'r') as openfile:
	# 	json_object = json.load(openfile)
	# print(json_object) 
	# f = open('structured_pea_post_prod.txt','r')
	# lines = f.readlines()
	# f.close()
	# line = lines[0][:-1]
	# json_object['postProductionTechnique'] = line
	# with open("output_kg_pea.json", "w+") as outfile:
	# 	json.dump(json_object, outfile)
if __name__ == '__main__':
	main()