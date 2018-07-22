import re
import sys
import io
sys.path.append("..")
sys.path.append("../..")
import postgis_functions

# input and output files
# infile = sys.argv[1]
outfile = "/home/bill/Desktop/thesis/code/tweet2vec/misc/processed_tweets.txt"

regex_str = [
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)+' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    tokens = [token.lower() for token in tokens]

    html_regex = re.compile('<[^>]+>')
    tokens = [token for token in tokens if not html_regex.match(token)]

    mention_regex = re.compile('(?:@[\w_]+)')
    tokens = ['@user' if mention_regex.match(token) else token for token in tokens]

    url_regex = re.compile('http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+')
    tokens = ['!url' if url_regex.match(token) else token for token in tokens]

    hashtag_regex = re.compile("(?:\#+[\w_]+[\w\'_\-]*[\w_]+)")
    tokens = ['' if hashtag_regex.match(token) else token for token in tokens]

    flag = False
    for item in tokens:
        if item=='rt':
            flag = True
            continue
        if flag and item=='@user':
            return ''
        else:
            flag = False

    return ' '.join([t for t in tokens if t]).replace('rt @user : ','')


ttable = "matched_twitter_ams"
#tweets = postgis_functions.get_rows_from_table_where_col_is_null(ttable, "processedtext")
tweets = postgis_functions.get_rows_from_table(ttable)
count=0
with open(outfile, 'w') as file:
    for t in tweets:
        count+=1
        file.write(t["processedtext"].rstrip()+'\n')
        #print(t["text"])
        #print(t["processedtext"])
        print(count)
        #postgis_functions.add_processed_text_to_table(preprocess(t["text"].replace("'", "''")),
        # "processedtext ttable, t["id"])
# with io.open(outfile, 'w') as tweet_processed_text, io.open(infile, 'r') as fin:
#     for line in fin:
