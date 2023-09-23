import pickle

with open("all_articles.txt") as file:
    articles = file.read()
articles = articles.split("\n\n")

#delete empty elements
articles.pop(0)
articles.pop()

#define an empty structure for forward index
forward_index = {}
#define an empty structure for doc_no
DocNo_dict = {}
#a loop for articles
for i in range(len(articles)):
    rslt = articles[i].split()
    doc_no = rslt.pop(0)
    DocNo_dict[i] = doc_no

    word_counts = {}
    #a loop for words in an article
    for word in rslt:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    forward_index[i] = word_counts

#binary saving doc_no as a pkl file
with open("doc_no.pkl", "wb") as f:
    pickle.dump(DocNo_dict, f)
print("Primary keys has been saved in doc_no.pkl.")

#define an empty structure for inverse_index
inverse_index = {}
for article_no, words_collection in forward_index.items():
    for word, counter in words_collection.items():
        if word in inverse_index:
            inverse_index[word].append([article_no, counter])
        else:
            inverse_index[word] = [[article_no, counter]]
print("Complete extract postings.")

def sort_key(sub_list):
    return sub_list[1]
#sort postings by frequency
for word, the_list in inverse_index.items():
    # 使用键函数对列表进行排序
    sort_list = sorted(the_list, key=sort_key, reverse=True)
    inverse_index[word] = sort_list
#sort inverse_index by alphabetical order
keys = list(inverse_index.keys())
keys.sort()
inverse_index_list = []
for key in keys:
    temp = [key, inverse_index[key]]
    inverse_index_list.append(temp)

#building a binary file for postings
with open('postings.pkl', 'wb') as f:
    pass
#saving postings, return location and size
offsets = {}
for ele in inverse_index_list:
    with open('postings.pkl', 'ab') as f:
        offset_start = f.tell()
        pickle.dump(ele[1], f)
        offset_end = f.tell()
        size = offset_end - offset_start
    offsets[ele[0]] = [offset_start, size]

#prepare for dictionary
postings_index = offsets
keys = list(postings_index.keys())
keys.sort()
postings_index_list = []
for key in keys:
    temp = [key, postings_index[key]]
    postings_index_list.append(temp)

#build dictionary file and root file
with open('term.pkl', 'wb') as f:
    pass
offsets = {}
#500 words for a block
group_size = 500
for i in range(0, len(postings_index_list), group_size):
    with open('term.pkl', 'ab') as f:
        offset_start = f.tell()
        if i + group_size < len(postings_index_list):
            pickle.dump(postings_index_list[i:i + group_size], f)
        else:
            pickle.dump(postings_index_list[i:], f)
        offset_end = f.tell()
        size = offset_end - offset_start
    offsets[postings_index_list[i][0]] = [offset_start, size]

with open('key_index.pkl', 'wb') as f:
    pickle.dump(offsets, f)
print("Completing dictionary and root files.")