#!/usr/bin/env python
# coding: utf-8

# In[18]:


from pulp import *

# Create a dictionary of the BEST CASE activities and their durations in hours
bestActivities = {
    'DescProd':8, 
    'DevpMktingStrat':8, 
    'DesignBro':2, 
    'DevProdPro':0, 
    'ReqAnal':4, 
    'SoftDes':10, 
    'SysDes':12, 
    'Coding':16,
    'WriDoc':6, 
    'UnitTest':16, 
    'SysTest':16, 
    'PackDel':4,
    'SurvMark':16, 
    'DevPriPlan':24, 
    'DevImpPlan':16, 
    'WriPro':8
}

# Create a list of the activities
best_activities_list = list(bestActivities.keys())

# Create a dictionary of the EXPECTED CASE activities and their durations in hours
expectedActivities = {
    'DescProd':12, 
    'DevpMktingStrat':16, 
    'DesignBro':6, 
    'DevProdPro':0, 
    'ReqAnal':6, 
    'SoftDes':20, 
    'SysDes':20, 
    'Coding':32,
    'WriDoc':8, 
    'UnitTest':32, 
    'SysTest':32, 
    'PackDel':12,
    'SurvMark':20, 
    'DevPriPlan':32, 
    'DevImpPlan':20, 
    'WriPro':32
}

# Create a list of the activities
expected_activities_list = list(expectedActivities.keys())

# Create a dictionary of the WORST CASE activities and their durations in hours
worstActivities = {
    'DescProd':16, 
    'DevpMktingStrat':24, 
    'DesignBro':10, 
    'DevProdPro':0, 
    'ReqAnal':8, 
    'SoftDes':30, 
    'SysDes':24, 
    'Coding':48,
    'WriDoc':10, 
    'UnitTest':48, 
    'SysTest':48, 
    'PackDel':20,
    'SurvMark':24, 
    'DevPriPlan':40, 
    'DevImpPlan':24, 
    'WriPro':56
}

# Create a list of the activities
worst_activities_list = list(worstActivities.keys())

# Create a dictionary of the activity precedences
precedences = {
    'DescProd': [], 
    'DevpMktingStrat': [], 
    'DesignBro': ['DescProd'], 
    'DevProdPro': [],  
    'ReqAnal': ['DescProd'], 
    'SoftDes': ['ReqAnal'], 
    'SysDes': ['ReqAnal'], 
    'Coding': ['SoftDes','SysDes'],
    'WriDoc': ['Coding'], 
    'UnitTest': ['Coding'], 
    'SysTest': ['UnitTest'], 
    'PackDel': ['WriDoc','SysTest'],  
    'SurvMark': ['DevpMktingStrat','DesignBro'], 
    'DevPriPlan': ['PackDel','SurvMark'], 
    'DevImpPlan': ['DescProd','PackDel'], 
    'WriPro': ['DevPriPlan','DevImpPlan']
}

# Create the LP problems
best_prob = LpProblem("Critical Path", LpMinimize)
expected_prob = LpProblem("Critical Path", LpMinimize)
worst_prob = LpProblem("Critical Path", LpMinimize)

# Create the LP variables for BEST CASE
best_start_times = {activity: LpVariable(f"start_{activity}", 0, None) for activity in best_activities_list}
best_end_times = {activity: LpVariable(f"end_{activity}", 0, None) for activity in best_activities_list}

# Create the LP variables for EXPECTED CASE
expected_start_times = {activity: LpVariable(f"start_{activity}", 0, None) for activity in expected_activities_list}
expected_end_times = {activity: LpVariable(f"end_{activity}", 0, None) for activity in expected_activities_list}

# Create the LP variables for WORST CASE
worst_start_times = {activity: LpVariable(f"start_{activity}", 0, None) for activity in worst_activities_list}
worst_end_times = {activity: LpVariable(f"end_{activity}", 0, None) for activity in worst_activities_list}


# Add the constraints for BEST CASE
for activity in best_activities_list:
    best_prob += best_end_times[activity] == best_start_times[activity] + bestActivities[activity], f"{activity}_duration"
    for predecessor in precedences[activity]:
        best_prob += best_start_times[activity] >= best_end_times[predecessor], f"{activity}_predecessor_{predecessor}"
        
# Add the constraints for EXPECTED CASE
for activity in expected_activities_list:
    expected_prob += expected_end_times[activity] == expected_start_times[activity] + expectedActivities[activity], f"{activity}_duration"
    for predecessor in precedences[activity]:
        expected_prob += expected_start_times[activity] >= expected_end_times[predecessor], f"{activity}_predecessor_{predecessor}"
        
# Add the constraints for WORST CASE
for activity in worst_activities_list:
    worst_prob += worst_end_times[activity] == worst_start_times[activity] + worstActivities[activity], f"{activity}_duration"
    for predecessor in precedences[activity]:
        worst_prob += worst_start_times[activity] >= worst_end_times[predecessor], f"{activity}_predecessor_{predecessor}"

        
# Set the objective function for BEST CASE
best_prob += lpSum([best_end_times[activity] for activity in best_activities_list]), "minimize_end_times"

# Set the objective function for EXPECTED CASE
expected_prob += lpSum([expected_end_times[activity] for activity in expected_activities_list]), "minimize_end_times"

# Set the objective function for WORST CASE
worst_prob += lpSum([worst_end_times[activity] for activity in worst_activities_list]), "minimize_end_times"

# Solve the LP problems
best_status = best_prob.solve()
expected_status = expected_prob.solve()
worst_status = worst_prob.solve()

# Print the results for BEST CASE
print("Best Case Critical Path time:")
for activity in best_activities_list:
    if value(best_start_times[activity]) == 0:
        print(f"{activity} starts at time 0")
    if value(best_end_times[activity]) == max([value(best_end_times[activity]) for activity in best_activities_list]):
        print(f"{activity} ends at {value(best_end_times[activity])} hours in duration")
        print(f"Minimum cost is: {value(best_end_times[activity])} * the hourly rate of $31.51.")
        print(f"Minimum cost is: ${round(value(best_end_times[activity])*31.51,2)}.")

# Print solution for BEST CASE
print("\nBest case Solution variable values:")
for var in best_prob.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)
        
print('-----------------------------------------------------------------------------------')
print('-----------------------------------------------------------------------------------')

# Print the results for EXPECTED CASE
print("Expected Case Critical Path time:")
for activity in expected_activities_list:
    if value(expected_start_times[activity]) == 0:
        print(f"{activity} starts at time 0")
    if value(expected_end_times[activity]) == max([value(expected_end_times[activity]) for activity in expected_activities_list]):
        print(f"{activity} ends at {value(expected_end_times[activity])} hours in duration")
        print(f"Minimum cost is: {value(expected_end_times[activity])} * the hourly rate of $31.51.")
        print(f"Minimum cost is: ${round(value(expected_end_times[activity])*31.51,2)}.")

# Print solution for EXPECTED CASE
print("\nExpected case solution variable values:")
for var in expected_prob.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)
        
print('-----------------------------------------------------------------------------------')
print('-----------------------------------------------------------------------------------')

# Print the results for WORST CASE
print("Worst Case Critical Path time:")
for activity in worst_activities_list:
    if value(worst_start_times[activity]) == 0:
        print(f"{activity} starts at time 0")
    if value(worst_end_times[activity]) == max([value(worst_end_times[activity]) for activity in worst_activities_list]):
        print(f"{activity} ends at {value(worst_end_times[activity])} hours in duration")
        print(f"Minimum cost is: {value(worst_end_times[activity])} * the hourly rate of $31.51.")
        print(f"Minimum cost is: ${round(value(worst_end_times[activity])*31.51,2)}.")

# Print solution for WORST CASE
print("\nSolution variable values:")
for var in worst_prob.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)

