from itertools import permutations
from random import randint
from math import sqrt
from copy import deepcopy
from time import time

#helper functions
def euclid_dist(a,b):
	return sqrt((b[1] - a[1])**2+(b[0]-a[0])**2)

def route_dist(points):
        dist = 0
        for i in range(1,len(points)):
                dist += euclid_dist(points[i-1], points[i])
        return dist

def point_generator(n): #generates n random points, from (0,0) to (99,99)
        return [(randint(0,99),randint(0,99)) for x in range(n)]

#TSP functions. Returns in the format (route, length of route, time taken to compute)
#input format: <list of points in the tuple format (x,y)>, <start point in format (x,y)>
def bruteforce_TSP(points, start): #recommended max size of points is 10
        start_t = time()
        combine = lambda x: [start]+list(x)
        perms = list(map(combine, permutations(points))) 

        min_r = perms[0]                
        for perm in perms[1:]:
                if route_dist(perm) < route_dist(min_r):
                        min_r = perm
        stop_t = time()
        return (min_r, round(route_dist(min_r),2),stop_t-start_t)

def nearest_n_TSP(points, start):
        start_t = time()
        point_lst = deepcopy(points)
        route = [start]

        while point_lst != []:
                d = lambda x: euclid_dist(route[-1], x)
                distances = list(map(d, point_lst))
                min_i = distances.index(min(distances))
                route.append(point_lst.pop(min_i))

        stop_t = time()
        return route, round(route_dist(route),2),stop_t-start_t

        
#todo: visualise?
#todo: optimise python parts
#todo: implement approximation algos
