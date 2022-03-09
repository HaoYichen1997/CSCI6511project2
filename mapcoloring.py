import copy

RED, YELLOW, GREEN, BLUE = 1000, 1001, 1002, 1003
color_list = [RED, YELLOW, GREEN, BLUE] # create some color as int
color_count = [0, 0, 0, 0]   # list count vertexes color
'''
# my heuristic in choosing next vertex is MRV
# my heuristic in choosing next value(color) is choose the most valid color in map

# this step use color count list, always choose biggest number
'''
class Vertex():  #one vertex
    def __init__(self):
        self.num = 0
        self.color = 0
        self.domain = list()
        self.neighbor = list()  # its neighbor



def next_colored_v(vertexlist):  #MRV
    '''
     my heuristic in choosing next vertex is min remaining values
     after color one vertex, algorithm will choose the next
     vertex with least possible color , least num of domain
    :param vertexlist:
    :return: a vertex
    '''
    min_domain_v = 0
    min_num = 100000  # python3 no inf int, if need bigger, ust float("inf") and int()
    for i in vertexlist:
        if i.color == 0 and len(i.domain) < min_num:
            min_num = len(i.domain)
            min_domain_v = i
    return min_domain_v

def next_color_in_domain(domain:list):
    '''
    :param domain:
    :return: next value(color) is choose the most valid color in map
    '''
    global color_count,color_list
    most_color_num = -1
    for i in domain:  # i is a color
        n = color_list.index(i)  # n is int, e.g. RED is 0
        if color_count[n] > most_color_num:
            most_color_num = color_count[n]
            most_color = i
    return most_color

def map_coloring(vertexlist, arc, num:int):  #use backtrack
    '''

    :param vertexlist:
    :param arc:
    :param num: the number how many vertexes are colored
    :return: True and the color updated in vertexlist
    False can not generate a colored map
    '''
    if num == len(vertexlist):  # finish then return
        return vertexlist

    vlist_copy = copy.deepcopy(vertexlist)  # make copy for backtrack
    arc_copy = copy.deepcopy(arc)

    while num < len(vertexlist):
        v = next_colored_v(vertexlist)
        i = next_color_in_domain(v.domain)
        v.color = i
        global color_list,color_count
        n = color_list.index(i)
        color_count[n] += 1
        v.domain.clear()
        v.domain.append(i)
        num += 1  # color a vertex more
        if ac3(vertexlist, arc):  # if pass the ac3, do recursion
            result = map_coloring(vertexlist, arc, num)
            if result:  # have a non null result
                return result  # color i return
        # if not return, this color in domain is invalid
        # go back to the copy
        vertexlist = copy.deepcopy(vlist_copy)
        vertexlist[v.num-1].domain.remove(i)   # i not work
        color_count[n] -= 1
        num -= 1  # cancel
        arc = copy.deepcopy(arc_copy)
    return False


def ac3(vertexlist, arc):
    '''
    arc is a constrain ac3 use to update domain in forward tracking
    based on slide. first generate a queue with the useful arc
    if two vertexes are both colored, do not add in queue
    pop the first and if Xi makes no valid domain of Xj
    remove Xi and add i's neighbor in queue
    if all v has at least one domain, return True
    :param vertexlist:
    :param arc:
    :return:
    '''
    queue = list()
    for i in arc:
        v1 = vertexlist[i[0]-1]; v2 = vertexlist[i[1]-1]
        if not(v1.color !=0 and v2.color != 0):  # if 2 v both colored, not add queue
            queue.append(i)
    while len(queue) != 0:
        edge = queue.pop(0)
        for i in range(2):  # check one edge two vertex
            if i == 1:
                edge = [edge[1], edge[0]]
            valid_value = False   # is xi domain valid ? False at start
            for domain_i in vertexlist[edge[0]-1].domain:  # vnum = order in list +1
                valid_value = False
                for domain_j in vertexlist[edge[1]-1].domain:  # domain i,j is a color
                    if domain_j != domain_i:  # if have a valid domain in  Xj
                        valid_value = True
                if not valid_value:  # if no valid value for xj domain to this xi
                    vertexlist[edge[0]-1].domain.remove(domain_i)  # vlist[0] = v1
                    for n in vertexlist[edge[0]-1].neighbor:  # n is num in vlist, no -1
                        if n != edge[1] :
                            queue.append([vertexlist[edge[0]-1].num, n])

                if len(vertexlist[edge[0]-1].domain) == 0:  # no valid value for v edge[0]
                    return False


    return True

def coloring_check(vertexlist, arc):
    '''
    traverse arc,
    to check if two node in one edge in different color
    :param vertexlist:
    :param arc:
    :return:
    '''
    v_color = list()
    print("check start")
    for vertex in vertexlist:
        if vertex.color in color_list:
            v_color.append(vertex.color)
        else:
            print(vertex.num, "color is not in list")
    for i in arc:
        if v_color[i[0]-1] == v_color[i[1]-1]:
            print(i, "not valid")
    print("check over")

if __name__ == "__main__":
    #read file
    with open("./gc_78317100510400.txt", "r") as f:   # the file name is here
        raw_data = f.readlines()
    data_temp = list()
    for i in raw_data:
        data_temp.append(i.strip("\n").split())

    # create range of color
    color_num = int(data_temp[2][2])
    print(f"color num:{color_num}")
    color_range = color_list[:color_num+1]
    data_temp = data_temp[4:]  # remove the first 4 as comment or color num

    arc = list() # edge list, constrain
    vertexlist = list()  # all vertexes list
    vertexset = set()  # use for add vertex
    for i in data_temp:
        if not i:
            continue
        a = copy.copy(i[0].split(','))
        for j in range(2):
            if int(a[j]) not in vertexset: # if the vertex in list, not add again
                v = Vertex()
                v.num = int(a[j])
                v.domain = copy.deepcopy(color_range)
                if j == 0:
                    v.neighbor.append(int(a[1]))
                else:
                    v.neighbor.append(int(a[0]))
                vertexlist.append(v)
                vertexset.add(int(a[j]))
            else:  # if the vertex in list, add new neighber
                for w in vertexlist:
                    if w.num == int(a[j]):
                        if j == 0:
                            w.neighbor.append(int(a[1]))
                        else:
                            w.neighbor.append(int(a[0]))
        arc.append([int(a[0]), int(a[1])])  # add arc
    # the vertex list is sorted and no gap in raw data, good!
    # if first vertex is 0, put it to 1, add 1 in all v num and neighbor
    zero_to_one = False  # the flag help to show result
    if 0 in vertexset:
        zero_to_one = True
        for i in vertexlist:
            i.num += 1
            for n in range(len(i.neighbor)):
                i.neighbor[n] += 1
            i.neighbor.sort()
        for edge in arc:
            edge[0] += 1
            edge[1] += 1

    print("arc:", arc)
    print("vset:", vertexset)
    for i in vertexlist:
        print(i.num, i.neighbor)
    print("number of vertexes:",len(vertexlist))

    if map_coloring(vertexlist, arc, 0):
        print("color a valid map")
    else:
        print("can not create a valid map")

    # print the result of (vertex:color)
    for i in vertexlist:
        if zero_to_one:
            print(f"{i.num-1} color is {i.color}")
        else:
            print(f"{i.num} color is {i.color}")

    coloring_check(vertexlist,arc)

