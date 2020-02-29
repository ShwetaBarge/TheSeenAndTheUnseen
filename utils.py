import numpy as np
import math
import matplotlib.pyplot as plt
import statistics
import timeit
import copy



plt.style.use('seaborn-darkgrid')
#--------------------------------------------------------------------------------------------------------------
#Testing Function
def theSeenAndTheUnseenTest(func1, func2, testcase) :
    '''
    A generic testing function 
    Arguments:
        func1 is the function to be tested
        func2 is the inbuilt function
        testcase is a list of testcases 
    
    Output:
        Graph1: Output of func1 against testcases
        Graph2: Output of func2 against testcases
        Graph3: Error plot
    
    '''
    ourvalues = []
    actualvalues = []
    error = []
    failed= []
    
    # This loop stores the output of the defined function,
    # output of inbuilt function in lists, and calculates
    # error
    for i in testcase :
        o = (func1(i)[0])
        a = (func2(i))
        ourvalues.append(o)
        actualvalues.append(a)
        
        if a != 0:            #avoiding division by zero
            e = ((a-o)/a)*100
            error.append(e)   # error
        else:
            e = 0
            error.append(e)
        if e > 0.01 :
            failed.append(i);
            
    fig, ax = plt.subplots(1,3,figsize=(20,5))

    # 1st subplot - plots values of defined function
    ax[0].plot(testcase, ourvalues, color = 'red')
    ax[0].set_title(func1.__name__ + "()")
    ax[0].set_xlabel("testcases")

    # 2nd subplot - plots values of inbuilt function
    ax[1].plot(testcase, actualvalues)
    ax[1].set_title(func2.__name__+"()")
    ax[1].set_xlabel("testcases")

    # 3rd subplot - plots the error
    ax[2].plot(testcase, error)
    ax[2].set_title("error")
    avg_error = sum(error)/len(error)

    # Title when all testcases are passed
    if(avg_error < 0.01) :
        fig.suptitle("All test cases passed, Accuracy: "+str(100-abs(avg_error))+"%", fontsize = 12)
        ax[2].set_xlabel("Average Error : ", '%.2f'avg_error, " % \n < 0.01%")
        #ax[2].text(0.5, -0.17, "Average Error :" +str(avg_error)+ "% \n < 0.01%",size=12, ha="center", transform=ax[2].transAxes)
    
    # Title when not all testcases are passed
    else :
        fig.suptitle("Accuracy: "+str(100-avg_error), fontsize = 12)
        ax[2].text(0.5, -0.17, "Average Error :" + str(avg_error)+ "% \n > 0.01%",
                   size=12, ha="center", transform=ax[2].transAxes)
        print(failed)
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#Finds Computation time
def find_time(testcase, func):
    '''
    Finds the computation time of each
    testcase for the function - 'func'.
    Returns the computation time in 
    list - 'time[]'
    '''
    time = []
    for i in testcase:
        t = timeit.Timer("func(i)", globals={"func": func, "i": i})
        time.append(t.timeit(number = 7))
    return time

#Plots the list containing computation time
def plot_time(testcase,plotNaive, **kwargs):
    '''
    This function plots two graphs
    1. Runtime
    2. Speedup with respect to naive implementation
    
    plotNaive is a boolean variable 
    if plotNaive = True:
        plot runtime for naive in graph-1
    else :
        don't plot naive runtime
        
    **kwargs is a dictionary of tuples - (list of time, function)
    This will help me compare any number of functions
    '''
    
    legend_list = []                        #legend for graph 1 - runtime
    legend_list_speedup = []                #legend for graph 2 - speedup
    avg_time = []                           #average time for different functions
    fno = 0
    base_list = []                          #runtime of naive implementation or any function you want to calculate speedup against
    time_list = []                          #contains lists of runtime for different functions in kwargs
    
    #iterating through kwargs
    for key, value in kwargs.items():
        time_list.append(value[0])                     #value is tuple of (list of runtime for a function, function)      
        avg_time.append(statistics.mean(value[0]))
        legend_list.append(value[1].__name__+"()")
        
        if fno == 0:                                
            base = value[1]                            #storing naive for finding speedup
            base_list = copy.deepcopy(value[0])
        fno += 1
        
    #for plotting time of only one function
    if fno == 1:
        fig, ax = plt.subplots(1, 1, figsize = (5,5))
        ax.plot(testcase, time_list[0])
        ax.set_ylabel("time")
        ax.legend(legend_list)
        ax.set_title("Runtime") 
        xlabel = "$x$"
        for i in range(len(legend_list)):
            xlabel = xlabel + "\n avg time for "+legend_list[i]+": "+str(avg_time[i])
        ax.set_xlabel(xlabel)


    #for plotting time of multiple functions and their speedup compared to naive
    else:
        fig, ax = plt.subplots(1, 2, figsize = (12, 5))

        xlabel_runtime = "$x$"
        xlabel_speedup = "$x$"
        
        if plotNaive == False :
            start = 1                                   
        else:
            start = 0
        
        for i in range(start, len(time_list)):
            ax[0].plot(testcase, time_list[i])              #plotting runtime
            
            if i > 0:
                speedup = [round(b / m, 7) for b,m in zip(base_list, time_list[i])]     #calculating speedup
                ax[1].plot(testcase, speedup)                                           #plotting speedup
                xlabel_speedup = xlabel_speedup + "\n avg speedup for "+legend_list[i] + ": " +str(round(sum(speedup)/len(speedup), 4))

        for i in range(len(legend_list)):
            xlabel_runtime = xlabel_runtime + "\n avg time for "+legend_list[i]+": "+str(avg_time[i])        
                
        #labels for runtime plot
        ax[0].set_ylabel("time")                            
        ax[0].legend(legend_list[start:])
        ax[0].set_title("Runtime") 
        ax[0].set_xlabel(xlabel_runtime)
        
        #labels for speedup
        ax[1].set_title("Speedup with respect to " + base.__name__)                 
        ax[1].set_ylabel("Speedup")                                     
        ax[1].legend(legend_list[1:])
        ax[1].set_xlabel(xlabel_speedup)
#--------------------------------------------------------------------------------------------------------------     
    
#--------------------------------------------------------------------------------------------------------------
#Plots Terms in a series
def plot_term(terms, function, string) :
    '''
    This is a generic function
    arguments:
        terms - different values of x for which the terms will be calulated
        function - will return the n^(th) term
        string - shows a general reperesentation of the term
    the function calculates first 30
    5th term is rounded off to its 3rd decimal and highlighted in red
    '''
    l = []
    for x in terms :
        sl = []
        for i in range(0,30) :
            sl.append(function(x,i))
        l.append(sl)

    
    if len(l) == 1 :
        fig, ax = plt.subplots(1,1, figsize = (5,5))
        ax.plot(l[0]);
        ax.set_title(terms[0]);
        ax.set_ylabel(string);
        ax.set_xlabel('i');
    else:
        fig, ax = plt.subplots(1, len(l), figsize = (20,4))
        
        for i in range(0,len(l)) :
            ax[i].plot(l[i]);
            ax[i].set_title(terms[i]);
            ax[i].set_ylabel(string);
            ax[i].set_xlabel('i');
            ax[i].text(5, l[i][5]+0.05, round(l[i][5],3), color = 'red')
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#plots the no.of iterations for every testcase for a given function
def plot_iterations(testcase, function):
    '''
    Plots the number of iteration taken by
    the function for each value in testcase list
    '''
    itr = []
    
    for i in testcase:
        itr.append(function(i)[1])
        
    fig, ax = plt.subplots(1, 1, figsize = (6,6))
    ax.plot(testcase, itr)
    ax.set_xlabel('$x$')
    ax.set_ylabel('iterations')
    ax.text(testcase[0] - testcase[-1]*0.02, itr[0] + itr[-1]*0.01, itr[0], color = 'red')
    ax.text(testcase[-1] - testcase[-1]*0.02, itr[-1] + itr[-1]*0.01, itr[-1], color = 'red')
    ax.set_title('Iterations for '+ function.__name__)
#--------------------------------------------------------------------------------------------------------------    

#--------------------------------------------------------------------------------------------------------------

def compare_functions(func1, func2, func3, function, testcases):
    '''
    compare_functions() takes 4 parameters -function1, function2, function3, type of the function.
    Function 1 and 2 need to return a tuple containing value of series 
    and the number of itertations. 
    Function 3 returns the actual value of the series. 
    
    compare_function will plot 2 graphs
    Graph 1 - Iterations taken by func1 and func2 
    Graph 2 - Values calculated by all 3 functions
    ''' 
    itr1 = []                       #iterations for func1
    itr2 = []                       #iterations for func2
    actual = []                     #actual ans for series
    ans1 = []                       #ans returned by func1
    ans2 = []                       #ans returned by func2
    
    for i in testcases :
        tup1 = func1(i)
        tup2 = func2(i)
        itr1.append(tup1[1])        #storing iteration
        itr2.append(tup2[1])
        ans1.append(tup1[0])        #storing ans
        ans2.append(tup2[0])
        actual.append(func3(i))  
        
        
    fig, ax = plt.subplots(1,2,figsize=(12,6))
    
    factor_x = testcases[-1]*0.05
    factor_y = itr1[-1]*0.02
    #Graph 1 - Iterations taken by func1 and func2
    ax[0].plot(testcases,itr1, color = 'red')
    ax[0].plot(testcases,itr2)
    ax[0].text(testcases[-1] - factor_x, itr1[-1] + factor_y, itr1[-1])
    ax[0].text(testcases[-1] - factor_x, itr2[-1]+ factor_y, itr2[-1])
    ax[0].text(testcases[0], itr1[0] + factor_y, itr1[0])
    ax[0].text(testcases[0], itr2[0] + factor_y, itr2[0])
    ax[0].legend([func1.__name__+"()", func2.__name__+"()"])
    ax[0].set_title("Iterations")
    ax[0].set_ylabel("No.of Iterations")
    ax[0].set_xlabel("$x$")
    
    #Graph 2 - Values returned by the 3 functions
    ax[1].plot(testcases, ans1, color = 'red')
    ax[1].plot(testcases, ans2)
    ax[1].plot(testcases, actual)
    ax[1].legend([func1.__name__+"()",func2.__name__+"()",func3.__name__])
    ax[1].set_title("Values of "+function)

#--------------------------------------------------------------------------------------------------------------
    
    