import re
from random import choice
from itertools import product
from Levenshtein import distance

def preprocessing():
	file = open('words.txt')
	words = file.readlines()
	file.close()
	words = [word.strip() for word in words]
	dict_words = {}
	for word in words:
		if len(word) not in dict_words:
			dict_words[len(word)] = [word]
		else:
			dict_words[len(word)] += [word]
	
	return dict_words

def make_string(*args):
	if type(args[0]) != list:
		if len(args) == 1:
			return args[0]
	else:
		args = args[0]
	
	args = list(args)
	set_a = args.pop(0)
	if type(args[0][0]) == list:
		args = [arg for arg in args[0]]
	
	set_b = args.pop(0)
	strings = []
	for item in product(set_a, set_b):
		strings += [''.join(item)]
	
	if args != []:
		args = [strings] + args
		return make_string(args)
	else:
		return strings

def frequency(word_list):
	n = len(word_list[0])
	frequencies = {}
	for word in word_list:
		for i in range(n):
			if word[i] not in frequencies:
				frequencies[word[i]] = [0 for i in range(n)]
			
			frequencies[word[i]][i] += 1
	
	return frequencies

def initial_guess(word_list, letters = 5):
	n = len(word_list[0])
	frequencies = frequency(word_list)
	args = []
	for i in range(n):
		aux = []
		for key, value in frequencies.items():
			aux += [[key, value[i]]]
		
		aux.sort(reverse = True, key = lambda x : x[1])
		args += [[]]
		for j in range(min(letters, len(aux))):
			args[-1] += [aux[j][0]]
			
	return make_string(args)

def choose_word(word_list, have = [], not_have = [' '], form = None):
	if form == None:
		n = str(len(word_list[0]))
		form = '\S{' + n + '}'
	
	suggests = []
	word_list = [word for word in re.findall(form, ' '.join(word_list))]
	if word_list == []:
		return None
	
	if ' ' not in not_have:
		not_have.append(' ')
	
	for word in word_list:
		out = False
		for letter in have:
			if letter not in word:
				out = True
		
		for letter in not_have:
			if letter in word:
				out = True
		
		if not out:
			suggests += [word]
	
	if suggests == []:
		return None
	
	return choice(suggests)

def play():
	n = int(input('How many letters have the word?\n'))
	t = int(input('How many turns do you have?\n'))
	words = preprocessing()
	words = words[n]
	turns = 0
	have = []
	not_have = []
	form = '.' * n
	while turns < t:
		if turns == 0:
			guess = choice(words)
		else:
			guess = choose_word(word_list, have = have, not_have = not_have, form = form)
		
		print()
		print(f'My guess is the word: {guess}')
		print()
		for pos, letter in enumerate(guess):
			ans = input(f'The letter {letter} is in the secret word? [y/n]\n').lower()
			if ans.startswith('n'):
				not_have.append(letter)
			else:
				have.append(letter)
				ans = input('Is this letter in its real position? [y/n]\n')
				if ans.startswith('y'):
					form = form[:pos] + letter + form[pos + 1:]
		
		if '.' not in form:
			return form

play()
