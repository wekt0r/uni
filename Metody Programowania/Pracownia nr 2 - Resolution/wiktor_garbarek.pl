:- module(wiktor_garbarek, [resolve/4, prove/2]).
:- op(200, fx, ~).
:- op(500, xfy, v).

%this solution got 4 points out of 7 in tests (a lot of TLE)
%solution is not elegant nor smart - brute force all the way, because of proofs format and time shortage
%idea is to take all clauses, resolve them and store "tree of resolution" - ie. if we resolve left parent and right parent we get node

variable(X) :- X \= _ v _, X \= ~_.
literal(X) :- X \= _ v _.

delete_repeating_clauses([],[]).
delete_repeating_clauses([X:A],[X:A]).
delete_repeating_clauses([X:A,X:_|Xs],Zs) :- delete_repeating_clauses([X:A|Xs],Zs).
delete_repeating_clauses([X:A,Y:B|Ys],[X:A|Zs]) :- X \= Y, delete_repeating_clauses([Y:B|Ys],Zs).

list_from_trees([],[]).
list_from_trees([X:_|T],[X|T1]):- list_from_trees(T,T1).

%surprisingly works in both ways (ie. +,- and -, +)
clause_into_list([],[]) :- !.
clause_into_list(A, [A]) :- literal(A), !.
clause_into_list(A v B,[A|B1]) :- clause_into_list(B,B1).

singleton([_]).

tautology(Vars, CL) :- select(Var, Vars, _), strictmember(Var,CL), strictmember(~Var,CL), !.

amount_and_list_of_literals(Set,N,L) :- amount_of_literals(Set,0,N,L).
amount_of_literals([],N,N,[]).
amount_of_literals([A:_|T],N,X,[A|T1]) :- literal(A), !, N1 is N+1, amount_of_literals(T, N1, X,T1).
amount_of_literals([_:_|T],N,X,T1) :- amount_of_literals(T,N,X,T1).

getposition(Member,List,X) :- getposition(Member,List,1, X).
getposition(H,[H|_], X,X) :- !.
getposition(H,[_|T], X1, X) :- X2 is X1 + 1, getposition(H,T,X2,X).

equallength([],[]).
equallength([_|T],[_|T1]) :- equallength(T,T1).


listlength(Set,N) :- listlength(Set,0,N).
listlength([],N,N).
listlength([_|T],N,X):- N1 is N+1, listlength(T,N1,X).

appendclause(A, X, A v X) :- literal(A), !. 
appendclause(H v T, X, H v Y) :-
	appendclause(T, X, Y).

variables(A,[A]) :- variable(A), !.
variables(~A,[A]) :- variable(A), !.
variables(A v B,[A|X2]) :- variable(A), variables(B,X2), \+ member(A, X2), !.
variables(A v B,[C|X2]) :- literal(A), A = ~C, variables(B,X2), \+ member(C,X2), !.
variables(A v B,X) :- variable(A), variables(B,X), !.
variables(A v B,X) :- literal(A), variables(B,X), !.

all_variables_in_list([],[]) :- !.
all_variables_in_list([H|T],X):- variables(H,Y1), all_variables_in_list(T,Y2), append(Y1,Y2,X).

%strict_member(-X,-Y). -- works O(n)

strictmember(X,X) :- !.
strictmember(X,X v _) :- !.
strictmember(X,_ v Y):- strictmember(X,Y).

resolve(V,C1,C2,X) :- clause_into_list(C1,L1), memberchk(V,L1), clause_into_list(C2,L2), memberchk(~V,L2), sort(L1,LS1), sort(L2,LS2), select(V, LS1, LN1), select(~V,LS2,LN2), append(LN1,LN2,LN), sort(LN,LNX), clause_into_list(X,LNX). 
resolvetree(V, C1:X1, C2:X2, X:node(C1:X1,X,C2:X2)) :- resolve(V,C1,C2,X).

almostsubset([],_) :- !.
almostsubset([A|T],X):- memberchk(A,X), !, almostsubset(T,X).
almostsubset([A|T],X):- memberchk(~A,X), almostsubset(T,X).

subset([],_).
subset([H|T],X):- memberchk(H,X), subset(T,X).

%resolveset(Last,Current,Result)
%subsumption(CL1, CL2) when CL1 < CL2 (CL1 has the same literals as CL2 does (CL2 can be bigger))

subsumption(A,A) :- !.
subsumption(A,B) :- literal(A), strictmember(A,B), !.
subsumption(A v A1, B) :- strictmember(A,B), subsumption(A1,B).

look_for_smaller(_,[],[]).
look_for_smaller(A,[H:F|T],[H:F|T1]) :- subsumption(H,A), !, look_for_smaller(A,T,T1).
look_for_smaller(A,[_:_|T],T1) :- look_for_smaller(A,T,T1).

make_subsumptions(Clauses, Result) :- make_subsumptions(Clauses, Clauses, Result).

make_subsumptions([],_,[]) :- !.
make_subsumptions([H:F|T],CL,[H:F|T1]) :- look_for_smaller(H,CL,X), sort(0, @<, X,Y), delete_repeating_clauses(Y,[_]), !, make_subsumptions(T,CL,T1).
make_subsumptions([_:_|T],CL,T1) :- make_subsumptions(T,CL,T1).

%every clause is subsumption of itself, if whole set of smaller clauses of one clause is singleton (contains itself)
%then we know this clause is "small enough" to be important in our resolution

allresolution_2clauses([],_,_,[]) :- !.
allresolution_2clauses([V|Vars], C1:node(LC1,C1,RC1), C2:node(LC2,C2,RC2), [ONERES|T]) :- resolvetree(V, C1:node(LC1,C1,RC1),C2:node(LC2,C2,RC2),ONERES), !, allresolution_2clauses(Vars,C1:node(LC1,C1,RC1), C2:node(LC2,C2,RC2),T).
allresolution_2clauses([V|Vars], C1:node(LC1,C1,RC1), C2:node(LC2,C2,RC2), [ONERES|T]) :- resolvetree(V, C2:node(LC2,C2,RC2), C1:node(LC1,C1,RC1),ONERES), !, allresolution_2clauses(Vars,C1:node(LC1,C1,RC1), C2:node(LC2,C2,RC2),T).
allresolution_2clauses([_|Vars], C1:node(LC1,C1,RC1), C2:node(LC2,C2,RC2), T) :- allresolution_2clauses(Vars,C1:node(LC1,C1,RC1), C2:node(LC2,C2,RC2),T). 

%theorem: if resolution is possible for more than one variable, then resolvents are tautologies in all cases 
%(proof is trivial) - this speeds us up - instead of appending, we can simply check if Res is singleton and
%put it on head of list of clauses

allresolution_2sets(Vars, SetA, Result) :- allresolution_2sets(Vars, SetA, SetA, Result).

allresolution_2sets(_,[],[],[]) :- !.
allresolution_2sets(Vars, [_|SetA], [], Result) :- allresolution_2sets(Vars, SetA, SetA, Result).
allresolution_2sets(Vars, [A|SetA],[B|SetB], [X|Result]) :- allresolution_2clauses(Vars,A,B,[X]), !, allresolution_2sets(Vars,[A|SetA],SetB, Result).
allresolution_2sets(Vars, [A|SetA],[_|SetB], Result) :- allresolution_2sets(Vars,[A|SetA],SetB, Result).

delete_tautologies(_, [],[]) :- !.
delete_tautologies(Vars, [X:_|T], T1) :- tautology(Vars, X), !, delete_tautologies(Vars, T,T1).
delete_tautologies(Vars, [X:Y|T],[X:Y|T1]) :- delete_tautologies(Vars, T,T1).

allresolutionsneeded(Vars, A, A2) :- memberchk([]:_,A), !, delete_tautologies(Vars,A,A1), make_subsumptions(A1,A2) .
allresolutionsneeded(Vars, A, X) :- allresolution_2sets(Vars, A,A1), delete_tautologies(Vars, A1,A2), append(A2,A,X), make_subsumptions(X,XN), list_from_trees(XN,SimpleX1), list_from_trees(A,SimpleA1), sort(SimpleX1, F), sort(SimpleA1, F), !.
allresolutionsneeded(Vars, A, B) :- allresolution_2sets(Vars, A,A1), delete_tautologies(Vars, A1,A2), append(A2,A,X), make_subsumptions(X,XN), allresolutionsneeded(Vars,XN,B).

make_axiom_list([],[]).
make_axiom_list([H|T],[H:node(axiom,H,axiom)|T1]) :- make_axiom_list(T,T1). 

find_empty_clause([[]:node(A,[],B)|_], []:node(A,[],B)):- !.
find_empty_clause([_:_|T],X) :- find_empty_clause(T,X).

make_almost_proof_from_tree(X:node(axiom,X,axiom), [(X,axiom)]).
make_almost_proof_from_tree(C:node(A,C,B), [(C,(A1,B1))|T]) :- A = A1:node(_,A1,_), B = B1:node(_,B1,_), make_almost_proof_from_tree(A,T1), make_almost_proof_from_tree(B,T2), append(T1,T2,T). 

enumerate(Vars,S,S1) :- enumerate(Vars,S,S,S1).

enumerate(_,_,[],[]) :- !.
enumerate(Vars,U,[(A,axiom)|T], [(A,axiom)|T1]) :- !, enumerate(Vars,U, T,T1).
enumerate(Vars,U,[(A,(C1,C2))|T],[(A, (V1, P1, P2))|T1]) :- getposition((C1,_),U,P1), getposition((C2,_),U,P2), select(V1, Vars, _), resolve(V1,C1,C2,A),enumerate(Vars,U,T,T1).

prove([[]],[([],axiom)]).
prove(Set, Proof) :- \+ singleton(Set), all_variables_in_list(Set,Vars1), sort(Vars1, Vars), sort(Set,Setx), make_axiom_list(Setx,Set1), make_subsumptions(Set1, Set2) ,allresolutionsneeded(Vars, Set2, A), find_empty_clause(A, X), make_almost_proof_from_tree(X,Pr),reverse(Pr, Prf), enumerate(Vars, Prf,Proof).



