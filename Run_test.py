
# coding: utf-8

# In[ ]:



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



path [0, 7, 5, 8, 1, 2, 6, 3, 9, 4, 0] incumbent 5.179893431317443
2.020004955912092 path cost
1.51387122195219 path cost
4.90197525369645 possible incumbent
[0, 7, 1, 5, 9, 4, 3, 2, 6, 8, 0] possible path
1.8991116896150342 path cost
2.8077121112744026 path cost
3.614263960289944 path cost
3.658403632388306 path cost
4.054066749091475 path cost
4.900909217384384 path cost

execution_time

0.03816308599925833

see

(4.90197525369645, [0, 7, 1, 5, 9, 4, 3, 2, 6, 8, 0])

