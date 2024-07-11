import random
import clingo
import numpy as np
import time

start = time.perf_counter()  # begin_time

asp_code_arg = """
    arg(a).
"""

asp_code_attack = """
    attack(a, b, w, i).
"""

asp_code_support = """
    support(a, b, w, i).
"""

asp_code_in = """
    in(a, w, i).
"""

asp_code_out = """
    out(a, w, i).
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
ctl.add("arg", ["a"], asp_code_arg)
ctl.add("attack", ["a", "b", "w", "i"], asp_code_attack)
ctl.add("support", ["a", "b", "w", "i"], asp_code_support)
ctl.add("in", ["a", "w", "i"], asp_code_in)
ctl.add("out", ["a", "w", "i"], asp_code_out)
ctl.add("preferred", [], asp_code_preferred)
# ground
argN = 700000  # number of arguments
relationN = random.randint(argN, 2*argN)  # number of relations
maxWeight = 10  # maximum weight except "alpha"
asp_code_input = []
# ground for arg() and in()
weightList = np.random.randint(1, maxWeight + 2, argN).tolist()
# print(weightList)
for i in range(0, argN):
    asp_code_input.append(("arg", [clingo.Number(i + 1)]))
    if weightList[i] == maxWeight + 1:
        w = clingo.String("alpha")
    else:
        w = clingo.Number(weightList[i])
    asp_code_input.append(("in", [clingo.Number(i + 1), w, clingo.Number(i + 1)]))
ctl.ground(asp_code_input)
# ground for attack() and support()
ctl.cleanup()
asp_code_input = []
weightList = np.random.randint(1, maxWeight + 2, relationN).tolist()
# print(weightList)
relationList = np.random.randint(0, 2, relationN).tolist() # 0 represents attack, 1 represents support
# print(relationList)
aList = np.random.randint(1, argN + 1, relationN).tolist()
# print(aList)
bList = np.random.randint(1, argN + 1, relationN).tolist()
# print(bList)
for i in range(0, relationN):
    if weightList[i] == maxWeight + 1:
        w = clingo.String("alpha")
    else:
        w = clingo.Number(weightList[i])
    if relationList[i] == 0:
        relation = "attack"
    else:
        relation = "support"
    asp_code_input.append((relation, [clingo.Number(aList[i]), clingo.Number(bList[i]), w, clingo.Number(i + 1)]))
ctl.ground(asp_code_input)
# ground for preferred
ctl.cleanup()
ctl.ground([("preferred", [])])
# solve
# print(ctl.solve(on_model=print))

end = time.perf_counter()  # end_time
runTime = end - start
print("论据数量：", argN)
print("关系数量：", relationN)
print("运行时间：", runTime * 1000, "ms")