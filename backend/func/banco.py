def salva_dados(db, colecao, l):
    col = db[colecao]
    col.insert_many(l)

def salva_um(db, colecao, doc):
    col = db[colecao]
    col.insert_one(doc)

def recupera_documentos(db, colecao, query):
    col = db[colecao]
    l = []

    for i in col.find(query):
        del i['_id']
        l.append(i)

    return l

def limpa_banco(db, colecao):
    db.drop_collection(colecao)