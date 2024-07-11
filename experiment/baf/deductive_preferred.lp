%%实现deductive

% 猜测一个子集S
in(A) :- not out(A), arg(A).
out(A) :- not in(A), arg(A).

% attack关系: A => -B、B => -A
out(B) :- in(A), attack(A, B).
out(A) :- in(B), attack(A, B).

% support关系: A => B、-B => -A
in(B) :- in(A), support(A, B).
out(A) :- out(B), support(A, B).

%%实现preferred

lt(X,Y) :- arg(X), arg(Y), X<Y, not input_error.
% succ表示直接继承关系（相邻），nsucc表示不相邻
nsucc(X,Z) :- lt(X,Y), lt(Y,Z).
succ(X,Y) :- lt(X,Y), not nsucc(X,Y).
ninf(X) :- lt(Y,X).
nsup(X) :- lt(X,Y). 
% inf表示下界，sup表示上界
inf(X) :- not ninf(X), arg(X).
sup(X) :- not nsup(X), arg(X).

%% 猜测一个S', S'包含S（通过S'确保S为最大集合包含，即preferred extension）
inN(X) :- in(X).
inN(X) | outN(X) :- out(X).

%% 若S'=S，则spoil
%% 使用继承函数，从下界开始，检查S'中的元素是否在S中。不成立，则stop
%% 若到达上界，则spoil up

% eq表示一个S'猜测是否与S猜测相等
eq_upto(Y) :- inf(Y), in(Y), inN(Y).
eq_upto(Y) :- inf(Y), out(Y), outN(Y).
eq_upto(Y) :- succ(Z,Y), in(Y), inN(Y), eq_upto(Z).
eq_upto(Y) :- succ(Z,Y), out(Y), outN(Y), eq_upto(Z).
eq :- sup(Y), eq_upto(Y). 

%% 如果S'等于S，则spoil
spoil :- eq.

%% 如果AF为空，则spoil
not_empty :- arg(X).
spoil :- not not_empty.

%% S'必须满足BAF中的attack和support关系，否则spoil
spoil :- inN(X), inN(Y), attack(X, Y).
spoil :- inN(X), outN(Y), support(X, Y).
spoil :- outN(X), inN(Y), support(X, Y).

inN(X) :- spoil, arg(X).
outN(X) :- spoil, arg(X).

%% 执行最终的spoil-thing
:- not spoil.

%输出
#show in/1.