#!/usr/bin/env python3
#usage python3 recent_articles.py

import json
import regex as re
import csv

path = '/home/benglick/data-00020.json'


def get_recent_articles(path, printInfo=False):
    """
    This function will read the json file which is the formatted as a dictionary of dictionaries.
    Then it will check if the dictionaries for each article actual has a publication date. From that
    the script will get articles from dictionaries that have a publication date of 2010 - present.
    It will take in a path to a json file and a true or false statement depending of whether or not
    the user wants additional data about the json file.
    The function will return a list of articles that were published during or after 2010.
    """
    with open(path, 'r') as f:
        recent = []
        count = 0  # Tracks how many articles there are before 2010.
        rcount = 0  # Tracks how many articles there are from 2010-present.
        tcount = 0  # Tracks total # of articles.
        # Tracks how many rows of the json file don't have a publication date.
        incomplete = 0
        c = 0
        for line in f:  # Iterates through each row of the json file.

            tcount += 1  # Tracks how many articles there are total.
            data = json.loads(line)

            """
            This where I check that the publication date exists in the json and then that
            the publication data is in the 21st Century. Then I call 'data' which references
            the content of the article.
            """
            if 'publication-date' in data.keys(
            ):   # This makes sure that each row has a publication date.
                if '201' in data['publication-date']:
                    rcount += 1
                    recent += [data]
                else:
                    count += 1
            else:
                incomplete += 1

        # This allows user to show info about json file if they want.
        if printInfo:
            research = recent[3]
            print(research['type'])
            print("There are " + str(tcount) + " articles total.")
            print(
                "There are " +
                str(count) +
                " articles published before 2010.")
            print(
                "There are " +
                str(rcount) +
                " articles published after or during 2010.")
    """
    This is just a check to make sure the program worked. rcount = # of articles from 2010 - present
    and len(recent) should be the same thing. Thus if they aren't equal something didn't work.
    """
    if len(recent) == rcount:
        return recent
    else:
        print("Something is probably wrong with the json file.")
        print(
            "There are " +
            str(rcount) +
            " articles from 2010-present but the list that stores these possible articles has a length different that the counter...")


def parse_research_articles(list_of_dict, addInfo=False):
    """
    This function will take get_articles as a parameter and then return a list of dictionaries
    for every research article. It will also check that each dictionary actually has a doi.
    """
    data = list_of_dict
    research_articles = []
    for x in range(len(data)):
        articleDict = list_of_dict[x]
        if 'doi' in articleDict.keys():
            if 'type' in articleDict.keys():
                if 'research-article' in articleDict['type']:
                    research_articles += [articleDict]

    # This is just a conditional to give the user an option to display more
    # info if needed.
    if addInfo:
        print('There are ' + str(len(research_articles))) + \
            ' research articles.'
        t = research_articles[0]
        print(['title'])
    return research_articles


def get_dictionaries(path):
    """
    This just combines the two functions above.
    """
    articles = parse_research_articles(get_recent_articles(path))
    return articles


def min_jsonDict(list_of_dict, number_of_articles=0):
    """
    This function will create a list of dictionaries where each entry has the articles
    doi and the content. It will look like [{'doi': 4363653, }].
    It will return
    """
    if number_of_articles == 0:
        number_of_articles = len(list_of_dict)
    else:
        number_of_articles = number_of_articles
    articleList = []
    for x in range(number_of_articles):
        totalDict = {}  # This will hold the doi and content. Then it will be added as an index to articleList
        # print(x)
        dataDict = list_of_dict[x]
        # print(dataDict)
        doi = dataDict['doi']
        title = dataDict['title']
        # the content is in a nested dictionary... dumb I know
        content = dataDict['data']
        # and then this is a nested list... what the fuck
        contentList = content['ocr']
        # And then I need to join it to....
        totalArticle = u''.join(contentList)
        totalDict['content'] = totalArticle
        totalDict['title'] = title
        totalDict['doi'] = doi

        articleList.append(totalDict)
    # print(len(articleList))
    # It's a list of dictionaries that correlate to individual articles.
    return articleList


def split_references(list_of_dict, addInfo=False):
    """
    This function splits the article into a content section and a references section.
    When running this the input should call min_jsonDict so it should look like this,
    split_references(minJsonDict(path_to_jsonfile))
    """
    articleList = []
    count = 0  # this will help us see how successful this is.
    wrong = 0  # ""
    # Iterates through each article's dictionary in the list.
    for x in range(len(list_of_dict)):
        articleDict = list_of_dict[x]

        content = articleDict['content']

        ex = re.compile(r"""(( +[R|r][E|e][F|f][E|e][R|r][E|e][N|n][C|c][E|e][S|s])|( +[B|b][I|i][B|b][L|l][I|i][O|o][G|g][R|r][A|a][P|p][H|h][Y|y])|( +[W|w][O|o][R|r][K|k][S|s] ?[C|c][I|i][T|t][E|e][D|d])|( +[E|e][N|n][D|d] ?[N|n][O|o][T|t][E|e][S|s]))""")
        article = re.split(ex, content)

        # this is a check that the regex actually split successfully.
        if len(article) == 7:
            articleDict['references'] = article[6]
            articleDict['content'] = article[0]
            articleList.append(articleDict)
            count += 1
        else:
            wrong += 1
    if addInfo:  # this is just to show additional info if wanted.
        print(
            str(count) +
            ' articles were split succesfully at the reference section')
        print("And " + str(wrong) + ' articles were not split sucessfully :(')
    return articleList


def old_split_references(list_of_dict):
    """Same as above but without a regex"""
    articleList = []
    # Iterates through each article's dictionary in the list.
    for x in range(len(list_of_dict)):
        articleDict = list_of_dict[x]
        content = articleDict['content']
        article = content.split('References')
        if len(article) == 2:
            articleDict['references'] = article[1]
            articleDict['content'] = article[0]
            articleList.append(articleDict)
        else:
            article = content.split('REFERENCES')
            if len(article) == 2:
                articleDict['references'] = article[1]
                articleDict['content'] = article[0]
                articleList.append(articleDict)
            else:
                article = content.split('Bibliography')
                if len(article) == 2:
                    articleDict['references'] = article[1]
                    articleDict['content'] = article[0]
                    articleList.append(articleDict)
                else:
                    article = content.split('BIBLIOGRAPHY')
                    if len(article) == 2:
                        articleDict['references'] = article[1]
                        articleDict['content'] = article[0]
                        articleList.append(articleDict)
                    else:
                        article = content.split('BIBLIOGRAPHY')
                        if len(article) == 2:
                            articleDict['references'] = article[1]
                            articleDict['content'] = article[0]
                            articleList.append(articleDict)
                        else:
                            article = content.split('Endnotes')
                            if len(article) == 2:
                                articleDict['references'] = article[1]
                                articleDict['content'] = article[0]
                                articleList.append(articleDict)
                            else:
                                article = content.split('ENDNOTES')
                                if len(article) == 2:
                                    articleDict['references'] = article[1]
                                    articleDict['content'] = article[0]
                                    articleList.append(articleDict)
                                else:
                                    article = content.split('work cited')
                                    if len(article) == 2:
                                        articleDict['references'] = article[1]
                                        articleDict['content'] = article[0]
                                        articleList.append(articleDict)
    return articleList


"""
def get_full_citations(articleStr, flag):
    matches=[]
    refs = refextract.extract_references_from_string(articleStr, is_only_references=flag)
    for ref in refs:
        matches.append(ref["raw_ref"][0])
    return matches
"""


def get_intexts(articleStr):
    """Get all in text citations given a string representation of 
    text of an article"""
    author = "(?:[A-Z][A-Za-z'`-]+)"
    etal = "(?:et al.?)"
    additional = "(?:,? (?:(?:and |& )?" + author + "|" + etal + "))"
    year_num = "(?:19|20)[0-9][0-9]"
    page_num = "(?:, p.? [0-9]+)?"  # Always optional
    year = "(?:, *" + year_num + page_num + \
        "| *\(" + year_num + page_num + "\))"
    regex = "(" + author + additional + "*" + year + ")"
    matches = re.findall(regex, articleStr)
    return matches


def get_full_citations_regex(articleStr):
    """Get all full citations given text of a references section of a paper"""
    ex = re.compile(
        r"""(?<year>([(][^)]*(19|20) ?[0-9]{2}[^)]*[)]))|[19|20]{2}\d{2};\d{2}:.*\.|(?<year3>(19|20)\d{2}[a-z]?\.) """)
    matches = re.split(ex, articleStr)
    tempMatches = []
    for i in range(0, len(matches) - 1, 2):
        match = xstr(matches[i]) + " " + xstr(matches[(i + 1)])
        tempMatches.append(match)
    return tempMatches


def xstr(s):
    """convert NoneType to empty string"""
    if s is None:
        return ''
    return str(s)


def extract_text_from_pdf(doi):
    """Extract all text from an article pdf given a doi"""
    text = ""
    pdf_file = open('{}.pdf'.format(doi), 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    for i in range(number_of_pages):
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        text += " " + page_content
    return text


def get_and_compare_citations(articles):
    """pull all citations out of all articles in @param articles
    output will be written to file with filename the same as the doi
    of the articles inputted"""
    for article in articles:
        #  (article)
        doi = article['doi']
        title = article['title']
        intexts = get_intexts(article['content'])
        fulls = get_full_citations_regex(article['references'])
        matches = map_citations(intexts, fulls, article['content'])
        write_to_csv(matches, doi.replace("/", ":"), title)
    return 0


def map_citations(intexts, fulls, content):
    """Given a list of in text citations, a
    list of full citations, and a string representation
    of the full text of the article, return a list of citations.
    each citation is a dictionary with items intext, full, and context"""
    mapping = []
    for intext in intexts:
        citation = {"intext": intext}
        pos = content.index(intext)
        before = content[pos - 150:pos]
        after = content[pos:pos + 150]
        context = before + ' ' + after
        citation['context'] = context
        # Split year from name/institution
        split_cite = re.split(r'(\s+)', intext)
        year = ''.join(filter(lambda x: x.isdigit(), split_cite[-1:][0]))
        other_stuff = ''.join(split_cite[:-1])
        for full in fulls:
            otherMatch = other_match(other_stuff, full)
            if year in full and otherMatch:
                citation['full'] = full
                break
        mapping.append(citation)
    return mapping


def other_match(other_stuff, full):
    """Checks for matches between in text citation
    and full citation, ignoring year. Most of the time this
    will be an author, but sometimes it's a conference or 
    an institution or something

    I know this is an ugly ass pile of logic but that's citation 
    extraction in a nutshell for you
    
    i'm sorry to anyone who has to read this in future -BG
    """
    if ',' in other_stuff:
        if other_stuff.split(',')[0].strip() in full:
            return True
        elif 'and' in other_stuff:
            if other_stuff.split('and')[0].strip() in full or other_stuff.split('and')[
                    1].strip() in full:
                return True
        return False
    elif "As" in other_stuff or "as" in other_stuff:
        if other_stuff.lower().split('as')[1].strip() in full:
            return True
        return False
    elif 'and' in other_stuff:
        if other_stuff.split('and')[0].strip() in full or other_stuff.split('and')[
                1].strip() in full:
            return True
        return False
    elif '&' in other_stuff:
        if other_stuff.split('&')[0].strip() in full or other_stuff.split('&')[
                1].strip() in full:
            return True
        return False
    elif 'et al.' in other_stuff:
        if other_stuff.split('et al.')[0].strip() in full:
            return True
        return False
    elif other_stuff.strip() in full:
        return True
    elif other_stuff in full:
        return True
    return False


def write_to_csv(matches, doi, title):
    """Writes all citations to csv with their 
    respective in-text citation, full citation,
    context, doi, and title"""
    fh = open('{}.csv'.format(doi), 'w')
    cols = ['intext', 'full', 'context', 'doi', 'title']
    writer = csv.DictWriter(fh, fieldnames=cols, delimiter=',')
    writer.writeheader()
    for citation in matches:
        citation['doi'] = doi
        citation['title'] = title
        writer.writerow(citation)
    fh.close()

allDictionaries = get_dictionaries(path)
articles = old_split_references(min_jsonDict(allDictionaries))
get_and_compare_citations(articles)
