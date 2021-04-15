from matplotlib.pyplot import *
from res import *


def plot_increase(inc_attr, offset=0):                
    attr_conf = {
                'n'    : f"== {3}",
                'r'    : f"< {None}",
                's'    : f"< {3}",
                't'    : f"< {3}",
                'delta': f"< {961}", # < 40 / 961
                'roh'  : f"< {47}" # < 21 /47
                }
    del attr_conf[inc_attr]

    base = rs.where(" and ".join([f"res.{attr} {cond}" for attr, cond in attr_conf.items()]))
    v1 = base == ('version',"1")
    v2 = base == ('version',"2")

    # x values
    xs = range(base.min(inc_attr) + offset, base.max(inc_attr) + 1)


    for a in xs:
        print(f"{a}: {len(v1 == (inc_attr, a))}")

    to_plot = {
        # runtime avg
          "pure algorithm" : [(v1.passed == (inc_attr, i)).avg('time_use', fallback=None) for i in xs]
        , "zero column check" : [(v2.passed == (inc_attr, i)).avg('time_use', fallback=None) for i in xs]

        # # runtime max
        # , "run max 1" : [(v1.passed == (inc_attr, i)).max('time_use') for i in xs]
        # , "run max 2" : [(v2.passed == (inc_attr, i)).max('time_use') for i in xs]

        # # runtime min
        # , "run min 1" : [(v1.passed == (inc_attr, i)).min('time_use', fallback=-50) for i in xs]
        # , "run min 2" : [(v2.passed == (inc_attr, i)).min('time_use', fallback=-50) for i in xs]

        # # memory avg
        # , "mem avg 1" : [(v1.passed == (inc_attr, i)).avg('mem_use', fallback=10000) for i in xs]
        # , "mem avg 2" : [(v2.passed == (inc_attr, i)).avg('mem_use', fallback=10000) for i in xs]

        # # memory max
        # , "mem max 1" : [(v1.passed == (inc_attr, i)).max('mem_use') for i in xs]
        # , "mem max 2" : [(v2.passed == (inc_attr, i)).max('mem_use') for i in xs]
        # # failed %
        # , "fail 1"    : [(len(v1.failed == (inc_attr, i))*500/len(v1 == (inc_attr, i))) for i in xs]
        #  "test failures"    : [(len(v2.failed == (inc_attr, i))/len(v2 == (inc_attr, i))) for i in xs]
        #  "fail total"    : [(len(v2.failed == (inc_attr, i))) for i in xs]

        # , "passed 1"    : [(len(v1.passed == (inc_attr, i))*500/len(v1 == (inc_attr, i))) for i in xs]
        # , "passed 2"    : [(len(v2.passed == (inc_attr, i))*500/len(v2 == (inc_attr, i))) for i in xs]
        # , "passed total"    : [(len(v2.passed == (inc_attr, i))) for i in xs]

        # genaral
        # , "case num 1": [len(v1 == (inc_attr, i)) for i in xs]
        # , "delta max" : [(v1 == (inc_attr, i)).max('delta') for i in xs]
        # , "delta avg" : [(v1 == (inc_attr, i)).avg('delta')*100 for i in xs]
        # , "delta min" : [(v1 == (inc_attr, i)).avg('delta') for i in xs]

        # , "roh max" : [(v1 == (inc_attr, i)).max('roh') for i in xs]
        # , "roh avg" : [(v1 == (inc_attr, i)).avg('roh')*100 for i in xs]
        # , "roh min" : [(v1 == (inc_attr, i)).avg('roh') for i in xs]

        # , "roh_sum max" : [(v1 == (inc_attr, i)).max('roh_sum') for i in xs]
        # , "roh_sum avg" : [(v1 == (inc_attr, i)).avg('roh_sum') for i in xs]
        # , "roh_sum min" : [(v1 == (inc_attr, i)).avg('roh_sum') for i in xs]
    }

    colors = ["b", "r", "g", "y"]
    i = 0
    for lbl, lst in to_plot.items(): 
        # plot(xs, lst, f"{colors[i]}", label=lbl)
        # plot(xs, lst, f"o{colors[i]}")
        plot(xs, lst, label=lbl)
        i += 1

    fontsize = 25
    rc('font', size=fontsize) 

    xlabel(f"{inc_attr}", fontsize=fontsize)
    ylabel('average run time in seconds', fontsize=fontsize+3)
    # ylabel('failed tests in %', fontsize=fontsize+3)
    xticks(xs, xs, fontsize=fontsize)
    yticks(fontsize=fontsize)
    
    x = {
        'n'    : attr_conf.get('n') ,
        'r'    : attr_conf.get('r') ,
        's'    : attr_conf.get('s') ,
        't'    : attr_conf.get('t') 
        }
    del x[inc_attr]
    # Avarage run time for passed tests.\nIncreasing {inc_attr}   
    # title(", ".join([f"{attr} {cond}" for attr, cond in x.items()]) )
    title("n=3, s < 3, t < 3")
    # title(f"Increasing {inc_attr}   (" +", ".join([f"{attr} {cond}" for attr, cond in attr_conf.items()]) + ")")
    legend()
    show()


plot_increase('r')