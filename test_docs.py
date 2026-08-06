from Project.indexing.data_ingestion import git_ingestion
docs = git_ingestion('https://github.com/Anurag07-crypto/chatbot.git')
for doc in docs:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content preview: {doc.page_content[:200]}...")
