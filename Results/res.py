import re
import os
import json

class NFILP:
    def __init__(self, path):
        with open(path, 'r') as f:
            txt = f.readlines()
            n, r, s, t = [int(i) for i in txt[0].split(' ')]
            
            l  = [int(i) for i in txt[1].split(' ')]
            u  = [int(i) for i in txt[2].split(' ')]
            b  = [int(i) for i in txt[3].split(' ')]
            c  = [int(i) for i in txt[4].split(' ')]

            assert len(l) == n*t
            assert len(u) == n*t
            assert len(b) == r + n*s
            assert len(c) == n*t

            self.txt = "".join(txt)

            self.roh = max([u[i]-l[i] for i in range(n*t)])
            self.roh_sum = sum([u[i]-l[i] for i in range(n*t)])

            self.delta = 0
            for line in txt[5:]:
                i_lst = [int(i) for i in line.split(' ')]
                self.delta = max([self.delta] + i_lst)

class Result:
    def __init__(self, x ,from_json=False):
        if from_json:
            j = x
            # print(j.values())
            # print(type(j))
            for name, value in j.items():
                setattr(self, name, value)
        else:
            proc_name = x
            # splt = x.split('_')[0]
            # self.n = int(splt[3])
            # self.r = int(splt[4])
            # if len(splt) > 7:
            #     self.s = 10
            #     self.t = int(splt[7])
            # else:
            #     self.s = int(splt[5])
            #     self.t = int(splt[6])

            self.n = int(proc_name.split('_')[0][1:])
            self.r = int(proc_name.split('_')[1])
            self.s = int(proc_name.split('_')[2])
            self.t = int(proc_name.split('_')[3].split('B')[0])
            if re.search(".*V[a-z0-9A-Z]*$", proc_name):
                self.version = re.findall(".*V([a-z0-9A-Z]*)$", proc_name)[0]
            else:
                print("Warn default version 1")
                print(proc_name)
                self.version = "1"
            with open(f"{ResList.err_path()}/{proc_name}.err", 'r') as stderr:
                with open(f"{ResList.out_path()}/{proc_name}.out", 'r') as stdout:
                    with open(f"{ResList.script_path()}/{proc_name}.sbatch", 'r') as batchf:
                        err_str = stderr.read()
                        out_str = stdout.read()
                        batch_str = batchf.read()


                        inp_file_path = "./myCases/" + re.findall("~/IntOpt/myCases/(.*)", batch_str)[0]
                        nfilp = NFILP(inp_file_path)
                        self.delta = nfilp.delta
                        self.input = nfilp.txt
                        self.roh = nfilp.roh
                        self.roh_sum = nfilp.roh_sum

                        self.time_ex = bool(re.search("DUE TO TIME LIMIT", err_str))
                        if not self.time_ex:
                            try:
                                self.out = re.findall("([ -:0-9a-zA-Z\n]*)\nSlurm Job Summary", out_str)[0]
                                self.err = err_str

                                self.mem_ex = bool(re.search("been killed by the cgroup out-of-memory handler", err_str))
                                self.passed = not self.mem_ex

                                self.mem_use = float(re.findall("MaxRSS = [0-9]*. [(] ([0-9.]*)M [)]", out_str)[0])
                                self.time_use = int(re.findall("[. ]*RunTime = [0-9][0-9]:[0-9][0-9]:[0-9][0-9] [(] ([0-9]*)s [)]", out_str)[0])

                                self.mem_giv = float(re.findall("MinMemoryNode = [0-9]*. [(] ([0-9.]*)M [)]", out_str)[0])
                                self.time_giv = int(re.findall("[. ]*Timelimit = [0-9][0-9]:[0-9][0-9]:[0-9][0-9] [(] ([0-9]*)s [)]", out_str)[0])
                                
                            except IndexError as e:
                                print(f"could not load {proc_name} with Error: {e}")
                        else:
                            self.passed = False
        
    def to_json(self):
        return self.__dict__

class ResList:
    pre = ""
    post = ""

    def __init__(self,lst=None, reload=False):
        if lst is not None:
            self.results = lst
        elif reload:
            self.results = [Result(file_name[:-4]) for file_name in os.listdir(ResList.out_path())]
            json_results = [r.to_json() for r in self.results]
            with open(self.json_path(),'w') as j_file:
                json.dump({'res':json_results}, j_file)
        else:
            with open(self.json_path(), 'r') as j_file:
                json_results = json.load(j_file)['res']
            self.results = [Result(json_r, from_json=True) for json_r in json_results]

    
    @classmethod
    def out_path(cls):
        return f"./{cls.pre}stdouts{cls.post}"
    
    @classmethod
    def err_path(cls):
        return f"./{cls.pre}stderrs{cls.post}"

    @classmethod
    def script_path(cls):
        return f"./{cls.pre}sbatches{cls.post}"
    
    @classmethod
    def json_path(cls):
        return f"./{cls.pre}results{cls.post}.json"

    def __eq__(self, x):
        attr, val = x
        return ResList([res for res in self if getattr(res, attr) == val])
    
    def __ne__(self, x):
        attr, val = x
        return ResList([res for res in self if getattr(res, attr) != val])
    
    def __le__(self, x):
        attr, val = x
        return ResList([res for res in self if getattr(res, attr) <= val])
    
    def __lt__(self, x):
        attr, val = x
        return ResList([res for res in self if getattr(res, attr) <  val])
    
    def __ge__(self, x):
        attr, val = x
        return ResList([res for res in self if getattr(res, attr) >= val])

    def __gt__(self, x):
        attr, val = x
        return ResList([res for res in self if getattr(res, attr) >  val])
        
    def __getitem__(self, i):
        return self.results[i]
    
    def __iter__(self):
        return self.results.__iter__()
    
    def __len__(self):
        return len(self.results)

    def get(self, n, r, s, t):
        return ResList([res for res in self.results if res.n==n and res.s==s and res.r==r and res.t==t])

    @property
    def attr(self):
        return ResList([res for res in self if hasattr(res, "mem_use")])
    
    @property
    def passed(self):
        return ResList([res for res in self.noTimeEx if not res.mem_ex])
    
    @property
    def failed(self):
        return ResList([res for res in self if res.time_ex or res.mem_ex])

    @property
    def noTimeEx(self):
        return ResList([res for res in self.results if not res.time_ex])

    @property
    def groups(self):
        return dict([((n,r,s,t), self.get(n,r,s,t) ) for n in range(1,6) for r in range(1,6) for s in range(1,6) for t in range(1,6)])

    def orderBy(self, attr, desc=True):
        self.results.sort(key=attr)

    def where(self, cond_str):
        return ResList([res for res in self.results if eval(cond_str)])

    def aggregate(self, attr, ag):
        return ag([getattr(res,attr) for res in self.results])

    def sum(self, attr, fallback=0):
        if len(self) == 0:
            return fallback
        return self.aggregate(attr, sum)

    def avg(self, attr, fallback=0):
        if len(self.results) == 0:
            return fallback
        return self.sum(attr)/len(self.results)


    def max(self, attr, fallback=0):
        if len(self) == 0:
            return fallback
        return self.aggregate(attr, max)

    def min(self, attr, fallback=0):
        if len(self) == 0:
            return fallback
        return self.aggregate(attr, min)
    
    def print(self, *attr):
        if attr == []:
            for res in self:
                print(str(res.__dict__))
        else:
            for res in self:
                print(*[getattr(res, a) for a in attr ])
    
    def __repr__(self):
        return f"<ResList" + "\n"\
               f"Laufend  : " + str(len(self.where("not res.time_ex and not hasattr(res, 'mem_use')"))) + "\n"\
               f"Runntime : " + str(len(self.where("res.time_ex"))) + "\n"\
               f"Memory   : " + str(len(self.noTimeEx.where("res.mem_ex"))) + "\n"\
               f"Vollendet: " + str(len(self.passed)) + "\n"\
               f"--------------------------" +"\n"\
               f"Gesamt   : " + str(len(self)) +" >"




rs = ResList()



v1 = rs == ('version', '1')
v2 = rs == ('version', '2')
brute = rs == ('version', 'brute')

v1p = v1.passed
v2p = v2.passed

def avg(lst):
    return sum(lst)/len(lst)

# Only passed rest from basis cases
def plt(lst, attr, ag_func=max, y_attr='time_use'):
    mi = lst.min(attr)
    ma = lst.max(attr)
    ys = [(lst == (attr, i)).aggregate(y_attr, ag_func) for i in range(mi, ma+1) if len(lst == (attr,i)) > 0]
    xs = [ i                 for i in range(mi, ma+1) if len(lst == (attr,i)) > 0]
    return xs, ys



