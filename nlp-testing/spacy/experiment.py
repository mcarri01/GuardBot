import spacy
from spacy.matcher import PhraseMatcher


nlp = spacy.load('en_vectors_web_lg')

#doc4 = nlp(u"I'm chatting with Bob.")
#doc5 = nlp(u"I'm running a race.")

# doc1 = nlp(u"The labrador barked.")
# doc2 = nlp(u"The labrador swam.")
# doc3 = nlp(u"the labrador people live in canada.")
#
#
# for doc in [doc1, doc2, doc3]:
#     keyword = doc[1]
#     print(keyword)
#     work = nlp(u"dog")
#     print(keyword.similarity(work))
#
#
# print("Second example")

doc1 = nlp(u"Doing some homework.")
doc2 = nlp(u"I'm working on a project.")
doc3 = nlp(u"I'm working on an assignment.")

#print(doc1.similarity(doc2))

#matcher = PhraseMatcher(nlp.vocab)
#matcher.add('project', None, nlp(u"homework"))

#matches = matcher(doc1)
#print(matches)
#start = matches[0][1]
#end = matches[0][2]

#n_vectors = 105000  # number of vectors to keep
#removed_words = nlp.vocab.prune_vectors(n_vectors)
#doc1 = nlp(u"Doing some food")

#print(doc1.similarity(doc2))

#print(nlp(u"food").similarity(nlp(u"homework")))
#print(nlp(u"Doing some food").similarity(nlp(u"Doing some homework")))
print(nlp(u"Doing some homework").similarity(nlp(u"Doing a project")))
print(nlp(u"Doing some food").similarity(nlp(u"Doing a project")))
#matcher = PhraseMatcher(nlp.vocab)
#matcher.add('project', None, nlp(u"homework"))

#matches = matcher(doc1)
#print(matches)
#start = matches[0][1]
#end = matches[0][2]
#print(doc1[start:end])
#
# def on_match(matcher, doc, id, matches):
#     print('Matched!', matches)
#
# matcher = PhraseMatcher(nlp.vocab)
# matcher.add('OBAMA', on_match, nlp(u"Barack Obama"))
# matcher.add('HEALTH', on_match, nlp(u"health care reform"),
#                                 nlp(u"healthcare reform"))
# doc = nlp(u"Barack Obama urges Congress to find courage to defend his healthcare reforms")
# matches = matcher(doc)
#

# for doc in [doc1, doc2, doc3]:
#     for other_doc in [doc1, doc2, doc3]:
#         print(doc.similarity(other_doc))
