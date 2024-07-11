import clingo
import answer

asp_code_input = """
    arg(1).
    arg(2).
    arg(3).
    arg(4).
    arg(5).
    attack(2, 5, "alpha", 1).
    attack(5, 2, "alpha", 2).
    attack(2, 3, 10, 3).
    support(3, 1, 8, 4).
    support(4, 3, "alpha", 5).
    in(1, "alpha", 1).
    in(5, 5, 2).
"""

asp_code_preferred = """
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
"""

ctl = clingo.Control()
# find all best answers
ctl.configuration.solve.opt_mode = "optN"
# add each program
ctl.add("input", [], asp_code_input)
ctl.add("preferred", [], asp_code_preferred)
# ground
ctl.ground([("input", []), ("preferred", [])])
# solve
models = ctl.solve(yield_=True)
answer.print_max_model(models)
answer.print_optimization(ctl.solve(yield_=True))