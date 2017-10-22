% Strips as a regression planner.
% Top-level interface.
strips(InitState, GoalList, Plan) :-
	strips1(InitState, GoalList, [], [], _, RevPlan),
	reverse(RevPlan, Plan).

% Base case: All goals satisfied in State.
strips1(State, GoalList, Plan, _, State, Plan) :-
 subset(GoalList, State).

% Plan
strips1(State, GoalList, Plan, BadActions, NewState, NewPlan) :-
	member(Goal, GoalList),
	not(member(Goal, State)),    % Find unsatisfied goal.
	write('\nAttempting goal:  '),write(Goal),nl,
	adds(Ac, Goal),              % Find action that achieves it.
	write(' Choosing Action:  '),write(Ac),
	not(member(Ac, BadActions)), % Do not repeat actions (dangerous).
	write(' -- not a bad action.'),nl,
	preclist(Ac, PrecList),      % Find preconds and achieve them.       
	strips1(State, PrecList, Plan, [Ac|BadActions], TmpState1, TmpPlan1),
	apply_rule(Ac, TmpState1, TmpState2),  % Recurse w/new state and goals.
	strips1(TmpState2,GoalList,[Ac|TmpPlan1],BadActions,NewState,NewPlan).
	
% Apply Rule
apply_rule(Ac, State, NewState) :-
	write('\nSimulating '),write(Ac),nl,
	write('From: '), write(State), write('\n----> '),
	dellist(Ac, DelList),                     % find deleted props
	subtract(State, DelList, TmpState),       % remove deleted props
	addlist(Ac, AddList),                     % find added props
	union(AddList, TmpState, NewState),       % add props to old state
	write(NewState).
   
% Utilities
preclist(Action, Plist) :- strips_rule(Action, Plist, _, _).
prec(Action, Cond) :- preclist(Action, Plist), member(Cond, Plist).
addlist(Action, Alist) :- strips_rule(Action, _, Alist, _).
adds(Action, Cond) :- addlist(Action, Alist), member(Cond, Alist).
dellist(Action, Dlist) :- strips_rule(Action, _, _, Dlist).
dels(Action, Cond) :- dellist(Action, Dlist), member(Cond, Dlist).

% Pretty-print Init, Goal, and Plan.
plan(InitState, Goal) :-
	strips(InitState,Goal,Plan),
	write('\n\nInit: '), write(InitState),nl,
	write('Goal: '),write(Goal),nl,
	write('Plan:\n'),
        writeplan(Plan),nl.

% Pretty-print the plan.
writeplan([]).
writeplan([A|B]):-
  write('       '),write(A),nl,
  writeplan(B).

