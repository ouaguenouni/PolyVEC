
def merge_dict(d_list):
    D= {}
    for d in d_list:
        for k in d:
            D[k] = D.get(k, []) + [d[k]]
    return D

