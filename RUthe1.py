import random
import time
NUM_ROUNDS = 10
NUM_COUPLES = 10
COMPUTE_ALL = 3000
SAMPLE_SIZE = 500


#inputs a list and returns a list of lists corresponding 
#to every possible permutation of elements in the original list. Uses Recursion
def enumerate_perms(lst):
	if len(lst) == 1:
		return [lst]
	perms = []	
	for x in lst:
		newlst = [y for y in lst if y != x]
		sub_perms = enumerate_perms(newlst)
		for sp in sub_perms:
			perms.append([x] + sp)
	return perms

#computes hamming distance between two lists. Must be the same length
def distance(lst1, lst2):
	if(len(lst1) != len(lst2)):
		return -1
	count = 0	
	for i in range(len(lst1)):
		if lst1[i] != lst2[i]:
			count = count + 1
	return count

#inputs a list of possible matches and returns a pair that is true in half of all matches (or as close to that as possible)
def find_best_pair(matches):
	#generate a matrix whose ijth entry is the 'probability' that
	#man i is paried with woman j. (The number of still viable matches where i and j are paired)
	prob_matrix = [[0] * NUM_COUPLES for _ in range(NUM_COUPLES)]

	for match in matches:
		for i in range(len(match)):
			prob_matrix[i][match[i]] += 1

	#iterate through all pairs and see which one's probability is closest to 50%
	half = len(matches)/2
	best = (0,0, abs(prob_matrix[0][0] - half))
	

	for i in range(NUM_COUPLES):
		for j in range(NUM_COUPLES):
			if abs(prob_matrix[i][j] - half) < best[2]:
				best = (i,j,abs(prob_matrix[i][j] - half))
	return (best[0],best[1])

#given a list of hamming distances, computes the expected number of outcomes that are ruled out
def expected_cut(lst):
	total = sum(lst)*1.0
	xc = 0
	for x in lst:
		xc += (x/total)*(total - x)
	return xc


#For a given matching, we can compute the expected amount of information guessing it  
#would produce by comparing its hamming distance to other viable outcomes then taking expected value
#This function does that. If the number of mathces is sufficeintly small, it finds the best guess
#if the number of matches is too large, it takes a random sample and chooses the best
def find_best_attempt(matches):	
	best = (0, -1)

	#do whole computation if len < COMPUTE_ALL
	if(len(matches) < COMPUTE_ALL):
		for match in matches:
			distances = [0]*(NUM_COUPLES+1)
			for match_2 in matches:
				distances[distance(match,match_2)] += 1
			ec = expected_cut(distances)
			if ec > best[1]:
				best = (match, ec)
		return best[0]

	#take best of SAMPLE_SIZE random samples if len >= COMPUTE_ALL	
	for i in range(SAMPLE_SIZE):
		match = random.choice(matches)
		distances = [0]*(NUM_COUPLES+1)
		for j in range(SAMPLE_SIZE):
			match_2 = random.choice(matches)
			distances[distance(match,match_2)] += 1
		ec = expected_cut(distances)
		if ec > best[1]:
			best = (match, ec)
	return best[0]

#In the second round of truth-booth the information given so far is so low and the number of options
# is so high that I wrote a second function to enumerate all possibilities
#matches is the list of viable options
#tb is a bool indicating whether or not the first truth booth guess was successful
#mc is an int indicating how many guesses in the first round were correct
#attempt0 is a list describing what the first guess was 
def round_2_pair(matches, tb, mc, attempt0):
	#don't do computations on round 2

	if tb: #we got lucky and solved 0
		if mc == 1: #nothing in round 1 attempt is true
			return (1, matches[0][1])

		else: #something in round 1 attempt is true
			#take tb guess from second couple in round 1 attempt
			return (1,attempt0[1])

	else: #first guess did not work
		if mc == 0: #first matching was all wrong
			#any tb is okay
			return (0, matches[0][0])
			
		elif mc == 1:# One pair was right in the matching
			#any tb is okay
			return (0, matches[0][0])
			
		else: #More than one pair was right in the matching
			#guess a pair from our round 1 matching attempt
			return (0, attempt0[0])


#A function that takes a fixed solution, and a list of viable matches, and tries solving
#Used for statistically showing how often this program works
def solve(solution, matches):
	#don't do computations on round 1

	#check arbitrary pair in truth booth
	tb = solution[0] == 0
	matches_temp = []
	for match in matches:
		if (match[0] == 0) == tb:
			matches_temp.append(match)
	matches = matches_temp

	#matching ceremony, again random
	attempt = matches[0]
	matches_temp = []
	mc = distance(attempt, solution)
	for match in matches:
		if distance(match, attempt) == mc:
			matches_temp.append(match)
	matches = matches_temp

	#print("After 1 round there are " + str(len(matches)) + " options")

	bp = round_2_pair(matches, tb, mc, attempt)
	tb = solution[bp[0]] == bp[1]
	matches_temp = []
	for match in matches:
		if (match[bp[0]] == bp[1]) == tb:
			matches_temp.append(match)
	matches = matches_temp

	attempt = matches[0]
	matches_temp = []
	mc = distance(attempt, solution)
	for match in matches:
		if distance(match, attempt) == mc:
			matches_temp.append(match)
	matches = matches_temp	


	#print("After Round 2 there are " + str(len(matches)) +" options")

	count = 3
	while(len(matches) > 1):
		bp = find_best_pair(matches)
		tb = solution[bp[0]] == bp[1]
		matches_temp = []
		for match in matches:
			if (match[bp[0]] == bp[1]) == tb:
				matches_temp.append(match)
		matches = matches_temp		

		attempt = find_best_attempt(matches)
		matches_temp = []
		mc = distance(attempt, solution)
		if mc == 0:
			break
		for match in matches:
			if distance(match, attempt) == mc:
				matches_temp.append(match)
		matches = matches_temp
		#print("After Round " + str(count) + " there are " + str(len(matches)) +" options")
		count += 1
		
	#print("Rounds needed: " + str(count))
	return count

#runs the solving algorithm for *number* couples a total of *trials* times
def check_accuracy(number, trials):
	lst = range(number)
	matches = enumerate_perms(range(number))
	overall = [0]*15
	for i in range(trials):
		random.shuffle(lst)
		#start = time.time()
		s = solve(lst, matches)
		#end = time.time()
		if s< 15:
			overall[s-2] += 1
		else:
			overall[-1] += 1
		#print("Time elapsed: " + str(end-start))

	print("OVERALL STATISTICS:")
	for i in range(2,16):
		print("The process terminated in " + str(i) + " rounds " + str(overall[i-2]))
	print("The process took more than 16 steps " + str(overall[-1]) + " time(s)")

def pretty_print_attempt(attempt):
	string = ""
	for i in range(len(attempt)):
		string += str( (i, attempt[i])) + "  "
	return string

#after receiving an answer from the truth booth, remove all pairings that can't be true
#matches = list of viable matches, a list of lists of ints
#bp = pair that was guessed, a 2-tuple of ints
#tb = Was the guesss correct? A bool
def tb_reduce(matches, bp, tb):
	matches_temp = []
	for match in matches:
		if (match[bp[0]] == bp[1]) == tb:
			matches_temp.append(match)
	return matches_temp

#after receiving an answer from the truth booth, remove all pairings that can't be true
#matches = list of viable matches, a list of lists of ints
#attempt = the last guess, a list of ints
#d = number of correct guesses
def mc_reduce(matches, attempt, d):
	matches_temp = []
	for match in matches:
		if distance(match, attempt) == d:
			matches_temp.append(match)
	return matches_temp


#runs an interactive mode where the user can make a guess and the computer solves it
def interactive(number):
	print("Welcome to 'ARE YOU THE ONE?' solver")
	print("Please wait while program loads")
	matches = enumerate_perms(range(number))
	#print(pretty_print_attempt(perms[-1]))
	print("Please create a pairing, with the men and women numbered 0 through " + str(NUM_COUPLES-1))
	print("----------------------")

	bp = (0, matches[0][0])
	print("Round 1 Truth Booth: " + str(bp) )

	tb = input("0 for no, 1 for yes: ")
	matches = tb_reduce(matches, bp, tb)

	attempt1 = matches[0]
	print("Round 1 Matching ceremony: " + pretty_print_attempt(attempt1))
	d = NUM_COUPLES - input("How many are correct?   ")
	matches = mc_reduce(matches, attempt1, d)

	#round 2

	bp = round_2_pair(matches, tb, d, attempt1)
	print("Round 2 Truth Booth: " + str(bp))
	tb = input("0 for no, 1 for yes:  ")
	matches = tb_reduce(matches, bp, tb)

	attempt2 = matches[0]
	print("Round 1 Matching ceremony: " + pretty_print_attempt(attempt2))
	d = NUM_COUPLES - input("How many are correct?   ")
	matches = mc_reduce(matches, attempt2, d)

	round_number = 3
	while(len(matches) > 1):
		bp = find_best_pair(matches)
		print("Round " + str(round_number) + " Truth Booth: " + str(bp))
		tb = input("0 for no, 1 for yes:  ")
		matches = tb_reduce(matches, bp, tb)

		attempt = find_best_attempt(matches)
		print("Round " + str(round_number) + " Matching ceremony: " + pretty_print_attempt(attempt))
		d = NUM_COUPLES - input("How many are correct?   ")
		matches = mc_reduce(matches, attempt, d)
		if d == 0:
			break
		round_number += 1

	print("The answer is " + pretty_print_attempt(matches[0]))

	print("FINISHED, I took " + str(round_number) + " rounds!")

if __name__ == '__main__':
	interactive(NUM_COUPLES)	
























