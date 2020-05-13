import sys

import connect as con

cur = con.cursor


def save_docs(doc, label):
    try:

        cur.execute(f"INSERT INTO all_docs (doc,label) VALUES ('{doc}','{label}') ")

        print("Document saved successfully")

    except:

        print(sys.exc_info()[1])


def get_doc_by_label(label):
    return con.return_tables(f"""SELECT doc, label FROM all_docs WHERE label= '{label}';""")


def get_all_tfidf():
    return con.return_tables("""SELECT * FROM tfidf""")


def get_score_term_by_label(list_tfidf):
    cur.execute(f"""SELECT score FROM tfidf WHERE term= '{list_tfidf[0]}' AND label = '{list_tfidf[1]}';""")

    rows = cur.fetchall()

    result = []

    [result.append(row[0]) for row in rows]

    if len(result) == 0:

        print("term or label does not exist")

    else:

        return result


def get_count_doc(label):
    cur.execute(f"""SELECT * FROM all_docs WHERE label = '{label}';""")

    return cur.rowcount


con.conn.commit()

if __name__ == '___main__':
    cur.close()

    con.conn.close()