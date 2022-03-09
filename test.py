import unittest
import mapcoloring as mc
import copy
# use the test frame work
RED, YELLOW, GREEN, BLUE = 1000, 1001, 1002, 1003
color_list = [RED, YELLOW, GREEN, BLUE]
color_count = [0, 0, 0, 0]

class test_map_coloring(unittest.TestCase):
    '''
    write functions one to one in mapcoloring.py
    '''

    @classmethod
    def setUpClass(self):
        global color_count, color_list
        class Vertex():
            def __init__(self):
                self.num = 0
                self.color = 0
                self.domain = list()
                self.neighbor = list()  # with neighbor



        with open("./gc_78317100510400.txt", "r") as f:  # the file name is here
            raw_data = f.readlines()
        data_temp = list()
        for i in raw_data:
            data_temp.append(i.strip("\n").split())

        color_num = int(data_temp[2][2])
        color_range = color_list[:color_num + 1]
        data_temp = data_temp[4:]  # remove the first 4 as comment or color num

        arc = list()  # edge list, constrain
        vertexlist = list()  # all vertexes list
        vertexset = set()  # use for add vertex
        for i in data_temp:
            if not i:
                continue
            a = copy.copy(i[0].split(','))
            for j in range(2):
                if int(a[j]) not in vertexset:  # if the vertex in list, not add again
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
        self.arc = arc
        self.vertexlist = vertexlist

    def setUp(self):
        print("test start")

    def tearDown(self):
        print("test over")

    def test_next_colored_v(self):
        v = mc.next_colored_v(self.vertexlist)
        self.assertEqual(v,self.vertexlist[0])

    def test_next_color_in_domain(self):
        global color_count, color_list
        c = mc.next_color_in_domain([RED, YELLOW, GREEN, BLUE])
        self.assertEqual(c, RED)

    # def test_map_coloring(self):
    #     m = mc.map_coloring(self.vertexlist,self.arc,0)
    #     self.assertEqual(m,True)

    def test_ac3(self):
        d = mc.ac3(self.vertexlist,self.arc)
        self.assertEqual(d, True)

    # def test_coloring_check(self):
    #     r = mc.coloring_check(self.vertexlist,self.arc)

if __name__ == '__main__':
    unittest.main()
