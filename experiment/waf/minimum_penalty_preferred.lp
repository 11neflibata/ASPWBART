%% 猜测一个子集S
in(X) :- not out(X), arg(X).
out(X) :- not in(X), arg(X).

%% S不一定conflict-free
:~ in(X), in(Y), attack(X, Y, W, I), W!="alpha". [W@0]
:~ in(X), in(Y), attack(X, Y, W, I), W="alpha". [1@1]

%% 论据x被S defeat
defeated(X) :- in(Y), attack(Y,X).

%% 论据x不被S defend
not_defended(X) :- attack(Y,X), not defeated(Y).

%% S中的所有论据x都要被S defend (admissibility)
:- in(X), not_defended(X).

%in(X)?
#show in/1.