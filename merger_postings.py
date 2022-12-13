from indexing import Posting

def merge_phrase(x:list[Posting], y: list[Posting], offset):
    i = 0
    j = 0
    res_pos_list = []
    while(i<len(x) and j <len(y)):
        if x[i].doc_id == y[j].doc_id:
            positions_x = x[i].position_list
            positions_y = y[j].position_list
            posidx = 0 #ids for positions list of x and y
            posidy = 0

            while(posidx < len(positions_x) and posidy < len(positions_y)):
                if positions_y[posidy] - positions_x[posidx] == offset:
                    if x[i] not in res_pos_list:
                        res_pos_list.append(x[i])
                    posidx += 1
                    posidy += 1
                else:
                    if positions_y[posidy] < positions_x[posidx]:
                        posidy += 1
                    elif positions_y[posidy] > positions_x[posidx]:
                        posidx += 1
                    else:
                        posidy += 1
                        posidx += 1
            i+=1
            j+=1

        elif x[i].doc_id < y[j].doc_id:
            i += 1
        else:
            j += 1

    return res_pos_list


def and_merge(x: [Posting], y: [Posting]):
    i = 0
    j = 0
    merge_posting = []
    while(i < len(x) and j < len(y)):
        if x[i].doc_id == y[j].doc_id:
            merge_posting.append(x[i])
            i += 1
            j += 1
        elif x[i].doc_id > y[j].doc_id:
            j += 1
        elif x[i].doc_id < y[j].doc_id:
            i += 1
    return merge_posting


def or_merge(x:[Posting], y:[Posting]):
    i = 0
    j = 0
    merged_posting = []
    while(i <len(x) and j < len(y)):
        if x[i].doc_id == y[j].doc_id:
            merged_posting.append(x[i])
            i+=1
            j+=1
        elif x[i].doc_id > y[j].doc_id:
            merged_posting.append(y[j])
            j += 1
        elif x[i].doc_id < y[j].doc_id:
            merged_posting.append(x[i])
            i+=1
    while i < len(x):
        merged_posting.append(x[i])
        i += 1
    while j < len(y):
        merged_posting.append(y[j])
        j += 1
    return merged_posting


def and_not_merge(x:[Posting], y:[Posting]):
    i = 0
    j = 0
    merged_posting = []
    while(i<len(x) and j< len(y)):
        if x[i].doc_id == y[j].doc_id:
            i+=1
            j+=1
        elif x[i].doc_id < y[j].doc_id:
            merged_posting.append(x[i])
            i+=1
        elif x[i].doc_id > y[j].doc_id:
            j+=1
#remaing data of that term add it back
    while i<len(x):
        merged_posting.append(x[i])
        i+=1
    return merged_posting
