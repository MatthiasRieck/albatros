from example_brach import run

import cProfile
import pstats
import io
from pstats import SortKey


pr = cProfile.Profile()
pr.enable()

run()

pr.disable()
s = io.StringIO()
sortby = SortKey.TIME
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.reverse_order()
ps.print_stats()
print(s.getvalue())
