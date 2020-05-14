import pre_process
import connect
import query_db
import query_doc
import find_tf_idf


def system_first_uploading():
    '''
    this func is being called only once when system first uploads
    this func uploads documents with label to DB
    :return:
    '''
    try:
        clean = pre_process.get_clean_data("https://en.wikipedia.org/wiki/Sport", "sport")
        text_arr = []

        for i in clean.clean_data:
            text_arr.append([i, clean.label[0]])

        for i in text_arr:
            query_doc.save_docs_into(i[0], i[1])

        clean2 = pre_process.get_clean_data("https://en.wikipedia.org/wiki/Medicine", "medicine")

        text_arr = []

        for i in clean2.clean_data:
            text_arr.append([i, clean2.label[0]])

        for i in text_arr:
            query_doc.save_docs_into(i[0], i[1])

        query_doc.con.conn.commit()


    except Exception as e:

        print(e)

def uploading_more_ducs_to_system():
    """
    this func uploads the system with more docs beyond the docs  which already exists
    """
    new_url = input("enter a new URL to update the docs in system")
    label = input("enter the URL subject")
    try:
        clean = pre_process.get_clean_data(new_url, label)
        text_arr = []

        for i in clean.clean_data:
            text_arr.append([i, clean.label[0]])

        for i in text_arr:
            query_doc.save_docs_into(i[0], i[1])
    except Exception as e:

        print(e)



def finds_users_input_subject():
    """
this func gets user's URL and hopfully returns if the subject is sport medicine or unrecognised
    :return:
    """
    while (True):
        try:
            users_new_url = input("please enter url:")

            clean_user_text = pre_process.get_clean_data(f"{users_new_url}", "")
            print(find_tf_idf.finding_label_of_new_file(
                [clean_user_text.clean_data[0] + clean_user_text.clean_data[1] + clean_user_text.clean_data[2], ""],
                query_doc.get_docs()))
            return
        except Exception as e:
            print(e)


def list_of_all_docs_terms_score_to_DB():
    '''
    this func updats the DB with all documents terms values
    :param list:[[text,label][text,label]...]
    :return: list: list [[term,score,label],[term,score,label],...]
    '''
    try:
        list = query_doc.get_docs()
        tf_idf_score_list = find_tf_idf.finds_list_of_all_documents_terms_values(list)
        query_doc.save_tfidf(tf_idf_score_list)
        print("finish")
        return find_tf_idf.finds_list_of_all_documents_terms_values(list)
    except Exception as e:
        print(e)


finds_users_input_subject()
# url's which as been tested successfully:
# "https://en.wikipedia.org/wiki/Sport"
# "https://en.wikipedia.org/wiki/Medicine"
# "https://en.wikipedia.org/wiki/Hospital"
# "https://en.wikipedia.org/wiki/Tel_Aviv"
# "https://en.wikipedia.org/wiki/Basketball"
# "https://en.wikipedia.org/wiki/Jerusalem"
