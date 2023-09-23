import re


#delete useless terms
def my_delete(ori_str, delete_str):
    for ele_str in delete_str:
        ori_str = ori_str.replace(ele_str, "")
    return ori_str


#read xml file
with open("wsj.xml") as file:
    text = file.read()

#list of useless terms
delete_list = ["<DOC>", "</DOC>", "<HL>", "</HL>", "<DD>", "</DD>", "<SO>", "(J)", "</SO>", "<IN>", "</IN>", "<DATELINE>",
               "</DATELINE>", "<TEXT>",
               "</TEXT>", "</DOCNO>"]
text = my_delete(text, delete_list)

#split docs
paper_list = text.split("<DOCNO>")

#parse
for i in range(len(paper_list)):
    article = paper_list[i]
    #split words and join by \n
    article = "\n".join(article.split())
    #lower words
    article = article.lower()
    #delete punctuation
    article = re.sub(r'[^\w\s-]', '', article)
    #save tokens as a file
    with open("all_articles.txt", "a") as save_file:
        save_file.write(article + "\n\n")
    print(str(i) + '/' + str(len(paper_list)))
