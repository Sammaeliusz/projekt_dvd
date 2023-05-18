def unlist(l:list):
    if len(l) == 1:
        if isinstance(l[0], (list, tuple)):
            return unlist(l[0])
        else:
            return l[0]
    elif len(l) > 1:
        for x, y in enumerate(l):
            if isinstance(l[0], (list, tuple)):
                l[x] = unlist(y)
        return list(l)
    return None

a = [(2,3,4,5,6)]
print(unlist(a))
