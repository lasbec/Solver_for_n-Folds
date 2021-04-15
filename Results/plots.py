from res import *

# base = rs == ('version', '1')
# attr = 'delta'
# for i in range(base.min(attr), base.max(attr)):
#     sl = base == (attr, i)
#     if len(sl.passed) > 0:
#         print(f"{attr} {i}: {len(sl.passed)}/{len(sl)}            --{sl.max('roh_sum')}")


v1 = rs.where("res.r > 3 or res.s > 3") == ('version', '1')
v2 = rs.where("res.r > 3 or res.s > 3") == ('version', '2')
attr = 's'

print(f"v1 passed {len(v1.passed)}")
print(f"v2 passed {len(v2.passed)}\n")

zip12 = []
for c1 in v1.passed:
    for c2 in v2.passed:
        if c1.input == c2.input:
           zip12.append((c1,c2)) 


print(f"total zip: {len(zip12)}")

v1_faster = ResList([c1 for c1, c2 in zip12 if c1.time_use < c2.time_use ])
v2_faster = ResList([c2 for c1, c2 in zip12 if c1.time_use > c2.time_use ])
print(f"c1 faster {len(v1_faster)}")
for attr in ['roh_sum', 'delta', 'n', 'r', 's','t'] :
    print(f"c1 faster avg {attr}: {v1_faster.avg(attr)}")

print(" ")
print(f"c2 faster {len(v2_faster)}")
for attr in ['roh_sum', 'delta', 'n', 'r', 's','t'] :
    print(f"c2 faster avg {attr}: {v2_faster.avg(attr)}")


print(f"c1 less mem {len([0 for c1, c2 in zip12 if c1.mem_use < c2.mem_use ])}")
print(f"c2 less mem {len([0 for c1, c2 in zip12 if c1.mem_use > c2.mem_use ])}")

