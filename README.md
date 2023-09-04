# algorithm-analyses
A repository for analysing various types of algorithms done by three
friends.

lab2 contains runtime tests for "bad" sorts like selection and insertion sort
which are $O(n^2)$ runtime and for "good" sorts like quicksort and others which
have theoretical runtimes less than $O(n^2)$. Along with the basic algorithms
for the sorts, some improvements have been implemented into those algorithms
as new functions. 

lab4 contains tests for various graph data structures and algorithms, like depth-first 
search, path finding, and minimum vertex covers.

lab6 contains tests for trees, specifically an implementation of red-black trees and 
binary search trees along with their respective algorithms like searching and inserting.

labFinal contains a directed, weighted graph created using the London, England subway system.
The main algorithms here are the various path algorithms like Dijkstra's, Bellman-Ford,
and all sources, all paths.

In all files, there is testing code which compares runtimes between the various algorithms
and then graphs them using the matplotlib library. If you want to run any of these tests,
uncomment the testing code and wait (for some of them it may take a few minutes for the 
graphs to be generated).
