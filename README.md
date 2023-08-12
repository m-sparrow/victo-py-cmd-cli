# victo-py-cmd-cli

This project is a sample "Q and A" AI application built on top of [Victo - vector database] (https://pypi.org/project/victo/)

## Introduction

```
The Experience says "How to Answer" and
The Expertise  says "What to Answer"
```

Pre-trained language models has the experience on "how to answer" a question. The models takes the "context" supplied to it as the expertise or knowledge on "what to answer".

The idea behind this project is:

Let's say you have data in text format
- Split the data into small chunks of text
- Save the chunks of plain text in the file system
- Using a pre-trained NLP model, get the vector embeddings for this text and put into Victo DB
- When there is a query, convert the query into vector embeddings, search in Victo for relevant data, re-map the embeddings to plain text, pass it as context to Model for answers.

## Getting Started

<div align="center"> <h2> This code works only in MacOS</h2></div>

I have used [LangChain] framwork as abstraction for working with NLP models (https://python.langchain.com/docs/get_started/introduction.html) and Cohere NLP models for vector embeddings and generative AI. You may sign up for account in [Cohere](https://cohere.com/) and get a API key.

```
pip install langchain
pip install cohere
pip install victo
```

### Prerequisites

As a matter of first step, add "env.py" file in the project to call Cohere APIs

```
api_key = "<cohere API key>"
```

Next, you need to update victo.properties

```
[VectorDatabase]
database.path=**This where the victo database is created in the file system**

[DataDump]
datadump.path=**This where the chunks of plain text corresponding to the vector embeddings are store**

[KnowledgeBase]
knowledgebase.path=**This where the system search for data file to split into chunks of plain text and update the corresponding vector embeddings into Victo**
```

### Manual

### Add a collection 

```
python3 main.py put --args '{"id":"<id>"}'
```

### Delete a collection

```
python3 main.py delete --args '{"id":"<id>"}'
```

### Get the count of collection in a database

```
python3 main.py count
```

### Get the list of collections in a database

```
python3 main.py list
```

### Add vector records

```
python3 main.py put --args '{"collection":"<collection-id>", "data":"<data.txt>"}'
```

### Delete vector record

```
python3 main.py delete -- args '{"collection":"<collection-id>", "id": "<vector-id>"}'
```

### Get a vector record

```
python3 main.py get -- args '{"collection":"<collection-id>", "id": "<vector-id>"}'
```

### Query vector records

```
python3 main.py query -- args '{"collection":"<collection-id>","query":"<question>","vd-method":"< 0 or 1 or 2 or 3>", "k-value": "<knn value upon which search is done>", "logical-op","<-1 or -2 or 0 or 1 or 2>}'
```
Vector Distance Method:
- 0: Euclidean Distance
- 1: Cosine Similarity
- 2: Mahattan Method
- 3: Minkowski Method

Logical Operation
- -1: Less than
- -2: Less than equal to  
-  0: Equal to
-  1: Greater than
-  2: Greater than or equal to

### Get the count of vector records in a collection

```
python3 main.py count -- args '{"id":"<collection-id>"}'
```

### Get the list of vector records in a collection

```
python3 main.py list -- args '{"id":"<collection-id>"}'
```

## Author

Sree Hari - hari.tinyblitz@gmail.com
