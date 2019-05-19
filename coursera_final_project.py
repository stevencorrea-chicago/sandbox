def strip_punctuation(string):
    punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
    for punctuation in punctuation_chars:
        if punctuation in string:
            string = string.replace(punctuation,"")
    return string

def get_pos(string):
    string = strip_punctuation(string)
    string_lst = string.split()
    #print(string_lst)
    positive_words = []
    counter = 0
    with open("positive_words.txt") as pos_f:
        for lin in pos_f:
            if lin[0] != ';' and lin[0] != '\n':
                positive_words.append(lin.strip())
                
    for word in positive_words:
        for string in string_lst:
            if word == string:
                #print(word, string)
                counter += 1
    return counter

def get_neg(string):
    string = strip_punctuation(string)
    string_lst = string.split()
    negative_words = []
    counter = 0
    
    with open("negative_words.txt") as pos_f:
        for lin in pos_f:
            if lin[0] != ';' and lin[0] != '\n':
                negative_words.append(lin.strip())
    
    for word in negative_words:
        for string in string_lst:
            if word == string:
                #print(word, string)
                counter += 1
    return counter

#rf contains, text of a tweet, the number of retweets of that tweet, and the number of replies to that tweet
#wf Number of Retweets, Number of Replies, Positive Score (which is how many happy words are in the tweet), 
#Negative Score (which is how many angry words are in the tweet), and the Net Score (how positive or negative 
#the text is overall) for each tweet

rf = open("project_twitter_data.csv", "r")
wf = open("resulting_data.csv", "w")
wf.write("Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score\n")
ignore_header = False
for line in rf:
    if ignore_header:
        line_lst = line.split(',')
        pos_score = get_pos(line_lst[0])
        neg_score = get_neg(line_lst[0])
        net_score = pos_score - neg_score
        
        string_for_write_file = str(line_lst[1]) + ',' + str(line_lst[2].strip()) + ',' + str(pos_score) + ',' + str(neg_score) + ',' + str(net_score) + '\n'
        wf.write(string_for_write_file)
    else:
        ignore_header = True
rf.close()
wf.close()
