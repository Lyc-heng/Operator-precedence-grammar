# 返回GS所有的状态
def get_state(GS):
    result = []
    for i in GS:
        if i[0] not in result:
            result.append(i[0])
    return result


# 计算得到FIRSTVT集合
def get_FIRSTVT(GS):
    # 获取FIRST中的状态集合
    state = get_state(GS)
    # 初始化FIRST表
    firstvt_table = [[i] for i in state]
    for i in range(len(firstvt_table)):
        result = recur_get_FIRSTVT(firstvt_table[i][0], GS)
        firstvt_table[i].extend(result)
    return firstvt_table


# 递归得到FIRSTVT集合
def recur_get_FIRSTVT(target, GS):
    result = []
    for i in range(len(GS)):
        # 当前要推导的符号和式子相同
        if GS[i][0] == target:
            # 判断是否为终结符号
            if GS[i][1][0].islower() or GS[i][1][0].isalpha() == False:
                add_into_result(result, GS[i][1][0])
            else:
                # 若为非终结符号,进行递归查询
                # 若非终结符号为自身，则不进行递归查询
                if target != GS[i][1][0]:
                    temp = recur_get_FIRSTVT(GS[i][1][0], GS)
                    add_into_result(result, temp)
                # 若后续有终结符号，则也加入
                if len(GS[i][1]) >= 2:
                    if GS[i][1][1].islower() or GS[i][1][1].isalpha() == False:
                        add_into_result(result, GS[i][1][1])
    return result


# 得到LASTVT集合
def get_LASTVT(GS):
    # 获取FIRST中的状态集合
    state = get_state(GS)
    # 初始化FIRST表
    lastvt_table = [[i] for i in state]
    for i in range(len(lastvt_table)):
        result = recur_get_LASTVT(lastvt_table[i][0], GS)
        lastvt_table[i].extend(result)
    return lastvt_table


# 递归得到LASTVT集合
def recur_get_LASTVT(target, GS):
    result = []
    for i in range(len(GS)):
        # 当前要推导的符号和式子相同
        if GS[i][0] == target:
            # 判断是否为终结符号
            if GS[i][1][-1].islower() or GS[i][1][-1].isalpha() == False:
                add_into_result(result, GS[i][1][-1])
            else:
                # 若为非终结符号
                # 若非终结符号为自身，则不进行递归查询
                if target != GS[i][1][-1]:
                    temp = recur_get_LASTVT(GS[i][1][-1], GS)
                    add_into_result(result, temp)
                # 若后续有终结符号，则也加入
                if len(GS[i][1]) >= 2:
                    if GS[i][1][-2].islower() or GS[i][1][-2].isalpha() == False:
                        add_into_result(result, GS[i][1][-2])
    return result


# 向list中添加不重复的元素
def add_into_result(old, add):
    for i in add:
        if i not in old:
            old.extend(i)


# 得到优先关系表
def get_priority_table(firstvt, lastvt, GS):
    # 标记该文法是否符合算法优先文法任一终结符号之间至多只有一种关系
    isflag = True
    state = get_priority_state(firstvt, lastvt)
    # 初始化预测分析表
    table = [["0" for col in range(len(state))] for row in range(len(state))]
    # 寻找=关系
    for i in range(len(GS)):
        # 得到该文法语句长度
        length = len(GS[i][1])
        for x in range(len(GS[i][1])):
            if x + 2 > length - 1:
                break
            if (GS[i][1][x] == GS[i][1][x + 2] and GS[i][1][x] == "#") or (
                    GS[i][1][x] == "(" and GS[i][1][x + 2] == ")"):
                y0, x0 = get_x_y(GS[i][1][x], GS[i][1][x + 2], state)
                if table[y0][x0] != "0":
                    isflag = False
                table[y0][x0] = "="
    # 寻找<关系
    for i in range(len(GS)):
        # 得到该文法的长度
        length = len(GS[i][1])
        for x in range(len(GS[i][1])):
            # 若出现数字越界，跳出
            if x + 1 > length - 1:
                break
            # 如果该符号是终结符号且下一位是非终结符号
            if GS[i][1][x] in state and GS[i][1][x + 1] not in state:
                # 取出FIRSTVT的元素，对关系表进行修改
                temp = firstvt[GS[i][1][x + 1]]
                for q in temp:
                    y0, x0 = get_x_y(q, GS[i][1][x], state)
                    if table[x0][y0] != "0":
                        isflag = False
                    table[x0][y0] = "<"
    # 寻找>关系
    for i in range(len(GS)):
        # 得到该文法的长度
        length = len(GS[i][1])
        for x in range(len(GS[i][1])):
            # 若出现数字越界，跳出
            if x + 1 > length - 1:
                break
            # 如果该符号是终结符号且下一位是非终结符号
            if GS[i][1][x] not in state and GS[i][1][x + 1] in state:

                # 取出FIRSTVT的元素，对关系表进行修改
                temp = lastvt[GS[i][1][x]]
                for q in temp:
                    y0, x0 = get_x_y(q, GS[i][1][x + 1], state)
                    if table[y0][x0] != "0":
                        isflag = False
                    table[y0][x0] = ">"

    return table, state, isflag


# 返回两个符号在表中的位置
def get_x_y(para1, para2, state):
    # 得到行坐标
    y = -1
    x = -1
    for i in range(len(state)):
        if para1 == state[i]:
            y = i
    for i in range(len(state)):
        if para2 == state[i]:
            x = i
    return y, x


# 得到firstvt、lastvt所有的状态
def get_priority_state(firstvt, lastvt):
    state = []
    for key, value in firstvt.items():
        for x in range(0, len(value)):
            if value[x] not in state:
                state.extend(value[x])
    for key, value in lastvt.items():
        for x in range(0, len(value)):
            if value[x] not in state:
                state.extend(value[x])
    return state


# 使用算符优先表分析输入串
def analy_input_string(GS, table, state, input):
    # 初始化分析栈
    ana_shed = []
    # 输入串栈
    input_shed = []
    # 对栈初始化，并将输入串进行倒序入栈
    ana_shed.append("#")
    input_shed.extend(list(reversed(list(input))))
    # 用来打印输出顺序
    show_count = 1
    print("%s %8s %8s %8s %8s" % ("步骤", "栈", "优先关系", "剩余输入串", "移进或规约"))
    while (True):
        print(show_count, end="")
        show_count += 1
        print("%12s" % ("".join(ana_shed)), end="")
        # 充当指针，指向当前栈内参与比较的元素，默认是栈顶
        indicator = len(ana_shed) - 1
        # 如果为非终结符号，向栈底读取字符，至到读取到非终结字符
        if ana_shed[indicator].isupper():
            for i in reversed(range(len(ana_shed) - 1)):
                if ana_shed[i].isupper() == False:
                    indicator = i
                    break
        # 对栈顶符号进行比较,获得两者之间的关系
        y, x = get_x_y(ana_shed[indicator], input_shed[-1], state)
        relationship = table[y][x]
        print("%8s" % (relationship), end="")

        print("%14s" % "".join(list((reversed("".join(input_shed))))), end="")
        if (relationship == "<" or relationship == "=") and len(input_shed) != 1:
            print("%8s" % ("移进"))
        elif relationship == ">":
            print("%8s" % ("归约"))
        else:
            print("%8s" % ("接受"))

        # 如果运算栈内只剩下非终结符号一个，并且输入栈无符号，则规约成功
        if len(ana_shed) == 2 and len(input_shed) == 1:
            break

        # 执行移入操作
        if relationship == "<" or relationship == "=":
            ana_shed.append(input_shed[-1])
            input_shed.pop()
        # 执行规约操作
        elif relationship == ">":
            if indicator == len(ana_shed) - 1:
                # 如果规约符号位于栈顶，则只将栈顶的非终结符号进行规约
                if Statute(GS, ana_shed[indicator], ana_shed[indicator]):
                    ana_shed.pop()
                    ana_shed.append("N")
            else:
                # 如果不位于栈顶，则将运算符左右两边的符号一起进行规约
                if Statute(GS, ana_shed[indicator - 1:indicator + 2], ana_shed[indicator]):
                    ana_shed.pop()
                    ana_shed.pop()
                    ana_shed.pop()
                    ana_shed.append("N")


def Statute(GS, input, symbol):
    # 用来记录标志位规约情况

    for i in range(len(GS)):
        if len(GS[i][1]) == len(input) and symbol in GS[i][1]:
            # 用来进行符号规约
            count = 0
            for x in range(len(GS[i][1])):
                if GS[i][1][x] == symbol:
                    count += 1
                elif str(GS[i][1][x]).isupper() and str(input[x]).isupper():
                    count += 1
            # 查看是否能进行规约
            if count == len(GS[i][1]):
                return True
    return False


if __name__ == '__main__':
    # 测试样例文法
    GS = [["A", "#E#"],
          ["E", "E+T"],
          ["E", "T"],
          ["T", "T*F"],
          ["T", "F"],
          ["F", "P|F"],
          ["F", "P"],
          ["P", "(E)"],
          ["P", "i"]]
    input_str = "i+i#"

    print("进行构造的文法G[S]")
    for i in GS:
        print("%s -> %s" % (i[0], i[1]))
    print("===============================================", end="\n")
    # 得到FIRSTVT集合
    firstvt = {}
    output = get_FIRSTVT(GS)
    for i in range(len(output)):
        firstvt[str(output[i][0][0])] = output[i][1:]
    print("该文法的FIRSTVT:")
    for key, value in firstvt.items():
        print("FIRSTVT(%s) = {%s}" % (key, str(value)[1:-1]))
    print("===============================================", end="\n")

    # 得到LASTVT集合
    lastvt = {}
    output = get_LASTVT(GS)
    for i in range(len(output)):
        lastvt[str(output[i][0][0])] = output[i][1:]
    print("该文法的LASTVT集合:")
    for key, value in lastvt.items():
        print("LASTVT(%s) = {%s}" % (key, str(value)[1:-1]))
    print("===============================================", end="\n\n")

    # 得到算符优先关系表
    table, state, isFlag = get_priority_table(firstvt, lastvt, GS)
    print("%24s" % ("算符优先关系表"))
    print("---------------------------------------------------------")
    for i in state:
        print("%8s" % i, end="")
    print("")
    for i in range(len(table)):
        print("%s" % state[i], end="")
        print("%7s" % table[i][0], end="")
        for x in table[i][1:]:
            print("%8s" % x, end="")
        print("")
    print("该文法是否属于算符优先文法:%s" % (str(isFlag)), end="\n\n")

    # 对文法进行算符分析
    print("接下来对输入串 %16s 进行规约" % (input_str))
    print("---------------------------------------------------")
    analy_input_string(GS, table, state, input_str)
