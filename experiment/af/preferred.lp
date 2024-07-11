%% 猜测一个子集S
in(X) :- not out(X), arg(X).
out(X) :- not in(X), arg(X).

%% S必须conflict-free
:- in(X), in(Y), attack(X,Y).

%% 论据x被S defeat
defeated(X) :- in(Y), attack(Y,X).

%% 论据x不被S defend
not_defended(X) :- attack(Y,X), not defeated(Y).

%% S中的所有论据x都要被S defend (admissibility)
:- in(X), not_defended(X).

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

%% 获取不在S'中(outN)，且不被S' defeat的X

undefeated_upto(X,Y) :- inf(Y), outN(X), outN(Y).
undefeated_upto(X,Y) :- inf(Y), outN(X), not attack(Y,X).

undefeated_upto(X,Y) :- succ(Z,Y), undefeated_upto(X,Z), outN(Y).
undefeated_upto(X,Y) :- succ(Z,Y), undefeated_upto(X,Z), not attack(Y,X).

undefeated(X) :- sup(Y), undefeated_upto(X,Y).

%% 如果AF为空，则spoil
not_empty :- arg(X).
spoil :- not not_empty.

%% 如果对于所有的preferred extensions，S'等于S，则spoil
spoil :- eq.

%% S'必须是conflict-free，否则spoil
spoil :- inN(X), inN(Y), attack(X,Y).

%% S'必须是admissible，否则spoil
spoil :- inN(X), outN(Y), attack(Y,X), undefeated(Y).

inN(X) :- spoil, arg(X).
outN(X) :- spoil, arg(X).

%% 执行最终的spoil-thing
:- not spoil.

%in(X)?
#show in/1.