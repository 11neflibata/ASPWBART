%%实现deductive

% 猜测一个子集S
in(A) :- not out(A), arg(A).
out(A) :- not in(A), arg(A).

% 带权重的事实的转化: in(A, W, I)
in(A) :- not unsat(I), in(A, W, I).
unsat(I) :- not in(A), in(A, W, I).
:~ unsat(I), in(A, W, I), W!="alpha". [W@0, I]
:~ unsat(I), in(A, W, I), W="alpha". [1@1, I]
% 带权重的事实的转化: out(A, W, I)
out(A) :- not unsat(I), out(A, W, I).
unsat(I) :- not out(A), out(A, W, I).
:~ unsat(I), out(A, W, I), W!="alpha". [W@0, I]
:~ unsat(I), out(A, W, I), W="alpha". [1@1, I]

% attack关系的转化: A => -B
out(B) :- in(A), not unsat(I, 1), attack(A, B, W, I).
unsat(I, 1) :- in(A), not out(B), attack(A, B, W, I).
:~ unsat(I, 1), attack(A, B, W, I), W!="alpha". [W@0, I]
:~ unsat(I, 1), attack(A, B, W, I), W="alpha". [1@1, I] 
% attack关系的转化: B => -A
out(A) :- in(B), not unsat(I, 2), attack(A, B, W, I).
unsat(I, 2) :- in(B), not out(A), attack(A, B, W, I).
:~ unsat(I, 2), attack(A, B, W, I), W!="alpha". [W@0, I]
:~ unsat(I, 2), attack(A, B, W, I), W="alpha". [1@1, I] 

% support关系的转化: A => B
in(B) :- in(A), not unsat(I, 1), support(A, B, W, I).
unsat(I, 1) :- in(A), not in(B), support(A, B, W, I).
:~ unsat(I, 1), support(A, B, W, I), W!="alpha". [W@0, I]
:~ unsat(I, 1), support(A, B, W, I), W="alpha". [1@1, I] 
% support关系的转化: -B => -A
out(A) :- out(B), not unsat(I, 2), support(A, B, W, I).
unsat(I, 2) :- out(B), not out(A), support(A, B, W, I).
:~ unsat(I, 2), support(A, B, W, I), W!="alpha". [W@0, I]
:~ unsat(I, 2), support(A, B, W, I), W="alpha". [1@1, I] 

%输出
#show in/1.