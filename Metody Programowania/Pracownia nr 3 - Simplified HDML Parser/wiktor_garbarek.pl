:- module(wiktor_garbarek, [parse/3]).
%:-set_prolog_flag(answer_write_options,[quoted(true),portray(true),spacing(next_argument)]).

/* lexer */
/* lexer is reading comments - we delete them after making list of tokens by predicate delete_comments/2 */
/*a lot of inspiration was taken from Tomasz Wierzbickis while parser (lexer and parts of parser) */
lexer(Tokens) -->
    white_space,
   (  ( "(*",       !, { Token = tokLCom }
      ; "*)",       !, { Token = tokRCom }
      ;  "(",       !, { Token = tokLParen }
      ;  ")",       !, { Token = tokRParen }
      ;  "[",       !, { Token = tokLBracket }
      ;  "]",       !, { Token = tokRBracket }
      ;  "..",      !, { Token = tokDdot }
      ;  ",",       !, { Token = tokComma }
      ;  "=",       !, { Token = tokEq }
      ;  "<>",      !, { Token = tokNeq }
      ;  "<=",      !, { Token = tokLeq }
      ;  ">=",      !, { Token = tokMeq }
      ;  "<",       !, { Token = tokLess}
      ;  ">",       !, { Token = tokMore}
      ;  "^",       !, { Token = tokCaret }
      ;  "|",       !, { Token = tokPipe }
      ;  "+",       !, { Token = tokPlus }
      ;  "-",       !, { Token = tokMinus }
      ;  "&",       !, { Token = tokAmpersand }
      ;  "*",       !, { Token = tokTimes }
      ;  "/",       !, { Token = tokSlash }
      ;  "%",       !, { Token = tokPercent }
      ;  "@",       !, { Token = tokAt }
      ;  "#",       !, { Token = tokHash }
      ;  "~",       !, { Token = tokTilde }
      ;  digit(D),  !,
            number(D, N),
            { Token = tokNumber(N) }
      ;  letter(L), !, identifier(L, Id),
        {  member((Id, Token), [ (def, tokDef), ('_', tokUnderscore), (if, tokIf), (in, tokIn), (else, tokElse), (then, tokThen), (let, tokLet)]),
               !;  Token = tokId(Id) }
      ;  [_],
            { Token = tokUnknown }
      ),
      !,
    { Tokens = [Token | TokList] },
    lexer(TokList)
    ;  [],
    { Tokens = [] }
    ).

white_space --> [Char], { code_type(Char, space) }, !, white_space.
white_space --> [].

digit(D) -->
   [D],
      { code_type(D, digit) }.

digits([D|T]) -->
   digit(D),
   !,
   digits(T).
digits([]) -->
   [].

number(D, N) -->
   digits(Ds),
      { number_chars(N, [D|Ds]) }.

letter(L) -->
   [L], { code_type(L, csymf) }.

alphanum([A|T]) -->
   [A], { A == 39 ; code_type(A, csym)  }, !, alphanum(T).
alphanum([]) -->
   [].

identifier(L, Id) -->
   alphanum(As),
      { atom_codes(Id, [L|As]) }.

/* parser */ 
program(Ast) -->
 definitions(Ast).

definitions([D|DR]) --> definition(D),definitions(DR).
definitions([]) --> [].

definition(def(Id,P,E)) -->
  [tokDef],[tokId(Id)],[tokLParen],pattern(P),[tokRParen],[tokEq],expression(E).

pattern(P) --> simple_pattern(P).
pattern(pair(no,P1,P2)) -->simple_pattern(P1),[tokComma],pattern(P2).

simple_pattern(wildcard(no)) --> [tokUnderscore], !.
simple_pattern(var(no,Z)) --> [tokId(Z)], !.
simple_pattern(P) -->[tokLParen], !, pattern(P),[tokRParen].

/* to parse expressions with proper associativity we divided them into 5 types by analogy to their priorities and associativity*/

expression(if(no,E1,E2,E3)) --> [tokIf], !, expression(E1),[tokThen],expression(E2),[tokElse],expression(E3).
expression(let(no,P,E1,E2)) --> [tokLet], !, pattern(P),[tokEq],expression(E1),[tokIn],expression(E2).
expression(W) --> binary_expressionComma(W).

binary_expressionComma(pair(no, E1, E2)) --> 
	binary_expression(E1), [tokComma], !, binary_expressionComma(E2).
binary_expressionComma(E1) --> binary_expression(E1).

binary_expression(op(no, Op, E1, E2)) -->
	binary_expressionAt(E1), inequalities_operators(Op), binary_expressionAt(E2).

binary_expression(E1) --> binary_expressionAt(E1).

inequalities_operators('=') --> [tokEq].
inequalities_operators('<>') --> [tokNeq].
inequalities_operators('<=') --> [tokLeq].
inequalities_operators('>=') --> [tokMeq].
inequalities_operators('<') --> [tokLess].
inequalities_operators('>') --> [tokMore].

binary_expressionAt(op(no, Op, E1, E2)) -->
	binary_expressionArithmWeak(E1), at_operator(Op), binary_expressionAt(E2).
binary_expressionAt(E1) --> binary_expressionArithmWeak(E1).

at_operator('@') --> [tokAt].

%elimination of left recursion taken from Tomasz Wierzbickis while language parser

binary_expressionArithmWeak(A) -->
	binary_expressionArithmStrong(A1),
	binary_expressionArithmWeak(A1,A).

binary_expressionArithmWeak(AC, A) -->
	arithmweak_operators(Op), !,
	binary_expressionArithmStrong(A1),
	{AC1 = op(no, Op, AC, A1)},
	binary_expressionArithmWeak(AC1, A).

binary_expressionArithmWeak(E,E) --> [].

arithmweak_operators('|') --> [tokPipe].
arithmweak_operators('^') --> [tokCaret].
arithmweak_operators('+') --> [tokPlus].
arithmweak_operators('-') --> [tokMinus].

binary_expressionArithmStrong(A) -->
	unary_expression(A1),
	binary_expressionArithmStrong(A1,A).

binary_expressionArithmStrong(AC, A) -->
	arithmstrong_operators(Op), !, 
	unary_expression(A1), 
	{AC1 = op(no, Op, AC, A1)}, 
	binary_expressionArithmStrong(AC1, A).

binary_expressionArithmStrong(A,A) --> [].

arithmstrong_operators('&') --> [tokAmpersand].
arithmstrong_operators('*') --> [tokTimes].
arithmstrong_operators('/') --> [tokSlash].
arithmstrong_operators('%') --> [tokPercent].

unary_expression(op(no, Op, E1)) -->
	unary_operator(Op), unary_expression(E1).
unary_expression(E1) --> simple_expression(E1).

unary_operator('-') --> [tokMinus].
unary_operator('#') --> [tokHash].
unary_operator('~') --> [tokTilde].

simple_expression(E) --> 
	atomic(E1),
 	simple_expression(E1,E).

simple_expression(E) --> [tokLParen], !, expression(E), [tokRParen].

simple_expression(AC,E) -->
	bit_select(E1),
	{AC1 = bitsel(no, AC, E1)},
	simple_expression(AC1, E).

simple_expression(AC, E) -->
	bits_select(E1,E2),
	{AC1 = bitsel(no, AC, E1, E2)},
	simple_expression(AC1, E).

simple_expression(E,E) --> [].

atomic(var(no, X)) --> [tokId(X)].
atomic(num(no, N)) --> [tokNumber(N)].
atomic(empty(no)) --> [tokLBracket], [tokRBracket].
atomic(bit(no, E)) --> [tokLBracket], !, expression(E), [tokRBracket].
atomic(call(no, N, E)) --> [tokId(N)], [tokLParen], !, expression(E), [tokRParen].
atomic(E) --> [tokLParen], !, expression(E), [tokRParen].

bit_select(E2) --> [tokLBracket], expression(E2), [tokRBracket]. 
bits_select(E2,E3) --> [tokLBracket], expression(E2), [tokDdot], expression(E3), [tokRBracket].


/* non-dcg part to delete comments
we add to counter 1 if we are starting comment and subtract 1 if we are ending comment (and deleting everything from comments)
comments are balanced when counter is = 0 after going through whole list and counter cannot be negative number */
delete_comments(Tokens, NewTokens) :- delete_comments(Tokens, NewTokens, 0).

delete_comments(_,_, A) :- A < 0, !, fail.
delete_comments([],[], A) :- A =\= 0, !, fail.
delete_comments([],[],_).
delete_comments([tokLCom|RT], T1, Count1) :- Count2 is Count1 + 1, !, delete_comments(RT, T1, Count2).
delete_comments([tokRCom|RT], T1, Count1) :- Count2 is Count1 - 1, !, delete_comments(RT, T1, Count2).
delete_comments([_|RT], T1, Count) :- Count > 0, !, delete_comments(RT,T1,Count).
delete_comments([T|RT], [T|T1], 0) :- delete_comments(RT,T1,0).


/*main part*/
parse(_, X, Absynt) :-
   string_to_list(X,CharCodeList),
   phrase(lexer(TokList), CharCodeList),
   delete_comments(TokList, NewTokList),
   phrase(program(Absynt), NewTokList).

