# Traveling-Salesman-Branch-and-Bound
 
       Solving the Traveling Salesman problem can be useful across most areas of business .  It could find the best distance to 
build factories to have the minimum distance between distribution centers needed to travel to, saving on gas and drivers for trucks.
The distance between circuits on a circuit board could be found to minimize travel time, also the travel times for a city
subway.  The math behind this problem is not hard to do as long as the distances between points or the separate paths to each
of the points are known.  The most difficult aspects of this problem are checking that a solution is optimal, and the amount 
of time that it takes to do so.  Depending on how many locations need to be visited the problem could be solved in a few seconds to
a few days.  Using the Branch and Bound method and through the process of reducing the matrices the problem was solved.  The path 
needs to be traveled once to have a base incumbent value and path.  After traversed the path costs for each node which are less than
the first path cost are saved.  These path costs are then searched.  At any point if the following values from the saved costs
exceed the value of the incumbent those nodes aren't searched.  If the searches yields a smaller incumbent value then that value
takes the place of the incumbent.  And so on.  The backtracking function uses recursion to find the minimum path cost based on 
those conditions.  

```
start=perf_counter()
        
n=path_test(matrix_to_submit,start,visited_test,nv,mn,tv)

if len(n[2])<g:
    while len(n[2])<g:
        n=path_test((n[0]),(n[1]),(n[2]),(n[3]),
                    (n[4]),(n[5]))
b=full_spread(n)

incumbent_value=b[1]
incumbent_path=b[2]
test=search_tree(b,incumbent_value)


print("path",incumbent_path,"incumbent",incumbent_value)
see=b_track(test,incumbent_value,incumbent_path)
    
end=perf_counter()

execution_time=end-start

path [0, 6, 1, 4, 5, 9, 3, 8, 2, 7, 0] incumbent 46374.93894019773
1.7910129668272092 path cost
4.6670471133412095 possible incumbent
[0, 1, 4, 5, 9, 3, 8, 6, 2, 7, 0] possible path
2.784232575018332 path cost
2.891533780525485 path cost
3.0695422249127793 path cost
3.15106393905938 path cost
3.7424467662696794 path cost
3.8791948666974307 path cost

execution_time

0.03816308599925833

see

(4.90197525369645, [0, 7, 1, 5, 9, 4, 3, 2, 6, 8, 0])
```
The incumbent path is shown first for comparison.  Each path cost at each node that was searched is next shown followed
by "path cost".  When the function finds a better optimal path, the possible incumbent cost and possible path are then 
shown.  This example uses a random complete matrix of distances for display purposes.  For a larger matrix for 100 possible
locations the time increases.  The ten nodes took 0.03816308599925833 seconds.  To save space the call for a 100 node matrix
is shown and only the time will be shown:

```
test=np.inf

a=np.random.rand(100,100)
for i in range(0,100):
    a[i,i]=np.inf
        
A=cp.deepcopy(a)
nv=[]
mn=[]
visited_at=[]
tv=[]

execution_time

882.6312637529991

```
882.6312637529991 seconds!  Or 14.710521062549985 minutes.  With optimization like this there is always a worst-case scenario where 
the values might all be close in value to each other therefore causing a very long and complex search.  Run-times can be fine
tuned to obtain a faster time.
