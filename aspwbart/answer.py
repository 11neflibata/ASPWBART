# 将 symbols 中的每个 atom 的类型转化为字符串，得到的形式如’in(2)‘
def atom_to_str(atom):
    args = [str(arg) for arg in atom.arguments]
    atom_args = '(' + f"{', '.join(args)}" + ')'
    return atom.name + atom_args

# 将集合与现有集合进行对比，只保留最大集合
def only_keep_the_max(list, lists):
    for i, l in enumerate(lists):
        # 若包含已有的集合，则删除被包含的集合
        if set(l).issubset(set(list)):
            is_list_max = True
            del lists[i]
        # 若被包含，则该集合不做考虑
        elif set(list).issubset(set(l)):
            return
    lists.append(list)

# 找出最大包含集合，输入参数为 models，返回类型为 list[list1, list2.......]，例如 [['in(1)', 'in(3)'], ['in(1)', 'in(4)']
def max_contained_model_in_all_models(models):
    max_contained_models = []
    for model in models:
        if model.optimality_proven:
            pre_li = []
            for atom in model.symbols(shown=True):
                pre_li.append(atom_to_str(atom))
            only_keep_the_max(pre_li, max_contained_models)
    return max_contained_models

# 打印最大包含集合，输入参数为 models
def print_max_model(models):
    for max_contained_models in max_contained_model_in_all_models(models):
        print("Result：")
        for item in max_contained_models:
            print(item)

# 打印optimization
def print_optimization(models):
    for model in models:
        if model.optimality_proven:
            print(f"Optimization: {' '.join(map(str, model.cost))}")
            break
