
# coding: utf-8

# In[ ]:


import numpy as np
import copy as cp

test=np.inf

a=np.random.rand(10,10)
for i in range(0,10):
    a[i,i]=np.inf
        
A=cp.deepcopy(a)
nv=[]
mn=[]
visited_at=[]
tv=[]


f,g=a.shape

def reduction_matrix_first(mate):
  
    ##Reduction of the matrix each time it is used.  
    ##The process is:
    
    ##Iterating over each row first to see if the row is all np.inf or if a zero exists.
    ##If not then the minimum row or column position is found and subtracted from 
    ##each position in the column.  The reason for the np.inf spots are that they will
    ##remain unchanged and will not be affected for each modification.  The np.inf spots
    ##are saved in a way implicityly.  Each time the row/column operation is performed
    ##that number is added to the total cost for that position or "node".  
    d,e=mate.shape
    number=0
    for i in range(0,e):
        d=mate[i]
        if not np.all(d==np.inf) and not np.any(d==0):
                in_answ=d[np.isfinite(d)].min()
                number+=in_answ
                mate[i]=mate[i]-in_answ
        
    for i in range (0,e):
        d=mate[:,i]
        if not np.all(d==np.inf) and not np.any(d==0):
                in_answ=d[np.isfinite(d)].min()
                number+=in_answ
                mate[:,i]=mate[:,i]-in_answ 
        
    return number

cost=reduction_matrix_first(a)

##Normally the "0" node is the starting position.  
a[0]=test
node_values=[]
matrices=np.zeros((g-1,g,g))
A=cp.deepcopy(a)
cost_spot=0
for i in range(1,g):
    A=cp.deepcopy(a)
    A[:,i]=np.inf
    cost_spot=A[i][0]
    A[i][0]=np.inf
    c=reduction_matrix_first(A)
    node_values.append(c+cost+cost_spot)
    matrices[i-1]=A

og_nodes=cp.deepcopy(node_values)    
og_nodes
visited_test=[]
visited_test.append(0)


visited_at.append(cp.deepcopy(visited_test))

##The minimum value is chosen to start our path on.  
##The corresponding node for that value is then added into the path for the first search.
spot=np.argmin(nv[0])
visited_test.append(tv[0][spot].pop())

matrix_to_submit=cp.deepcopy(matrices[spot])
matrix_to_submit[visited_test]=np.inf
start=np.min(nv[0])

def path_test(mate,val,visited,N,M,T):
    
    d,e=mate.shape
    ranges=list(range(0,d))
    
    matrix_to_test=np.zeros((e,e))
    
    node_val=[]
    
    ##Checking if nodes have been visited out of the mandatory length that the path
    ##will have to be.  
    j=np.isin(ranges,visited)

    cost_spot=0
    
    ##Matrices for the path.  Each matrix needs to be saved for the purpose of using to
    ##search on.  
    matrices=[None]*(e-len(visited))
    
    l=0
    
    for i in range(0,e):
        if not j[i]:
            ##The last node and the second to last nodes spots in the original matrix are also
            ##added to the cost each time for the node value chosen.
            cost_spot=a[visited[-1]][visited[-2]]
            ##A copy of the matrix is made so that it is not changed.  It is saved.  
            A=cp.deepcopy(mate)
            ##The spot of the matrix corresponding to the visited nodes is represented.
            A[visited]=np.inf
            A[:,i]=np.inf
            ##Cost spot is changed
            A[visited[-1]][visited[-2]]=np.inf
            c=reduction_matrix_first(A)
            ##The value of the path specific node is saved
            node_val.append(c+val+cost_spot)
            ##The searched matrix is saved into the grouping for the path search.
            matrices[l]=A
            l+=1
            
    value_check=np.inf
    nee=cp.deepcopy(visited)
    M.append(matrices)
    N.append(node_val)
    
    
    insertion_for_test_visited=[None]*(e-len(visited))
    
    for i in range(0,len(matrices)):
        inst=[]
        
        for m in range(0,len(nee)):
            inst.append(nee[m])
            
        j=np.isin(ranges,nee)
        
        for k in range(0,e):
            if not j[k]:
                dee=cp.deepcopy(matrices[i][:,k])
                if all(dee==np.inf):
                    inst.append(k)
                    
        insertion_for_test_visited[i]=cp.deepcopy(inst)
        
    T.append(insertion_for_test_visited)
                
    for i in range(0,len(node_val)):
        if value_check>node_val[i]:
            value_check=cp.deepcopy(node_val[i])
            matrix_to_test=cp.deepcopy(matrices[i])
        
    blocked_row_inf=[]
    
    for i in range(0,len(j)):
        if not j[i]:
            d=cp.deepcopy(matrix_to_test[:,i])
            if np.all(d==np.inf):
                blocked_row_inf.append(i)
                visited.append(i)
        
    matrix_to_test[blocked_row_inf]=np.inf
    
   ##If the nodes are on the last run of the search before going to base the base cost is added to the path cost.
    if len(visited)==e:
        value_check+=a[visited[-1]][visited[0]]
        visited.append(visited[0])
        
        
    return (matrix_to_test,value_check,visited,N,M,T)

##The purpose of this function is to search which possible path is optimal for the final node searches for one
##path search.
def full_spread(g):
    
    d,e=g[0].shape
    if len(g[2])<e:
        while len(g[2])<e:
            g=path_test(g[0],g[1],g[2],g[3],g[4],g[5])  

    check_position=np.argmax(g[3][-2])
    
    n=path_test(cp.deepcopy(g[4][-2][check_position]),cp.deepcopy(g[3][-2][check_position]),
                cp.deepcopy(g[5][-2][check_position]),cp.deepcopy(g[3]),
                cp.deepcopy(g[4]),cp.deepcopy(g[5]))
   
    if len(n[2])<e:
        while len(n[2])<e:
            n=path_test(cp.deepcopy(n[0]),cp.deepcopy(n[1]),cp.deepcopy(n[2]),cp.deepcopy(n[3]),
                        cp.deepcopy(n[4]),cp.deepcopy(n[5]))

  
    d=len(cp.deepcopy(g[4]))
    d_spot=d-1
    
    ##Depending on which path is chosen that will be deleted from the search.  
    if n[5][d_spot-2]>n[5][d_spot]:
        n[3].pop(-2)
        n[5].pop(-2)
        n[4][0:len(n[4][0])]=cp.deepcopy(np.delete(mn,d_spot-1,0))
        return (n[0],n[1],n[2],n[3],n[4],n[5])
    else:
        n[3].pop(-1)   
        n[5].pop(-1)
        n[4][0:len(n[4][0])]=cp.deepcopy(np.delete(mn,d_spot,0))
        return (g[0],g[1],g[2],g[3],g[4],g[5])
    
##The path is iterated over to find any possible branches that could be the start of a better path with a 
##minimum distance.
def search_tree(path_to_search,cost_val):
    newmat=[]
    newval=[]
    newvisit=[]

    d1=[None]*(len(path_to_search[3]))
    e1=[None]*(len(path_to_search[3]))
    f1=[None]*(len(path_to_search[3]))
    
    for j in range(0,len(path_to_search[3])):
    

        d=[None]*len(path_to_search[3][j])
        e=[None]*len(path_to_search[3][j])
        f=[None]*len(path_to_search[3][j])

        for i in range(0,len(path_to_search[3][j])):
            d[i]=path_to_search[3][j][i]
            e[i]=path_to_search[5][j][i]
            f[i]=path_to_search[4][j][i]
        
        d1[j]=d
        e1[j]=e
        f1[j]=f
    

    for j in range(0,len(d1)):
        
        inc=min(d1[j])
        
        for x in range(0,(len(d1[j]))):
            if d1[j][x]==inc:
                min_spot=x
                break
        d1[j].pop(min_spot)
        e1[j].pop(min_spot)
        f1[j].pop(min_spot)
       
    empty_spots=[]
    
    for j in range(0,len(d1)):
        if (len(d1[j])==0):
            empty_spots.append(j)
            
    d1.pop(empty_spots[0])
    e1.pop(empty_spots[0])
    f1.pop(empty_spots[0])
      
    if len(empty_spots)>1:
        for j in range(2,len(empty_spots)):
            d1.pop(empty_spots[j]-1)
            e1.pop(empty_spots[j]-1)
            f1.pop(empty_spots[j]-1)
            
    
        
    for i in range(0,len(d1)):
        deletes=[]
        for j in range(0,len(d1[i])):
            if (d1[i][j]>=cost_val):
                deletes.append(j)
        
        if len(deletes)>0:
            e1[i].pop(deletes[0])
            f1[i].pop(deletes[0])
            d1[i].pop(deletes[0])
        
        if len(deletes)>1:
            for x in range(2,len(deletes)):
                d1[i].pop(deletes[x]-1)
                e1[i].pop(deletes[x]-1)
                f1[i].pop(deletes[x]-1)  
                
        if len(deletes)>2:
            d1[i].pop(0)
            e1[i].pop(0)
            f1[i].pop(0)
            
    
    d1=[x for x in d1 if x!=[]]
    e1=[x for x in e1 if x!=[]]
    f1=[x for x in f1 if x!=[]]
    d=[]
    e=[]
    f=[]
    for i in range(0,len(d1)):
        d.append(d1[i])
        e.append(e1[i])
        f.append(f1[i])
        
    ##If no positions to search are found the function returns "optimal".  The path is the optimal path.  
    
    if len(d1)==0:
        return ("optimal")
    else:
        return (d,e,f)
    
def data_for_search(one,two,three,a):
    
    ##This function uses the nodes visited, the matrices of those nodes visited and the cost at that position, to
    ##begin a search.  This is after or if a position was found that could possibly be part of a more optimal
    ##path.  This puts it in the format to work with the rest of the program.
    
    bign=[]
    bigm=[]
    visited_at=[]
    bigt=[]
    d,e=three.shape
    
    node_values=[]
    matr=np.zeros((e-len(two),e,e))
    A=cp.deepcopy(three)
    cost_spot=0
    
    ranges=list(range(0,e))
    j=np.isin(ranges,two)
    l=0

    for i in range(0,e):
        if not j[i]:
            cost_spot=a[two[-1]][two[-2]]
            A=cp.deepcopy(three)
            A[two]=np.inf
            A[:,i]=np.inf
            A[two[-1]][two[-2]]=np.inf
            c=reduction_matrix_first(A)
            node_values.append(c+one+cost_spot)
            matr[l]=A
            l+=1

    og_nodes=cp.deepcopy(node_values)    
    
    visited_test=[]

    for k in range(0,len(two)):
        visited_test.append(two[k])


    visited_at.append(cp.deepcopy(visited_test))

    bigm.append(matr)
    bign.append(node_values)
    

    insertion_for_test_visited=[]

    insertion_for_test_visited=[None]*(e-len(two))

    for i in range(0,len(matr)):
            inst=[]
            for l in range(0,len(two)):
                inst.append(two[l])

            for k in range(0,e):
                if not j[k]:
                    if all(matr[i][:,k]==np.inf):
                        inst.append(k)
            insertion_for_test_visited[i]=inst

    bigt.append(insertion_for_test_visited)
    
    

    spot=np.argmin(bign[0])
    check=cp.deepcopy(bigt[0][spot])
    visited_test.append(check.pop())


    
    
    matrix_to_submit=cp.deepcopy(matr[spot])
    matrix_to_submit[visited_test]=np.inf
    start=np.min(bign[0])
    return (matrix_to_submit,start,visited_test,bign,bigm,bigt)

def b_track(data,inc,path):
    x,y=data[2][0][0].shape
    ##Iterating over each node that was found to possibly be optimal.  If the cost of the node is less than the
    ##searched paths total cost then the function completes the search from that node.  If it is more than the optimal
    ##paths cost, the function stops and isn't searched any longer and the function moves onto the next node.
    
    for i in range(0,len(data[0])):
        
        for j in range(0,len(data[0][i])):
        
                print(data[0][i][j],"path cost")
                gee=data_for_search(cp.deepcopy(data[0][i][j]),cp.deepcopy(data[1][i][j]),cp.deepcopy(data[2][i][j]),cp.deepcopy(a))
                #######################
                
                n=path_test(cp.deepcopy(gee[0]),cp.deepcopy(gee[1]),cp.deepcopy(gee[2]),cp.deepcopy(gee[3]),cp.deepcopy(gee[4]),cp.deepcopy(gee[5]))
                ##Full path search
                if len(n[2])<inc:
                    while len(n[2])<y and n[1]<inc: 
                        n=path_test(cp.deepcopy(n[0]),cp.deepcopy(n[1]),cp.deepcopy(n[2]),cp.deepcopy(n[3]),
                        cp.deepcopy(n[4]),cp.deepcopy(n[5]))
                    if n[1]>inc:
                        break
                
                else:
                    break
                 ########################   
                trying=full_spread(n)
                
                if trying[1]<inc:
                    inc=trying[1]
                    path=trying[2]
                    print(inc,"possible incumbent")
                    print(path,"possible path")
                    t=search_tree(trying,inc)
                    if t=="optimal":
                        return inc
                    else:
                        return b_track(t,inc,path)
                else:
                   
                    break
        
     
    return inc,path       

        


