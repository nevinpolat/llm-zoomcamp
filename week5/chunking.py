if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

import hashlib

def generate_document_id(doc):
    combined = f"{doc['course']}-{doc['question']}-{doc['text'][:10]}"
    hash_object = hashlib.md5(combined.encode())
    hash_hex = hash_object.hexdigest()
    document_id = hash_hex[:8]
    return document_id
@transformer
def transform(data, *args, **kwargs):
    documents = []

    for course_dict in data:
        for doc in course_dict['documents']:
            doc['course'] = course_dict['course']
            # previously we used just "id" for document ID
            doc['document_id'] = generate_document_id(doc)
            documents.append(doc)
        print(len(documents))
        print(type(data))
        return documents