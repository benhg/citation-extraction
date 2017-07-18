"""
Before you can use this, you have to do the following:

wget http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip
unzip stanford-corenlp-full-2017-06-09.zip

cd stanford-corenlp-full-2017-06-09
java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000

pip install pycorenlp

MUST BE RUN WITH PYTHON 3
"""

from pycorenlp import StanfordCoreNLP
import numpy as np
import csv
import glob
import json

def analyze_context(context):
    """Perform stanford sentiment analysis on context of a citation"""
    nlp = StanfordCoreNLP('http://localhost:9000')
    res = nlp.annotate(context,
                       properties={
                           'annotators': 'sentiment',
                           'outputFormat': 'json',
                           'timeout': 10000,
                       })
    print(type(res))
    sentences =''
    try:
        sentences=res['sentences']
    except Exception as e:
        print(e)
    if type(res) is str:
        try:
            res=json.loads(res)
            sentences = res['sentences']
        except Exception as e:
            print(res)
            print(e)
    sentenceValues = []
    #print(json.dumps(res,indent=4))
    try:
        for s in sentences:
            sentenceValues.append(int(s['sentimentValue']))
            """print ("%d: '%s': %s %s" % (
                s["index"],
                " ".join([t["word"] for t in s["tokens"]]),
                s["sentimentValue"], s["sentiment"]))
                """
        average = np.mean(sentenceValues)
    except Exception as e:
        print(e)
    return average


def write_new_csv(doi):
    """Write sentiment analysis to csv"""
    reader = csv.DictReader(open("{}.csv".format(doi), 'r'))
    cols = ['intext', 'full', 'context', 'doi', 'title', 'sentiment']
    fh = open("{}_with_sentiment.csv".format(doi), 'w')
    writer = csv.DictWriter(fh, fieldnames=cols, delimiter=',')
    writer.writeheader()
    for row in reader:
        row['sentiment'] = analyze_context(row['context'])
        writer.writerow(row)


def write_all_csvs(path):
    """Get sentiment analysis for all csvs in directory"""
    files = glob.glob('{}/*csv'.format(path))
    for file in files:
        write_new_csv(file.split(".csv")[0])


write_all_csvs('/home/benglick/extract')
