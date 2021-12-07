from flask import Flask, render_template, request, session, url_for, redirect
import pandas as pd
import json
import plotly
import plotly.express as px
from werkzeug.wrappers import Request, Response
from flask import Flask
import socket
import threading
import uuid
from typing import Any, Callable, cast, Optional
from werkzeug.serving import run_simple
from flask import Flask, abort, jsonify
from flask_cors import cross_origin
from werkzeug.serving import run_simple
import requests
import datetime
from flask_pymongo import pymongo
import dateutil.parser
import googletrans
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt



app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
@app.route('/home',methods = ['POST', 'GET'])
def html():
    if request.method == 'POST':
        user = request.form["brand"]
        return redirect(url_for('brand',brandname = user))
    else:
        user = request.args.get("brand")
        return redirect(url_for('brand',brandname = user))


@app.route('/brand/<brandname>')

def brand(brandname):

    cursor = mydb.Facebook_Sentiment_Analysis_Collection.aggregate(
        [ { "$match" : { "brand" : brandname } }   

        ]
    )
    mongo_docs = list(cursor)
    df_mongodoc = pd.DataFrame(mongo_docs)
  
    sentiment_count = df_mongodoc['avg_sentiment'].value_counts()
    labels=sentiment_count.index
    pie = px.pie(values=sentiment_count, names=labels, title = 'Sentiment in year 2020')
    pieJSON = json.dumps(pie, cls=plotly.utils.PlotlyJSONEncoder)
    ##############################################################
    
    
    
    
    df_mongodoc['created_time'] = pd.to_datetime(df_mongodoc['created_time'])
    df_mongodoc.index = df_mongodoc['created_time']
    plot_scores = df_mongodoc[['created_time', 'avg_score']].groupby([pd.Grouper(key='created_time', freq='M')]).agg('mean').reset_index()
    fig = px.line(plot_scores, x='created_time', y="avg_score",range_x=['2020-01-01','2020-12-31'],  labels={
                         "created_time": "date",
                         "avg_score": "score"
                     },title="Sentiment Scores")
    fig.update_xaxes(rangeslider_visible=True,
                        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    ####################################################
    
##    wordcloud part


#     all_words = ' '.join([text for text in df_mongodoc['cleanMessage']])

#     # spacy + nltk + additional stopword
#     stopwords = ['purchase','ipad','computer','charge','money','pay','support','care','product','today','buying','company','change','number','lost','waiting','open','user','hold','people','dear','making','lot','hour','wait','day','guy','week','iphones','thereby', 'from', 'same', 'twelve', 'amongst', 'behind', 'hence', 'and', 'back', 'him', 'might', 'really', 'should', 'though', "'m", 'why', 'for', 'between', 'forty', 'seems', '’ve', 'among', 'anywhere', 'ours', 'no', 'about', 'hers', 'within', 'name', 'nor', 'alone', 'before', 'much', 'these', 'hereafter', 'were', 'me', 'few', 'his', '‘ve', 'put', "n't", 'her', 'another', 'without', 'eight', 'you', 'anyone', '‘d', 'one', 'whether', 'get', 'he', 'per', 'using', 'next', 'else', 'enough', 'am', 'either', 'when', 'so', 'had', 'serious', 'along', 'made', 'due', 'take', 'has', 'otherwise', 'three', 'thereupon', 'meanwhile', 'everything', 'whereafter', '’m', 'rather', 'throughout', 'been', 'not', 'to', 'however', 'she', 'became', 'i', 'whereby', 'four', 'anyway', "'ll", 'thereafter', 'who', 'become', 're', 'fifteen', 'yet', 'first', 'nevertheless', 'still', 'herself', 'everyone', 'too', 'wherein', 'my', 'besides', 'below', 'part', 'nine', 'here', 'everywhere', 'side', 'any', 'ourselves', 'which', 'some', 'than', 'just', 'make', 'becomes', 'somewhere', 'last', 'but', 'again', 'as', 'nowhere', 'nothing', 'doing', 'except', 'somehow', 'therefore', 'call', 'most', 'because', 'say', 'sometime', 'they', '’re', 'namely', 'such', 'how', 'we', 'out', 'hereupon', 'anything', 'two', 'thence', 'off', 'since', 'formerly', 'see', 'seeming', 'beforehand', 'beside', 'whenever', 'thru', 'against', 'by', 'ever', 'now', 'during', 'afterwards', 'while', 'yourself', 'unless', 'each', 'hundred', 'well', 'once', 'empty', 'be', "'d", 'them', 'those', 'with', 'third', 'mostly', 'full', 'several', 'already', 'six', '’d', 'have', 'a', 'quite', 'even', 'anyhow', 'if', 'do', 'amount', 'over', 'fifty', '‘m', 'it', "'ve", 'never', 'front', 'after', 'ten', 'indeed', 'hereby', "'s", 'former', 'themselves', 'go', 'toward', 'every', 'none', 'their', 'whereas', 'onto', 'are', 'himself', 'twenty', 'whence', 'must', 'sometimes', 'herein', 'also', 'mine', 'cannot', 'yourselves', 'into', 'of', 'that', 'used', 'towards', 'did', 'through', 'regarding', 'only', 'whose', 'n‘t', 'would', 'thus', 'nobody', 'could', 'moreover', 'whereupon', 'an', 'whatever', 'n’t', 'beyond', 'more', 'up', 'almost', 'seem', 'seemed', 'keep', 'the', 'further', 'upon', 'various', 'is', 'least', 'eleven', 'many', 'other', 'whom', 'neither', 'move', 'your', 'can', 'itself', 'latter', '’s', 'its', 'via', '‘re', 'own', 'or', 'together', '‘s', 'done', 'does', 'above', 'others', 'whole', 'elsewhere', 'under', 'around', 'what', 'where', 'five', 'give', "'re", 'less', 'something', 'perhaps', 'all', 'myself', 'whoever', 'please', 'very', 'top', '’ll', 'wherever', 'becoming', 'at', 'sixty', 'latterly', 'may', 'whither', 'both', 'until', 'ca', 'in', 'on', 'across', 'therein', 'someone', 'often', 'was', 'show', '‘ll', 'this', 'down', 'us', 'then', 'always', 'our', 'although', 'will', 'there', 'noone', 'yours', 'bottom', 'being','time','work','received','year','buy','called','asked','issue','hope','send','month','told',"apple", "iphone",'thing','great','bought','love','good','',"phone",'problem','sell','longer',"0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"]\
#         + list(STOPWORDS)

#     wordcloud = WordCloud(
#         background_color='white',
#         stopwords=stopwords,
#         width=1600,
#         height=800,
#         random_state=1,
#         colormap='jet',
#         max_words=15,
#         max_font_size=200).generate(all_words)
    
#     # It does not save to local directory
#     wordcloud.to_file('C:/Users/WeiWei/Desktop/Jupyter/static/wcad.png')    
    
    
  
    return render_template('chart.html', plotJSON_LINE=graphJSON, plotJSON_PIE = pieJSON)
if __name__== '__main__':
    app.run()
