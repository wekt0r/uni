:- op(200, fx, ~).
:- op(500, xfy, v).

% Scored 6 out of 7
% 1961 out of 1965 validity tests were OK, rest - TLE
% 268 out of 329 performance tests were OK, rest - TLE

%Input: List of clauses
%Output: List of logical values for every variable (t means true, f - false, x stands for "doesn't matter if true or false")
%Example: 
%?- solve([p v q], X).
%X = [(p,t),(q,x)];
%X = [(p,f),(q,t)];
%false

%Idea of this is based on dpll algorithm
%When we consider all variables in list of clauses, let's say [p,q,r,...], when we claim that p is true,
%we can be sure that (1) all clauses with non-negated p are true and (2) all clauses with negated p
%depends on the value of other variables so we can simplify clauses (eg. ~p v q v r v ~p can be simplified
%into q v r). And by analogy, while considering p false, we can delete all clauses with ~p and simplify
%rest of formulas by deleting p variable.

%variable predicate checks if X is raw variable, literal checks if it is variable or negation of it

variable(X) :- X \= _ v _, X \= ~_.
literal(X) :- X \= _ v _.

%variables predicate gives us list of all raw variables that are given in clause (with duplicates - later we delete duplicates with built-in sort/2 predicate).

variables(A,[A]) :- variable(A), !.
variables(~A,[A]) :- variable(A), !.
variables(A v B,[A|X2]) :- variable(A), variables(B,X2), \+ member(A, X2), !.
variables(A v B,[C|X2]) :- literal(A), A = ~C, variables(B,X2), \+ member(C,X2), !.
variables(A v B,X) :- variable(A), variables(B,X), !.
variables(A v B,X) :- literal(A), variables(B,X), !.

%all_variables_in_list gives us list of all variables in given clauses

all_variables_in_list([],[]) :- !.
all_variables_in_list([H|T],X):- variables(H,Y1), all_variables_in_list(T,Y2), append(Y1,Y2,X).

%Deletes all negations of given variable from clause.
%Note: This doesn't work for formulas like ~p v ~p v ~p (returns ~p as answer) and it is probably 
%impossible to get it work "correctly" (giving [] as answer to previous example would imply giving wrong 
%solution as we consider empty clause to be always false - we would have to delete this clause from list)
%BUT! it still works for this assignment purposes (it probably works slower, because ~p clause is left till 
%very end, and as the list of clauses cannot unify with empty list it gives fail in the solution)
%we could be checking AFTER deleting if there is ~p in list, but i've been testing this idea on some
%tests and it doesn't seem to be effective

delete_from_when_true(H, B, B):- literal(B), B \= H.
delete_from_when_true(H, B v ~H, B) :- !.
delete_from_when_true(H, ~H v B, B1):- delete_from_when_true(H,B,B1),!.
delete_from_when_true(H, A v B, A v B1):- delete_from_when_true(H,B,B1).

delete_from_when_false(H, B, B):- literal(B), B \= H.
delete_from_when_false(H, B v H, B) :- !.
delete_from_when_false(H, H v B, B1):- delete_from_when_false(H,B,B1),!.
delete_from_when_false(H, A v B, A v B1):- delete_from_when_false(H,B,B1).

go_through_list2(_,[],[]):- !.
go_through_list2(H,[H1|T1],[H2|T2]):- delete_from_when_false(H,H1,H2), go_through_list2(H,T1,T2).

go_through_list1(_,[],[]):- !.
go_through_list1(H,[H1|T1],[H2|T2]):- delete_from_when_true(H,H1,H2), go_through_list1(H,T1,T2).

%Checks if given variable (raw variable, not negated) is in given clause.
strictmember(X,X):- !.
strictmember(X,X v _):- !.
strictmember(X,_ v Y):- strictmember(X,Y).

%Checks if negation of given variable is in given clause.
strictmemberneg(X,~X):- !.
strictmemberneg(X,~X v _):- !.
strictmemberneg(X,_ v Y):- strictmemberneg(X,Y).

%Deletes from list all clauses with given variable (or negation of this variable)

deletee(_,[],[]):- !.
deletee(H,[C1|REST],REST1):-
   strictmember(H,C1),!,
   deletee(H,REST,REST1).

deletee(H,[C1|REST],[C1|REST1]):-
   deletee(H,REST,REST1).

deletenegated(_,[],[]):- !.
deletenegated(H,[C1|REST],REST1):-
   strictmemberneg(H,C1), !,
   deletenegated(H,REST,REST1).
deletenegated(H,[C1|REST],[C1|REST1]):-
   deletenegated(H,REST,REST1).

%Main solve predicate - in pre-processing we list all variables
%Note: algorithm takes [] as variable, so while we know that list with empty clause is always false we can 
%simply check if [] isn't a member of variables list

solve(CLA,RES):-
   all_variables_in_list(CLA,A1),
   sort(A1,VARS),
   \+ member([],VARS),
   solve(CLA,VARS,RES).

solve([],[],[]) :- !.
solve([],[H|T],[(H,x)|T2]) :- solve([],T,T2), !.

solve(CLA,[H|REST_VARS],[(H,t)|RES]):-
   deletee(H,CLA,CLA1),
   \+ member(~H,CLA1),
   go_through_list1(H,CLA1,CLA2),
   solve(CLA2,REST_VARS,RES).

solve(CLA,[H | REST_VARS],[(H,f)|RES]):-
   deletenegated(H,CLA,CLA1),
   \+ member(H,CLA1),
   go_through_list2(H,CLA1,CLA2),
   solve(CLA2,REST_VARS,RES).
