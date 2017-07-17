"""
So two ways I can go about getting recent articles...

1. I use my previous code from csv_to_txt.py to just get the column from the csv files 
and then only store the csv files that have a publication data of 2010 - present.

2. I could write a new script that does the same thing but with json files. 

Things to think about: 
1. I already have all the csv files now. If I did (2) I would have to get yadu to send
me all the other json files. 
2. Apparently Json files are better to work with but I'm having a hard time getting the content from them. 
"""

import json
import pprint 
import regex as re
import PyPDF2

path = '/home/benglick/data-00020.json'

"""
This function will take get_articles as a parameter and then return a list of dictionaries
for every research article. 
"""
def parse_research_articles(list_of_dict, addInfo = False):
    data = list_of_dict
    research_articles = []
    for x in range(len(data)):
        data = list_of_dict[x]
        if 'type' in data.keys():
            if 'research-article' in data['type']:
                research_articles += [data]
    if addInfo == True:
        print('There are '+str(len(research_articles)))+' research articles.'
        t = research_articles[0]
        print(t['title'])
    return research_articles

"""
This function will read the json file which is the formatted as a dictionary of dictionaries. 
Then it will check if the dictionaries for each article actual has a publication date. From that
the script will get articles from dictionaries that have a publication date of 2010 - present. 
It will take in a path to a json file and a true or false statement depending of whether or not
the user wants additional data about the json file.
The function will return a list of articles that were published during or after 2010.
"""
def get_recent_articles(path,printInfo = False):
    with open(path,'r') as f:
        recent = []
        count = 0 # Tracks how many articles there are before 2010.
        rcount = 0 # Tracks how many articles there are from 2010-present.
        tcount = 0 # Tracks total # of articles.
        incomplete = 0 # Tracks how many rows of the json file don't have a publication date. 
        c = 0
        for line in f: # Iterates through each row of the json file.
            
            tcount+=1 # Tracks how many articles there are total.
            data = json.loads(line)
            
            """
            This where I check that the publication date exists in the json and then that 
            the publication data is in the 21st Century. Then I call 'data' which references
            the content of the article. 
            """
            if 'publication-date' in data.keys():   # This makes sure that each row has a publication date.
                if '201' in data['publication-date']:
                    rcount+=1
                    recent += [data]    
                else:
                    count+=1
            else:
                incomplete+=1 
        

        # This allows user to show info about json file if they want.
        if printInfo==True:
            research = recent[3]
            print(research['type'])
            print("There are "+str(tcount)+" articles total.")
            print("There are "+str(count)+" articles published before 2010.")
            print("There are "+str(rcount)+" articles published after or during 2010.")
    """
    This is just a check to make sure the program worked. rcount = # of articles from 2010 - present
    and len(recent) should be the same thing. Thus if they aren't equal something didn't work. 
    """
    if len(recent) == rcount:
        return recent
    else:
        print("Something is probably wrong with the json file.")
        print("There are "+str(rcount)+" articles from 2010-present but the list that stores these possible articles has a length different that the counter...")

"""
This just combines the two functions above. 
"""
def get_dictionaries(path):
    articles = parse_research_articles(get_recent_articles(path))
    return articles 



allDictionaries = get_dictionaries(path)

def get_content(list_of_dict, number_of_articles = 1):
    articleList = []
    for x in range(len(list_of_dict)):
        dataDict = list_of_dict[x]
        content = dataDict['data'] # the content is in a nested dictionary... dumb I know
        contentList = content['ocr'] # and then the this is a nested list... what the fuck
        totalArticle = u''.join(contentList)
        articleList.append(totalArticle)
    print(len(articleList))
    return articleList


# def get_full_citations(articleStr, flag):
#     matches=[]
#     refs = refextract.extract_references_from_string(articleStr, is_only_references=flag)
#     for ref in refs:
#         matches.append(ref["raw_ref"][0])
#     return matches


def get_intexts(articleStr):
    author = "(?:[A-Z][A-Za-z'`-]+)"
    etal = "(?:et al.?)"
    additional = "(?:,? (?:(?:and |& )?" + author + "|" + etal + "))"
    year_num = "(?:19|20)[0-9][0-9]"
    page_num = "(?:, p.? [0-9]+)?"  # Always optional
    year = "(?:, *"+year_num+page_num+"| *\("+year_num+page_num+"\))"
    regex = "(" + author + additional+"*" + year + ")"
    matches = re.findall(regex, articleStr)
    return matches

def get_full_citations_regex(articleStr):
    ex = re.compile(r"""^(?<author>[A-Z](?:(?!$)[A-Za-z\s&.,‘’])+)\((?<year>\d{4})\)\.?\s*(?<title>[^()]+?[?.!])\s*(?:(?:(?<jurnal>(?:(?!^[A-Z])[^.]+?)),\s*(?<issue>\d+)[^,.]*(?=,\s*\d+|.\s*Ret))|(?:In\s*(?<editors>[^()]+))\(Eds?\.\),\s*(?<book>[^().]+)|(?:[^():]+:[^().]+\.)|(?:Retrieved|Paper presented))""")
    matches = re.findall(ex, articleStr)
    return matches


def extract_text_from_pdf(doi):
    text=""
    pdf_file = open('{}.pdf'.format(doi), 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    for i in range(number_of_pages):    
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        text += " "+page_content
    return text

def get_and_compare_citations(articles):
    articles = get_content(allDictionaries)
    for article in articles:
        intexts = get_intexts(article)
        fulls = get_full_citations_regex(article)
        print(fulls)
        print(intexts)