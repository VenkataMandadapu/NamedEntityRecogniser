import csv
import random
import math
import operator

def load(trainingset, testset):
	with open('dataset.csv','rb') as dataset:
		lines= csv.reader(dataset)
		hello = list(lines)
		for x in range(len(hello)-1):
			trainingset.append(hello[x])

def myRange(start,end,step):
	while start<=end:
		yield start
		start+=step

def add(case,h,word,l,count):
	y=0
	for x in range(len(case)):
		y=y+1
	
	word[l] = word[l] + '-'
	word[l] = word[l] + h
	
	total = count
	
	print word[l]
	
	return total
		
def response(neighbor,instance2,case,word,l,count):
	vote = [0,0,0]
	
	for x in range(len(neighbor)):
		if(neighbor[x][11]=='N'):
			vote[0] = vote[0]+1
		elif(neighbor[x][11]=='O'):
			vote[1] = vote[1]+1
		elif(neighbor[x][11]=='L'):
			vote[2] = vote[2]+1
	
	for x in range(3):
		if(vote[x]>=3):
			if(x==0):
				instance2[11]='N'
				total = add(case,'N',word,l,count)
			elif(x==1):
				instance2[11]='O'
				total = add(case,'O',word,l,count)
			elif(x==2):
				instance2[11]='L'
				total = add(case,'L',word,l,count)
				
			
	return total		
		
def distance(instance1,instance2):
	dist=0
	for x in myRange(1,10,1):
		dist = dist + pow((int(instance1[x])-instance2[x]),2)
		
	return dist

def neighbor(instance2,trainingset,case,word,l,count):
	complete =[]
	for x in range(len(trainingset)-1):
		dist = distance(trainingset[x],instance2)
		complete.append((trainingset[x],dist))
	complete.sort(key=operator.itemgetter(1))

	neighbor = []

	for x in range(5):
		neighbor.append(complete[x][0])
	
	count = response(neighbor,instance2,case,word,l,count)

	return count	
		
def found(word,trainingset):
	p = 'n'
	for x in range(len(trainingset)-1):
		test = (trainingset[x][0]).lower()
		if(word==test):
			p = trainingset[x][11]
	
	return p
	
#K-nearest neighbors classifier. classified words into Person, organization or location.
def knn(cases,word,l,trainingset,total):
	count = 0
	instan = [cases,0,0,0,0,0,0,0,0,0,0,'n']
	next = 'n'
	j = 1
	prev = word[l-1]
	if l < (len(word)-1):
		next = word[l+1]
		
	if(cases[0].isupper() == True):
		instan[2]=1
		
	case = cases.lower()
	prev = prev.lower()
	next = next.lower()

	m=found(case,trainingset)
	if(m=='N'):
		instan[3]=1
		
	elif(m=='O'):
		instan[7]=1
		
	elif(m=='L'):
		instan[10]=1
		
	
	if prev=='mr' or prev=='mrs' or prev=='dr' or prev=='sir' or prev=='president' or prev == 'mayor' or prev == 'governor' or prev == 'pm':
		instan[1]=1
	
	elif next=='manager' or next == 'doctor' or next == 'ceo' or next == 'cmd' or prev == 'actor ' or prev == 'ceo' :
		instan[4]=1
		print case
	
	elif next=='phd' or next == 'mba' or next == 'engineer' :
		instan[5]=1
	
	elif next =='org' or next =='ltd' or next=='co' or next=='inc' or next=='square' or next == 'garden' :
		instan[6]=1
		
	elif next == 'street' or next =='avenue' or next =='river' :
		instan[8]=1
		
	elif next == 'city' or next =='boulevard' or next == 'park':
		instan[9]=1
	
	for x in myRange(1,10,1):
		if instan[x]==1:
			count = count+1
	
	if count>=2:
		total = total + 1
		total = neighbor(instan,trainingset,case,word,l,total)

	return total	

def tag(case):
	y=0
	b = 'p'
	
	for x in range(len(case)):
		y=y+1
	if (case[y-2] == '-'):
		b = case[y-1].upper()
		
	return b
	
def modify(case,n,t):
	instan = [case,0,0,0,0,0,0,0,0,0,0,n]
	p=0
	q=0
	f=0
	if t==1:
		instan[2]=1
		
	if(n=='N'):
		instan[3]=1
	elif(n=='O'):
		instan[7]=1
	elif(n=='L'):
		instan[10]=1

	with open('dataset.csv', 'a') as f:
		writer = csv.writer(f)
		writer.writerows([instan])	
		
		
	
		
def patternMatching(case,word,l,count):	
	t=0
		
	if(case[0].isupper()== True):
		t=1
	
	case = case.lower()

	for x in range(len(word)):
		word[x] = word[x].lower()	
	
	if (l+2)<=(len(word)-1) and word[l+1]=='earned' and (word[l+2]=='money' or word[l+2]=='rs' or word[l+2]=='$') and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'N',word,l,count)
		modify(case,'N',t)
		print case
	
	elif (l+2)<=(len(word)-1) and word[l+1]=='joined' and tag(word[l+2])=='O' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'N',word,l,count)
		print case
		
	elif (l-2)>=0 and word[l-1]=='joined' and tag(word[l-2])=='N' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'O',word,l,count)
		modify(case,'O',t)
		print case
	
	elif (l+2)<=(len(word)-1) and word[l+1]==',' and (word[l+2]=='manager' or word[l+2]=='ceo' or word[l+2]=='cmd' or word[l+2]=='cfo' or word[l+2]=='coo') and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'N',word,l,count)
		modify(case,'N',t)
		print case
		
	elif (l+3)<=(len(word)-1) and word[l+1]=='fly' and word[l+2]=='to' and tag(word[l+3])=='L' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'N',word,l,count)
		modify(case,'N',t)
		print case 
		
	elif (l-2)>=0 and word[l-1]=='to' and word[l-2]=='fly' and tag(word[l-2])=='N' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'L',word,l,count)
		modify(case,'L',t)
		print case
	
	elif (l+3)<=(len(word)-1) and word[l+1]=='works' and (word[l+2]=='for' or word[l+2]=='at') and tag(word[l+3])=='O' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'N',word,l,count)
		modify(case,'N',t)
		print case
		
	elif (l-2)>=0 and (word[l-1]=='at' or word[l-1]=='for') and word[l-2]=='works' and tag(word[l-2])=='N' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'O',word,l,count)
		modify(case,'O',t)
		print case
	
	elif (l+1)<=(len(word)-1) and tag(word[l-1])=='N' and t==1 and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'N',word,l,count)
		modify(case,'N',t)
		print case	

	elif (l+3)<=(len(word)-1) and (word[l+1]=='lived' or word[l+1]=='lives' or word[l+1]=='stays') and (word[l+2]=='in' or word[l+2]=='at') and tag(word[l+3])=='L' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'N',word,l,count)
		modify(case,'N',t)
		print case		
		
	elif (l-3)>=0 and (word[l-2]=='lived' or word[l-2]=='lives' or word[l-2]=='stays') and (word[l-1]=='in' or word[l-1]=='at') and tag(word[l-3])=='N' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'L',word,l,count)
		modify(case,'N',t)
		print case
	
	elif (l+2)<=(len(word)-1) and word[l+1]=='headquarters' and tag(word[l+2])=='L' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'O',word,l,count)
		modify(case,'O',t)
		print case
		
	elif (l-2)>=0 and word[l-1]=='headquarters' and tag(word[l-2])=='O' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'L',word,l,count)
		modify(case,'L',t)
		print case

	elif (l+3)<=(len(word)-1) and (word[l+1]=='opened' or word[l+1]=='started') and word[l+2]=='at' and tag(word[l+3])=='L' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'O',word,l,count)
		modify(case,'O',t)
		print case 

	elif (l-3)>=0 and (word[l-2]=='opened' or word[l-2]=='started') and word[l-1]=='at' and tag(word[l-3])=='O' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'N',word,l,count)
		modify(case,'N',t)
		print case

	elif (l+2)<=(len(word)-1) and (word[l+1]=='beats' or word[l+1]=='defeated' or word[l+1]=='destroted') and tag(word[l+2])=='L' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'L',word,l,count)
		modify(case,'L',t)
		print case

	elif (l-2)>=0 and (word[l-1]=='beats' or word[l-1]=='defeated' or word[l-1]=='destroted') and tag(word[l-2])=='L' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'L',word,l,count)
		modify(case,'L',t)
		print case	
		
	elif (l+3)<=(len(word)-1) and (word[l+1]=='ceo' or word[l+1]=='cmd' or word[l+1]=='cfo' or word[l+1]=='coo' or word[l+1]== 'owner') and word[l+2]=='of' and tag(word[l+3])=='O' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'N',word,l,count)
		modify(case,'N',t)
		print case 	
		
	elif (l-3)>=0 and (word[l-2]=='ceo' or word[l-2]=='cmd' or word[l-2]=='cfo' or word[l-2]=='coo' or word[l-2]=='owner') and word[l-1]=='of' and tag(word[l-3])=='N' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'O',word,l,count)
		modify(case,'O',t)
		print case
		
	elif (l-2)>=0 and (word[l-1] == 'in' or word[l-1] == 'at') and tag(word[l-2])=='N' and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'L',word,l,count)
		modify(case,'L',t)
		print case

	elif (l+2)<=(len(word)-1) and (word[l+1] == 'in' or word[l+1] == 'at') and tag(word[l+2])=='L' and t == 1 and ( tag(word[l]) != 'N' and tag(word[l]) != 'L' and tag(word[l]) != 'O' ):
		count = add(case,'N',word,l,count)
		modify(case,'N',t)
		print case	
		
	return count	
		
		
		
def tweet(tweet,trainingset,count):
	word = []
	word = tweet.split()
	words = tweet.split()

	for x in range(len(word)):
		count = knn(word[x],word,x,trainingset,count)
		
	for x in range(len(word)):
		count = patternMatching(words[x],word,x,count)
		
	return count	
	
def main():
	trainingset = []
	testset = []
	load(trainingset, testset)
	
	targetFile = open('processed_tweets1.txt','r')
	
	count = 0
	
	for line in targetFile:
		count = tweet(line,trainingset,count)
		
	print count	
	
		
main()		
