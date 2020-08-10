from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UsersLoginForm
from .forms import UsersRegisterForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import SelectedCrop
from django.contrib.auth.models import User
from datetime import date
from py2neo import Graph, Node, Relationship
import json
import glob
import csv
from pprint import pprint
import pyowm
from collections import OrderedDict 
from django.views.decorators.csrf import csrf_exempt

def index(request):
	username = None
	if 'username' in request.session:
		username = request.session['username']
	return render(request, 'FarmerAdvisory/index.html', {
		'username' : username,
	})

def login_view(request):
	form = UsersLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		request.session['username'] = username
		user = authenticate(username = username, password = password)
		login(request, user)
		return redirect("/FarmerAdvisory")
	return render(request, "FarmerAdvisory/form.html", {
		"form" : form,
		"title" : "Login",
	})

def register_view(request):
	form = UsersRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save()
		password = form.cleaned_data.get("password")	
		user.set_password(password)
		user.save()
		new_user = authenticate(username = user.username, password = password)
		login(request, new_user)
		return redirect("/FarmerAdvisory/login")
	return render(request, "FarmerAdvisory/form.html", {
		"title" : "Register",
		"form" : form,
	})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/FarmerAdvisory")

def getCropData(request):
	crop = request.GET.get('crop')
	graph = Graph()
	cypher = graph.cypher
	data = {}
	cropGrownIn = ""
	climateRequirement = ""
	minwaterRequirement = ""
	maxwaterRequirement = ""
	soilRequirement = ""
	maxrainfallRequirement = ""
	minrainfallRequirement = ""
	totalGrowingPeriod = ""
	mintemperatureRequirement = ""
	maxtemperatureRequirement = ""
	cropContains = ""
	productionTechnique = ""
	postProductionTechnique = ""
	pestManagement = {}
	cropDisease = []
	suf = ', '
    #cropGrownIn
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:CropGrownIn) where n.name='"+crop+"' return n2.descrp as descrp"):
		cropGrownIn = cropGrownIn + record.descrp + ", "
	if cropGrownIn.endswith(suf):
		cropGrownIn = cropGrownIn[:-len(suf)]
	data['cropGrownIn'] = cropGrownIn
    #climateRequirement
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:climateRequirement) where n.name='"+crop+"' return n2.descrp as descrp"):
		climateRequirement = climateRequirement + record.descrp + ", "
	if climateRequirement.endswith(suf):
		climateRequirement = climateRequirement[:-len(suf)]
	data['climateRequirement'] = climateRequirement
    #minwaterRequirement
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:minwaterRequirement) where n.name='"+crop+"' return n2.descrp as descrp"):
		minwaterRequirement = minwaterRequirement + record.descrp
	data['minwaterRequirement'] = minwaterRequirement
    #maxwaterRequirement
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:maxwaterRequirement) where n.name='"+crop+"' return n2.descrp as descrp"):
		maxwaterRequirement = maxwaterRequirement + record.descrp
	data['maxwaterRequirement'] = maxwaterRequirement
    #soilRequirement
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:soilRequirement) where n.name='"+crop+"' return n2.descrp as descrp"):
		soilRequirement = soilRequirement + record.descrp + ", "
	if soilRequirement.endswith(suf):
		soilRequirement = soilRequirement[:-len(suf)]
	data['soilRequirement'] = soilRequirement
    #maxrainfallRequirement
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:maxrainfallRequirement) where n.name='"+crop+"' return n2.descrp as descrp"):
		maxrainfallRequirement = maxrainfallRequirement + record.descrp
	data['maxrainfallRequirement'] = maxrainfallRequirement
    #minrainfallRequirement
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:minrainfallRequirement) where n.name='"+crop+"' return n2.descrp as descrp"):
		minrainfallRequirement = minrainfallRequirement + record.descrp
	data['minrainfallRequirement'] = minrainfallRequirement
    #totalGrowingPeriod
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:totalGrowingPeriod) where n.name='"+crop+"' return n2.descrp as descrp"):
		totalGrowingPeriod = totalGrowingPeriod + record.descrp
	data['totalGrowingPeriod'] = totalGrowingPeriod
    #maxtemperatureRequirement
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:maxtemperatureRequirement) where n.name='"+crop+"' return n2.descrp as descrp"):
		maxtemperatureRequirement = maxtemperatureRequirement + record.descrp
	data['maxtemperatureRequirement'] = maxtemperatureRequirement
    #mintemperatureRequirement
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:mintemperatureRequirement) where n.name='"+crop+"' return n2.descrp as descrp"):
		mintemperatureRequirement = mintemperatureRequirement + record.descrp
	data['mintemperatureRequirement'] = mintemperatureRequirement
    #cropContains
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:contains) where n.name='"+crop+"' return n2.descrp as descrp"):
		cropContains = cropContains + record.descrp
	data['cropContains'] = cropContains
    #productionTechnique
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:productionTechnique) where n.name='"+crop+"' return n2.descrp as descrp"):
		productionTechnique = productionTechnique + record.descrp
	data['productionTechnique'] = productionTechnique
    #postProductionTechnique
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:postProductionTechnique) where n.name='"+crop+"' return n2.descrp as descrp"):
		postProductionTechnique = postProductionTechnique + record.descrp
	data['postProductionTechnique'] = postProductionTechnique
    #pestManagement
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:pestManagement) -[r2]->(n3) where n.name='"+crop+"' return n3.name as name ,n3.descrp as descrp"):
		pestManagement[record.name] = record.descrp
	data['pestManagement'] = pestManagement
    #cropDisease
	disease = {}
	thisset = {'dummy'}
	for record in cypher.execute("Match(n:Crop) -[r]-> (n2:diseases) -[r1]->(n3) -[r2]->(n4) where n.name='"+crop+"' return n3.name as disease_name"):
		thisset.add(record.disease_name)
	for element in thisset:
		if element != 'dummy':
			data1 = {}
			for record in cypher.execute("Match(n:Crop) -[r]-> (n2:diseases) -[r1]->(n3) -[r2]->(n4:symptom) where n.name='"+crop+"' and n3.name = '"+element+"' return n4.descrp as symptom"):
                #print(record.symptom)
				data1['symptom'] = record.symptom
			for record in cypher.execute("Match(n:Crop) -[r]-> (n2:diseases) -[r1]->(n3) -[r2]->(n4:management) where n.name='"+crop+"' and n3.name = '"+element+"' return n4.descrp as disease_management"):
                #print(record.disease_management)
				data1['management'] = record.disease_management
			disease[element] = data1
	cropDisease.append(disease)
	data['disease'] = cropDisease
	print(json.dumps(data, sort_keys=True, indent=4))
	return JsonResponse(data)

def cropHandling_view(request):
	username = None
	if 'username' in request.session:
		username = request.session['username']
	return render(request, 'FarmerAdvisory/cropHandling.html', {
		'username' : username,
	})
def cropPlan(request):
	username = None
	if 'username' in request.session:
		username = request.session['username']
	data = getLocationInfo()
	return render(request, 'FarmerAdvisory/cropPlan.html', {
		'username' : username,
		'state' : data['state'],
		'climate' : data['climate'],
		'soil' : data['soil'],
	})

def chatPortal(request):
	username = None
	if 'username' in request.session:
		username = request.session['username']
	return render(request, 'FarmerAdvisory/chatPortal.html', {
		'username' : username,
	})

def setState(request):
	username = request.session['username']
	#get user_id
	user_id = User.objects.get(username=username).pk
	query = SelectedCrop.objects.filter(farmer_id=user_id)
	crop_list = query.values_list('cropname', flat=True).order_by('id')
	i = 0
	data = {}
	for crop in crop_list:
		data[i] = crop
		i = i + 1
		print(crop)
	data['len'] = i
	return JsonResponse(data)
def addCrop(request):
	crop = request.GET.get('crop')
	print("add: " +crop)
	the_username = request.session['username']
	#get user_id
	user_id = User.objects.get(username=the_username).pk
	today = date.today().isoformat()
	instance = SelectedCrop(farmer_id = user_id,cropname = crop,date = today)
	instance.save() # save crop for the_user

	print(user_id)
	data = {
        'respond': "1"
    }
	return JsonResponse(data)


def removeCrop(request):
	crop = request.GET.get('crop')
	print("remove: "+ crop)
	the_username = request.session['username']
	#get user_id
	user_id = User.objects.get(username=the_username).pk
	instance = SelectedCrop.objects.get(farmer_id=user_id,cropname = crop)
	instance.delete()
	data = {
        'respond': "1"
	}
	return JsonResponse(data)


def getLocationInfo():
	graph = Graph()
	cypher = graph.cypher
	# get State
	data = {}
	State = []
	with open('indian_states.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			State.append(row[1])
	print("states_name : ",State)
	data['state'] = State
	#climate
	qry = "MATCH(n:climateRequirement) RETURN n"
	res = cypher.execute(qry)
	climateConditions = []
	for i in range(len(res)):
		climateConditions.append(res[i].n['descrp']) 
	data['climate'] = climateConditions 
	print(climateConditions)
	
	###Soil
	qry = "MATCH(n:soilRequirement) RETURN n"
	res = cypher.execute(qry)
	soilConditions = []
	for i in range(len(res)):
		soilConditions.append(res[i].n['descrp'])  
	data['soil'] = soilConditions
	print(soilConditions)

	return data
# get recommended crop
def initialise_votes(cypher, vote):
	qry = "MATCH(n:Crop) RETURN n"
	res = cypher.execute(qry)
	for i in range(len(res)):
		crop_name = res[i].n['name']
		vote[crop_name] = 0.0
	print("\nVotes_initialized")

# for state, climate and soil based votes
# name : condition name
# type : climate/soil/states
def UpdateVote1(cypher, name, vote_prior, type, vote):
	qry = "MATCH(n2:Crop)-[r:requires]->(n) WHERE n.name={a} and n.descrp={b} RETURN n2"
	res = cypher.execute(qry, a=type, b=name)
	if(type=="CropGrownIn"):
		q = "MATCH(n2:Crop)-[r:requires]->(n) WHERE n.descrp={a} RETURN n2"
		name = "ALL_INDIAN_STATES"
		r = cypher.execute(q, a=name)
		for i in range(len(r)):
			vote[r[i].n2['name']] += vote_prior
	for i in range(len(res)):
		crop_name = res[i].n2['name']
		vote[crop_name] += vote_prior



# for rainfall, temperature
# type : rain/temp
# req : temp in C or rainfall in cm 
def UpdateVote2(cypher, vote_prior, type, vote, req):
	qry = "MATCH(n2:Crop)-[r:requires]->(n) WHERE n.name={a} RETURN n,n2"
	res_min = cypher.execute(qry, a="min"+type)
	res_max = cypher.execute(qry, a="max"+type)
	if(len(res_min) != len(res_max)):
		print("\nSOME ERROR OCCURED!!! >>>>> length mismatched\n")
	else:
		for i in range(len(res_min)):
			min_req = int(res_min[i].n['descrp'])
			max_req = int(res_max[i].n['descrp'])
			if(req>=(min_req-5) and req<=(max_req+5)):
				crop_name = res_min[i].n2['name'] # same as res_max[i].n2['name']
				vote[crop_name] += vote_prior/2
			if(req>=min_req and req<=max_req):
				crop_name = res_min[i].n2['name'] # same as res_max[i].n2['name']
				vote[crop_name] += vote_prior/2
#@csrf_exempt
def getRecommendedCrop(request):
	state = request.POST.get('state')
	city = request.POST.get('city')
	climate = request.POST.getlist('climateType[]')
	soil = request.POST.getlist('soilType[]')
	temperature = request.POST.get('temperature')
	rainfall = request.POST.get('rainfall')
	print(state)
	print(city)
	print(climate)
	print(soil)
	print(temperature)
	print(rainfall)

	API_key = "627f715328f92e57880cd248e1485935" #input('ENTER API KEY ONLY FOR ADMIN : ')

	graph = Graph()
	cypher = graph.cypher

	vote = {} # dict containing votes for each crop e.g. "wheat":3
	state_vote = 3.0
	climate_vote1 = 1.5
	climate_vote2 = 1.0
	soil_vote1 = 1.5
	soil_vote2 = 1.0
	temp_vote = 1.2
	rain_vote = 1.0
	initialise_votes(cypher, vote)
	states_SF = {}
	states_FF = {}

	with open('indian_states.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			states_SF[row[1]] = row[2]
			states_FF[row[2]] = row[1]
	# filter on the basis of state
	UpdateVote1(cypher, state, state_vote, "CropGrownIn",vote)
	# filter on the basis of climate
	if len(climate) == 2:
		UpdateVote1(cypher, climate[0], climate_vote1, "climateRequirement", vote)
		UpdateVote1(cypher, climate[1], climate_vote2, "climateRequirement", vote)
	else:
		UpdateVote1(cypher, climate[0], climate_vote1, "climateRequirement", vote)
		UpdateVote1(cypher, climate[0], climate_vote2, "climateRequirement", vote)
	
	# filter on the basis of soil
	if len(soil) == 2:
		UpdateVote1(cypher, soil[0], soil_vote1, "soilRequirement", vote)
		UpdateVote1(cypher, soil[1], soil_vote2, "soilRequirement", vote)
	else:
		UpdateVote1(cypher, soil[0], soil_vote1, "soilRequirement", vote)
		UpdateVote1(cypher, soil[0], soil_vote2, "soilRequirement", vote)
	
	# filter on the basis of temperature

	if temperature == "":
		try:
			url = 'http://api.openweathermap.org/data/2.5/weather?q='+city+',IN&APPID='+API_key
			r = requests.get(url)
			a = r.json()
			if(a['cod'] == '404'):
				url = 'http://api.openweathermap.org/data/2.5/weather?q='+states_FF[state_name]+',IN&APPID='+API_key 
				r = requests.get(url)
				a = r.json()
			tp = a['main']
			temperature = str(int(tp['temp']) - 273)
		except:
			temperature = '28'
		if(temperature != '28'):
			print("Today's temperature in C : ", temperature)
	req = int(temperature)
	UpdateVote2(cypher, temp_vote, "temperatureRequirement", vote, req)

	# filter on the basis of rainfall
	req = int(rainfall)
	UpdateVote2(cypher, rain_vote, "rainfallRequirement", vote, req)

	#final vote
	print("Final_votes :")
	final_vote = OrderedDict(sorted(vote.items(), key=lambda item: item[1],reverse=True))
	data = {}
	iter = 0
	for i in final_vote:
		print(i + " : " + str(round(final_vote[i],1)))
		if iter < 7:
			name_vote_Array = []
			name_vote_Array.append(i)
			name_vote_Array.append(str(round(final_vote[i],1)))
			data[iter] = name_vote_Array
		iter = iter + 1
	data['len'] = 7
	print("Higher votes recommended\n")
	print(data)
	return JsonResponse(data)