import os
import env
import configparser
import json
import uuid
import cmdparser as cp
from victo import facade as fd
from langchain.llms import Cohere
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings import CohereEmbeddings
from langchain.chains.question_answering import load_qa_chain


config = configparser.RawConfigParser()

configPath = os.path.join(os.path.dirname(__file__),'victo.properties');
config.read(configPath)

db = config.get('VectorDatabase', 'database.path')
datadump = config.get('DataDump', 'datadump.path')
kb = config.get('KnowledgeBase', 'knowledgebase.path')

os.environ["COHERE_API_KEY"] = env.api_key
text_splitter = CharacterTextSplitter(separator = "\n", chunk_size = 1500, chunk_overlap  = 350, length_function = len)
embeddings = CohereEmbeddings(model="embed-english-light-v2.0")

def newCollection(args):
    try:
        val = json.loads(args)
        rs = fd.newCollection(db, val['id'])
        print(f"Response Code: {rs.errCode} and Response Message: {rs.errMsg}")
    except KeyError:
        print("Please provide ID for collection")

def deleteCollection(args):
    try:
        val = json.loads(args)
        rs = fd.deleteCollection(db, val['id'])
        print(f"Response Code: {rs.errCode} and Response Message: {rs.errMsg}")
    except KeyError:
        print("Please provide ID for collection")

    
def collectionCount():
    rs = fd.collectionCount(db)
    print(f"Response Code: {rs.errCode} and Response Message: {rs.errMsg} and Count: {rs.count}")

    
def collectionList():
    rs = fd.collectionList(db)
    print(f"Response Code: {rs.errCode} and Response Message: {rs.errMsg} and List: {rs.collections}")


def putVector(args):
    try:
        val = json.loads(args)

        data = open(os.path.join(kb,val['data']),"r")
        texts = text_splitter.split_text(''.join(data.readlines()))

        for text in texts:
            uid = uuid.uuid4()
            filename = str(uid) + ".txt"
            filepath = os.path.join(datadump, val['collection'], filename)
            with open(filepath, 'x') as file:
                file.write(text)
            query_result = embeddings.embed_query(text)
            rs = fd.putVector(db, val['collection'], "cohere-embed-english-light-v2.0", str(uid), len(query_result), query_result)
            print(f"Response Code: {rs.errCode} and Response Message: {rs.errMsg} and Hash: {rs.hash}")

    except KeyError:
        print("Invalid input") 
    

def getVector(args):
    try:
        val = json.loads(args)
        rs = fd.getVector(db, val['collection'], val['id'])
        # print(f"Response Code: {rs.errCode} and Response Message: {rs.errMsg}")
        # print(len(rs.node.vp))
    except KeyError:
        print("Please provide valid details")


def queryVector(args):
    try:
        val = json.loads(args)
        query_embed_result = embeddings.embed_query(val['query'])
        vd_method = val['vd-method']
        k_value = val['k-value']
        logical_op = val['logical-op']

        rs = fd.queryVector(db, val['collection'], "cohere-embed-english-light-v2.0", len(query_embed_result), query_embed_result, vector_distance_method=vd_method, logical_op=logical_op, k_value=k_value, p_value=3.0, include_fault=False)
        # print(rs.queryCount)

        if(rs.queryCount > 0) :
            docs = []
            for x in rs.queryVectorRS:
                print(f"Hash Code: {x.hash} and {x.distance}")
                texts = open(os.path.join(datadump, val['collection'], str(x.hash.decode('utf-8')) + ".txt"), "r")
                text = texts.readlines()
                for t in text:
                    docs.append(Document(page_content=t))
            
            chain = load_qa_chain(llm=Cohere(model="command-nightly", temperature=0))
            response = chain.run(input_documents=docs, question=val['query'])
            print(response)
        else:
            print("Data Shortage")
    except KeyError:
        print("Please provide valid details")    


def deleteVector(args):
    try:
        val = json.loads(args)
        rs = fd.deleteVector(db, val['collection'], val['id'])
        print(f"Response Code: {rs.errCode} and Response Message: {rs.errMsg}")
    except KeyError:
        print("Please provide valid input")

    
def vectorCount(args):
    try:
        val = json.loads(args)
        rs = fd.vectorCount(db, val['id'])
        print(f"Response Code: {rs.errCode} and Response Message: {rs.errMsg} and Count: {rs.count}")
    except KeyError:
        print("Please provide ID for collection")

    
def vectorList(args):
    try:
        val = json.loads(args)
        rs = fd.vectorList(db, val['id'])
        print(f"Response Code: {rs.errCode} and Response Message: {rs.errMsg} and List: {rs.vectors}")
    except KeyError:
        print("Please provide ID for collection")


def execute(args):
    if args.operation == "add" and args.object == "collection":
        newCollection(args.args)
    elif args.operation == "delete" and args.object == "collection":
        deleteCollection(args.args)
    elif args.operation == "count" and args.object == "collection":
        collectionCount()
    elif args.operation == "list" and args.object == "collection":
        collectionList()
    elif args.operation == "put" and args.object == "vector":
        putVector(args.args)
    elif args.operation == "get" and args.object == "vector":
        getVector(args.args)
    elif args.operation == "query" and args.object == "vector":
        queryVector(args.args)
    elif args.operation == "delete" and args.object == "vector":
        deleteVector(args.args)
    elif args.operation == "count" and args.object == "vector":
        vectorCount(args.args)
    elif args.operation == "list" and args.object == "vector":
        vectorList(args.args)
    else:
        print("Invalid Operation")
    # print(args)

if __name__ == "__main__":
    parser = cp.getArgParser()
    args = parser.parse_args()
    execute(args)
    