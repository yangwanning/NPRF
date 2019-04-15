import subprocess as sp
import argparse
import multiprocessing
import sys



def poolcontext(*args, **kwargs):
  pool = multiprocessing.Pool(*args, **kwargs)
  yield pool
  pool.terminate()

def grid_search_run(grid):
    b=grid[0]
    doc=grid[1]
    term=grid[2]
    run_args = 'bin/trec_terrier.sh' + ' ' + '-r' + ' ' + '-q' + ' ' + '-c' + ' ' + str(b) + ' ' + '-Dexpansion.documents=' + str(doc) + ' ' + '-Dexpansion.terms=' + str(term) + ' ' + '-Dtrec.results.file=' + str(b) + '_' + str(doc) + '_' + str(term) + '.res'
    s = sp.Popen(run_args, stdout=sp.PIPE, shell=True, encoding='utf-8')
    print("finish:{}".format([b,doc,term]))

def grid_search_eval(grid):
    b=grid[0]
    doc=grid[1]
    term=grid[2]
    global cur_map
    # obtain MAP
    evaluate_args = 'bin/trec_terrier.sh' + ' ' + '-e' + ' ' + str(b) + '_' + str(doc) + '_' + str(term) + '.res'
    o = sp.Popen(evaluate_args, stdout=sp.PIPE, shell=True, encoding='utf-8')
    out = o.communicate()
    # cur_map = out[0].strip('\n').split(' ')[14]
    try:
        cur_map = out[0].strip('\n').split(' ')[14]
    except:
        print(out)
    return cur_map,[b,doc,term]
b_range = [0.6,0.65,0.7,0.75,0.8]
doc_range = [5,8,10,12,15]
term_range = [25,30,35,40,45,50]
pool = multiprocessing.Pool(processes=4)
grid = [(b, doc,term) for b in b_range for doc in doc_range for term in term_range]
pool_outputs = pool.map(grid_search_eval, grid)

best = 0
for i in pool_outputs:
    if float(i[0]) > best:
        best = float(i[0])
        best_para = i[1]

print("Best score:{:.4f}".format(best))
print("Best parameters:{}".format(best_para))


# evaluate_args = 'bin/trec_terrier.sh'+' '+ '-e' +' '+ str(b) + '_' + str(doc) + '_' +str(term) + '.res'
# o = sp.Popen(evaluate_args, stdout=sp.PIPE, shell=True, encoding='utf-8')
# out = o.communicate()
# # o.stdout.close()
# print(out[0].strip('\n').split(' ')[14])
