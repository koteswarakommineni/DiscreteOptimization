#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import ceil
from collections import namedtuple
import sys
Item = namedtuple("Item", ['index', 'value', 'weight'])
#haschanged = False
notchanged = 0
maxiterations = 1000000

def get_upperbound(items, k):
	capacity = k
	upperbound = 0
	sortedItems = sorted(items, key=lambda item: (item.value/item.weight), reverse=True)
	#print(sortedItems)
	itemcount = 0
	for item in sortedItems:
		#print("Capacity: {0}, Weight: {1}, Upperbound: {2}".format(capacity, item.weight, upperbound))
		if item.weight <= capacity:
			upperbound += item.value
			capacity -= item.weight
			itemcount += 1
		else:
			break
		
	#print("Capacity After For Loop: {0}, Item: {1}".format(capacity, sortedItems[itemcount]))
	if capacity > 0 and itemcount < len(items):
		upperbound += ceil((sortedItems[itemcount].value * capacity)/sortedItems[itemcount].weight)

	return upperbound

def depthfirst_search(currentvalue, currentcombination, maxcombination, items, capacity, upperbound):
	# items - list of items to choose for the knapsack
	# capacity - Capacity
	#print("depthfirst level: " + str(len(items)))
	#print("CurrentValue: {0}, MaxCombination: {1}, Capacity: {2}, UpperBound: {3}, Items: {4}".format(currentvalue, maxcombination, capacity, upperbound, items))
	global notchanged
	global maxiterations

	#print("Notchanged: {0}".format(notchanged))
	item = items[0]
	if len(items) is 1:
		#for i in items:
		#	print(i)
		if item.weight <= capacity:
			#print("Chosen Item: {0}".format(items[0].index+1))
			if maxcombination[0] < currentvalue + item.value:
				maxcombination = (currentvalue+item.value, currentcombination + [1])
				notchanged = 0
			else:
				notchanged += 1
		return maxcombination
	else:
		#print(len(items))
		#for i in items:
		#	print(i)``

			#print(str(item.value / item.weight) + " --> (" + str(item.value) + ", " + str(item.weight) + ") --> Pending Capacity: " + str(capacity))
		if maxcombination[0] < currentvalue:
			maxcombination = (currentvalue, currentcombination)
			notchanged = 0
		else:
			notchanged += 1

		if any(x.weight <= capacity for x in items):
			if item.weight <= capacity:
				#print("Chosen Item: {0}".format(item.index+1))
				#print("Selecting {0}. linearrelaxation: {1}, maxvalue: {2}".format(item.index, linearrelaxation, maxcombination[0]))
				(chosenvalue, chosentaken) = depthfirst_search(currentvalue + item.value, currentcombination + [1], maxcombination, items[1:], capacity-item.weight, upperbound)
				#print(maxcombination)
				if maxcombination[0] < chosenvalue:
					maxcombination = (chosenvalue, chosentaken)

			excludedupperbound = get_upperbound(items[1:], capacity)
			if excludedupperbound + currentvalue > maxcombination[0]:
				#print("Not Chosen Item: {0}".format(item.index+1))
				#print("Not Selecting {0}. linearrelaxation: {1}, maxvalue: {2}".format(item.index, linearrelaxation, maxcombination[0]))
				(nonchosenvalue, nonchosentaken) = depthfirst_search(currentvalue, currentcombination + [0], maxcombination, items[1:], capacity, excludedupperbound)
				#print("Value: {0}, Choices: {1}".format(nonchosenvalue, nonchosentaken))
				if maxcombination[0] < nonchosenvalue:
					maxcombination = (nonchosenvalue, nonchosentaken)
					notchanged = 0
				else:
					notchanged += 1
			#print(maxcombination)
			return maxcombination
		else:
			return maxcombination

def solve_it(input_data):
	sys.setrecursionlimit(20000)
    # Modify this code to run your optimization algorithm
	global notchanged
	global maxiterations
    # parse the input
	lines = input_data.split('\n')

	firstLine = lines[0].split()
	item_count = int(firstLine[0])
	capacity = int(firstLine[1])

	items = []

	for i in range(1, item_count+1):
	    line = lines[i]
	    parts = line.split()
	    items.append(Item(i-1, int(parts[0]), int(parts[1])))

	# a trivial greedy algorithm for filling the knapsack
	# it takes items in-order until the knapsack is full
	#value = 0
	#weight = 0
	#taken = [0]*len(items)
	#sortedItems = sorted(items, key=lambda item: item.value/item.weight, reverse=True)
	#(linearrelaxation, linearconsidered) = get_linearrelaxation(items, capacity)
	upperbound = get_upperbound(items, capacity)
	#print("Upperbound: {0}".format(upperbound))
	#print(linearrelaxation)
	sortedItems = sorted(items, key=lambda item: (item.value/item.weight), reverse=True)
	(value, sortedtaken) = depthfirst_search(0, [], (0, []), sortedItems, capacity, upperbound)


	takenitemcount = len(sortedtaken)
	if takenitemcount < len(items):
		sortedtaken = sortedtaken + [0]*(len(items)-takenitemcount)
	itemcount = len(items)
	taken = [0] * itemcount

	for i in range(0, itemcount-1):
		if sortedtaken[i] is 1:
			taken[sortedItems[i].index] = 1

	#print("computed value: {0}".format(sum([i.value for i in items if taken[i.index] is 1])))
	'''
	pendingcapacity = capacity - sum(i.weight for i in items[:takenitemcount] if taken[i.index] is 1)
	if notchanged >= maxiterations or pendingcapacity > 0:
		pendingitems = [item for item in items if taken[item.index] is 0]
		pendingitemssorted = sorted(pendingitems, key=lambda item: item.weight)

		for item in pendingitemssorted:
			#print("Capacity: {0}, Weight: {1}, Upperbound: {2}".format(capacity, item.weight, upperbound))
			if item.weight <= pendingcapacity:
				value += item.value
				pendingcapacity -= item.weight
				taken[item.index] = 1
	'''
		#print("Pending Capacity: {0}, Least Weight: {1}".format(pendingcapacity, min([i.weight for i in pendingitemssorted if taken[i.index] is 0])))
	# prepare the solution in the specified output format
	output_data = str(value) + ' ' + str(1) + '\n'
	output_data += ' '.join(map(str, taken))
	return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
