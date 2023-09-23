import pickle
import time

#start loading
old_time = time.time()

#open root and a file for document_no.
with open('key_index.pkl', 'rb') as f:
    key_index = pickle.load(f)

with open("doc_no.pkl", "rb") as tf:
    docNo = pickle.load(tf)

#end loading and print the loading time
current_time = time.time()
loading_time = current_time-old_time
print("Loading time is ", loading_time)

#take postings for a word
def my_search_word(search_word):
    # find the root
    keys = list(key_index.keys())
    keys.sort()
    for i in range(len(keys)):
        if keys[i] > search_word:
            break
    key = keys[i - 1]

    # find the word's position
    with open('term.pkl', 'rb') as f:
        f.seek(key_index[key][0])
        data = f.read(key_index[key][1])
        term = pickle.loads(data)
    temp_list = []
    for ele in term:
        temp_list.append(ele[0])
    try:
        the_index = temp_list.index(search_word)
    except ValueError:
        print(search_word + " has not found!")
        return None

    #find location of postings and load
    lea = term[the_index][1][0]
    size = term[the_index][1][1]
    with open('postings.pkl', 'rb') as f:
        f.seek(lea)
        data = f.read(size)
        obj = pickle.loads(data)

    #return postings
    return obj

#merge postings for two words
def merge_ps(p1, p2):
    if p1 and p2:
        p_inter_list = []
        for ele1 in p1:
            for ele2 in p2:
                if ele1[0] == ele2[0]:
                    p_inter_list.append([ele1[0],ele1[1] + ele2[1]])
        return p_inter_list
    else:
        return []

#define a function for ranking by the second element of sublist
def sort_key1(sub_list):
    return sub_list[1]

#define a function for ranking by len
def sort_key2(sub_list):
    return len(sub_list)

#search and print
while True:
    query = input("Please enter the words you want to search for. Enter 'I done' to exit the program.\n")
    if query.lower() == "i done":
        break
    query = query.lower()
    words_list = query.split()

    #start searching
    old_time = time.time()

    #produce the total postings
    if len(words_list) == 1:
        result = my_search_word(words_list[0])
    else:
        list_postings = []
        for i in range(len(words_list)):
            list_postings.append(my_search_word(words_list[i]))
        sort_list_postings = sorted(list_postings, key=sort_key2, reverse=False)
        #start from the shortest postings
        result = sort_list_postings[0]
        for i in range(len(words_list)-1):
            p2 = sort_list_postings[i+1]
            result = merge_ps(result, p2)

    #rank and print
    if result:
        sort_result = sorted(result, key=sort_key1, reverse=True)
        for rslt in sort_result:
            doc_no = docNo[rslt[0]]
            print(doc_no, rslt[1])

    else:
        print("There is no result.")

    #end searching and print searching and printing time
    current_time = time.time()
    searching_time = current_time - old_time
    print("The searching and printing time is ", searching_time)

    

