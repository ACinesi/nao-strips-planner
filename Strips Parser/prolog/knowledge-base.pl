% Simple STRIPS-like planner
% Monkey and Bananas Problem

% Artificial intelligence programming in prolog
% Practical 9

% 23/11/04 Tim Smith

% This predicate initialises the problem states. The first argument
% of solve/3 is the initial state, the 2nd the goal state, and the 
% third the plan that will be produced.

test(Plan):-   
    solve(
        [ballAt(b),at(a),level(high),hand(empty)],
	    [bring(ball),at(a)],
         Plan
        ).

solve(State, Goal, Plan):-
    solve(State, Goal, [], Plan).

% This predicate produces the plan. Once the Goal list is a subset 
% of the current State the plan is complete and it is written to 
% the screen using write_sol/1.

solve(State, Goal, Plan, Plan):-
	is_subset(Goal, State).

solve(State, Goal, Sofar, Plan):-
	opn(Op, Preconditions, Delete, Add),
	is_subset(Preconditions, State),
	\+ member(Op, Sofar),
	delete_list(Delete, State, Remainder),
	append(Add, Remainder, NewState),
	solve(NewState, Goal, [Op|Sofar], Plan).
   
% The M&B problem has three operators.
% 1st arg = name
% 2nd arg = preconditions
% 3rd arg = delete list
% 4th arg = add list.

opn(move(X,Y),
    [at(X),level(high)],
    [at(X)],
    [at(Y)]).
    
opn(sitUp(Location),
    [at(Location),level(low)],
    [level(low)],
    [level(high)]).

opn(sitDown(Location),
    [at(Location),level(high)],
    [level(high)],
    [level(low)]).

opn(returnNWB(X,Y),
    [at(X),ballAt(X),hand(full),level(high)],
    [ballAt(X),at(X)],
    [ballAt(Y),at(Y),bring(ball)]).

opn(takeBall(Location),
    [ballAt(Location),at(Location),level(low),hand(empty)],
    [hand(empty)],
    [hand(full)]).

% Utility predicates.

% Check is first list is a subset of the second

is_subset([H|T], Set):-
    member(H, Set),
    is_subset(T, Set).
is_subset([], _).

% Remove all elements of 1st list from second to create third.

delete_list([H|T], List, Final):-
    remove(H, List, Remainder),
    delete_list(T, Remainder, Final).
delete_list([], List, List).
    
remove(X, [X|T], T).
remove(X, [H|T], [H|R]):-
    remove(X, T, R).

write_sol([]).
write_sol([H|T]):-
	write_sol(T),
	write(H), nl.
                 
append([H|T], L1, [H|L2]):-
    append(T, L1, L2).
append([], L, L).

member(X, [X|_]).
member(X, [_|T]):-
    member(X, T).

