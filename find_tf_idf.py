
import math

import numpy as np



"""

this func parsses the new text from string format to list of terms

:param new_string:new_string =[new_text,label] 

:return: [[list_of_terms_in_new_text],label]

"""





def parsing_new_string_to_list(new_string):

    global new_string_list

    new_string_list = [new_string[0].split(" "), new_string[1]]

    return [new_string[0].split(" "), new_string[1]]





"""

this func parsses all texts which are in the DB from string format to list of terms

:param list_of_all_documents:[[text,label],[text,label]...] 

:return: [[[terms],label],[[terms],label]...]

"""





def parssing_all_strings_to_list(list_of_all_documents):

    global list_of_all_documents_terms

    list_of_all_documents_terms = []

    for document in list_of_all_documents:

        list_of_all_documents_terms.append([document[0].split(" "), document[1]])

    return list_of_all_documents_terms



"""

:param d_terms_list: list of terms in text

:return: most frequency term in text divided in number of terms in text  

"""

def max_term_in_d(d_terms_list):

    max = 0

    for i in d_terms_list:

        if d_terms_list.count(i) / len(d_terms_list) > max:

            max = d_terms_list.count(i) / len(d_terms_list)

    return max





def tf(term, d_terms_list):

    return (0.5 + 0.5 * ((d_terms_list.count(term) / len(d_terms_list)) / max_term_in_d(d_terms_list)))





# use by the idf function

def num_docs_has_the_term(term, list_of_documents):

    count = 0

    for i in list_of_documents:

        if term in i[0]:

            count += 1

    return count





def idf(term, list_of_documents):

    return math.log(len(list_of_documents) / num_docs_has_the_term(term, list_of_documents))





def tfidf(term, d_terms_list, list_of_documents):

    return tf(term, d_terms_list) * idf(term, list_of_documents)



"""

parssing list of texts to a list of terms, terms value and label 

:param list_of_all_documents: [[text,label],[text,label]...] 

:return: [[term,terms_tfidf_value,label],[term,terms_tfidf_value,label]...]

"""

def finds_list_of_all_documents_terms_values(list_of_all_documents):

    list_of_all_documents_terms = []

    for document in list_of_all_documents:

        list_of_all_documents_terms.append([document[0].split(" "), document[1]])

    global list_of_all_terms_and_values

    list_of_all_terms_and_values = []

    list_a = []

    for list_of_terms_in_document in list_of_all_documents_terms:

        for term in list_of_terms_in_document[0]:

            list_a.append([term, tfidf(term, list_of_terms_in_document[0], list_of_all_documents_terms),

                           list_of_terms_in_document[1]])



        list_b = []

    #reducing duplicates terms in one single text(documante)

        for term in list_a:

            if term not in list_b:

                list_b.append(term)

        for term2 in list_b:

            list_of_all_terms_and_values.append(term2)

        list_a = []

     #calculate average of a term which presents in different texts(documents)

    for term3 in list_of_all_terms_and_values:

        num_of_doc = 0

        for term4 in list_of_all_terms_and_values:

            if term3[0] == term4[0] and term3[2] == term4[2] :

                num_of_doc += 1

                if num_of_doc >1:

                   total_sum = term3[1] + term4[1]

                   term3[1] = total_sum / num_of_doc

                   list_of_all_terms_and_values.remove(term4)



    return list_of_all_terms_and_values





def adding_new_list_to_all_documents_terms(list_of_all_documents_terms, new_string):

    '''

    this func adds the new text [[term,term...],label] to the list of all documents list of terms and label

    :param list_of_all_documents_terms:

    :param new_string:

    :return:

    '''

    global new_list_of_all_documents_terms

    new_list_of_all_documents_terms = list_of_all_documents_terms

    new_list_of_all_documents_terms.append(parsing_new_string_to_list(new_string))

    return new_list_of_all_documents_terms





def creating_list_of_new_document_terms_and_values(new_string_list, new_string, list_of_all_documents):

    '''

    this func creates a list [[term,score,""][term,score,""][term,score,""]...] of the new text the user input

    :param new_string_list:

    :param new_string:

    :param list_of_all_documents:

    :return:

    '''

    global list_of_new_document_terms_and_values

    list_of_new_document_terms_and_values = []

    for term in new_string_list[0]:

        list_of_new_document_terms_and_values.append(

            [term, tfidf(term, new_string_list[0],

                         adding_new_list_to_all_documents_terms(parssing_all_strings_to_list(list_of_all_documents),

                                                                new_string)), ""])

    return list_of_new_document_terms_and_values





def finding_label_of_new_file(new_string, list_of_all_documents):

    '''

    this func finds the label(subject) of the new text the user inputs

    :param new_string: a list [new text(after cleaning) the user inputs,""]

    :param list_of_all_documents:a list [[text,label][text,label]]

    :return:

    '''

    num_of_sport_score = 0.1

    num_of_medicine_score = 0.1

    creating_list_of_new_document_terms_and_values(parsing_new_string_to_list(new_string), new_string,

                                                   list_of_all_documents)

    list_of_all_documents.append(new_string)

    finds_list_of_all_documents_terms_values(list_of_all_documents)

    for term in list_of_new_document_terms_and_values:

        for term2 in list_of_all_terms_and_values:

            if (term[0] == term2[0] and term[1] - term2[1] < 0.8 and term[1] - term2[1] > -0.8 and term2[2] == "sport"):

                num_of_sport_score += 1

            if (term[0] == term2[0] and term[1] - term2[1] < 0.8 and term[1] - term2[1] > -0.8 and term2[

                2] == "medicine"):

                num_of_medicine_score += 1

    print(num_of_sport_score)

    print(num_of_medicine_score)

    new_text_subject = ""

    if num_of_sport_score/num_of_medicine_score > 1.6:

        new_text_subject = "sport"

    elif num_of_medicine_score/num_of_sport_score >1.29:

        new_text_subject = "medicine"

    else :

        new_text_subject = "unrecognized"

    return(f"the subject of the new text is: {new_text_subject}")







if __name__ == '__main__':

    print(finds_list_of_all_documents_terms_values(list_of_all_documents))

    finding_label_of_new_file(new_string, list_of_all_documents)