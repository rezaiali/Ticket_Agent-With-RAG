from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import Optional
from pathlib import Path

class ChromaRAG():
    def __init__(self,collectionName,DbLocation,embedding:OllamaEmbeddings):
        self._colloectionName=collectionName
        self._Dblocation=DbLocation
        self._embedding=embedding
        self._doc=""
        self.vector_store=None
    @property
    def DocumentPath(self):
        return self._doc
    @DocumentPath.setter
    def DocumentPath(self,value):
        self._doc =value


    def _createchunkText(self,chucksize:int):
        chucks:list[str]=[]
        _file=Path(self._doc)
        with open(_file,"r", encoding="utf-8") as file:
            content = file.read()
        startingPoint=0    
        contentLen=len(content)
        if startingPoint == contentLen:
            raise RuntimeError("Error reading file")
        
        while startingPoint < contentLen:
            if startingPoint >= contentLen:
                startingPoint = startingPoint - contentLen
                chuck=content[startingPoint: chucksize]
                chucks.append(chuck)
            else:
                chuck=content[startingPoint: chucksize]
                chucks.append(chuck)
                startingPoint = chucksize
                chucksize = chucksize * 2
            
        return chucks

    def createChromaVectorStore(self):
        self.vector_store=Chroma(
            collection_name=self._colloectionName,
            persist_directory=self._Dblocation,
            embedding_function=self._embedding
                            )
        if self._doc:
            chunks=self._createchunkText(80)
            self.vector_store.add_documents
            for index, _chuck in enumerate(chunks):
                _doc=[Document(page_content=_chuck,
                            metadata={"source": _doc, "chunk": index},
                            )]
            self.vector_store.add_documents(_doc,ids=[f"kb-{index}" for index in range(len(_doc))])

            return self.vector_store
    def retiever(self,k:int = 5):
        if self.vector_store:
           retiever=self.vector_store.as_retriever(search_kwargs={"k": k})
        return retiever
