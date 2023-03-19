from random import randint, shuffle
def crypt(id):
    id = int(id)
    id += 524288
    id = bin(id)
    id = id[2::]
    txt = ""
    hext = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    mhex = ['1', '3', '7', '8', 'a', '4', '5', '2', '6', 'e', '9', 'c', 'f', '0', 'd', 'b']
    for i in id:
        txt += i+str(randint(0, 1))+str(randint(0, 1))+str(randint(0, 1))
    id = int(txt, 2)
    id = hex(id)
    id = id[2::]
    for i in range(len(hext)):
        id.replace(hext[i], mhex[i])
    txt = ""
    for i in id:
        txt += i+mhex[randint(0, 15)]+mhex[randint(0, 15)]
    id = txt
    id = int(id, 16)
    key1 = 168432651498424765448654865149865498649851498413689
    id = id^key1
    id = str(id)
    dect = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    mdec = ['4', '3', '9', '0', '2', '5', '8', '1', '7', '6']
    for i in range(len(dect)):
        id.replace(dect[i], mdec[i])
    id = int(id)
    key2 = 735811653148354853646435786315423453246988649872545
    id = id^key2
    return id
def decrypt(id):
    key1 = 168432651498424765448654865149865498649851498413689
    key2 = 735811653148354853646435786315423453246988649872545
    dect = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    mdec = ['4', '3', '9', '0', '2', '5', '8', '1', '7', '6']
    hext = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    mhex = ['1', '3', '7', '8', 'a', '4', '5', '2', '6', 'e', '9', 'c', 'f', '0', 'd', 'b']
    id = id^key2
    id = str(id)
    for i in range(len(dect)):
        id.replace(mdec[i], dect[i])
    id = int(id)
    id = id^key1
    id = hex(id)
    id = id[2::]
    txt = ""
    for i in range(len(id)):
        if i%3==0:
            txt+=id[i]
    id = txt
    for i in range(len(hext)):
        id.replace(mhex[i], hext[i])
    id = int(id, 16)
    id = bin(id)
    id = id[2::]
    txt =""
    for i in range(len(id)):
        if i%4==0:
            txt+=id[i]
    id = txt
    id = int(id, 2)
    id -= 524288
    return id