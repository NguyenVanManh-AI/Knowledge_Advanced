from class_QA_Neo4j import QAUsingNeo4j

qa_neo4j = QAUsingNeo4j()

query = "Mất trí nhớ là triệu chứng của bệnh gì?"
answer = qa_neo4j.full_question_answer(query)

print(answer.text)