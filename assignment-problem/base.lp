#const n = 5.

agent(1..n).
task(1..n).

% Generator: each agent is assigned exactly one task
1 { assign(Agent, Task) : task(Task) } 1 :- agent(Agent).

% Ensure no task is assigned to more than one agent
:- assign(Agent1, Task), assign(Agent2, Task), Agent1 != Agent2.

% Minimum sum of costs
#minimize { Cost,Agent,Task : assign(Agent, Task), cost(Agent, Task, Cost) }.

#show assign/2.