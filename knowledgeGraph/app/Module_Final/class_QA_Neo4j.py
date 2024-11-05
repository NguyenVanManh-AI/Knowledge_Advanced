import json
import time
from neo4j import GraphDatabase
from rank_bm25 import BM25Plus
from .utils import bm25_tokenizer
import google.generativeai as genai
from underthesea import text_normalize, sent_tokenize, pos_tag
import os 
from django.conf import settings

# Example Django model class
class QAUsingNeo4j():
    def __init__(self):
        self.entity_types = ['symptom', 'cause', 'disease', 'organ', 'treatment', 'lifestyle', 'test', 'food']
        self.uri = "neo4j+s://f895f551.databases.neo4j.io"                   # Địa chỉ database
        self.username = "neo4j"                                              # Username
        self.password = "CBkTUIkK_Sf2xR82K_UIycrMXwh-l-OEdEY9dNnxro8"        # Password
        self.current_api_index = -1
        self.GOOGLE_API_KEY = 'AIzaSyCswsFvn0wX5Zi2fbUX0MS43_1RgUSim3Y'
        self.API_KEYS = [
            'AIzaSyDmfK5ddS0zi8F6pdNaBETRUdT1vvKM_gw',
            'AIzaSyDOMTpoMwPQcZ5sWNwyOtJXhclEnv5dSgg',
            'AIzaSyCHta9yVQFqxmLZeOWp-WqzLakSdWtgOgs',
            'AIzaSyCGKAIV5kasWUHAeBdHn0G1ivnsai-o_Rg',
            'AIzaSyBF8dgYBO8Ke5OMnR67hRn_Wj7o4cySXps',
            'AIzaSyD-zSSiRxkQJDojDVyp7qHJ08sb4u_whOY',
            'AIzaSyDfVEwGcBdjpENJzdPrsPOGH347Nf_tkSc',
            # 'AIzaSyD7g2Iyeeb2VmkflHMS_Fa1gk70dEOcOLg',
            # 'AIzaSyDZBX0aTTKo_nOUyMR7DNT05UzxU7SuqaQ',
            # 'AIzaSyAIl7q_o1Yligo9IDxp-mS8CTKIieMfpTc',
            # 'AIzaSyAO-bb7fkWIpvf7EYjW0PPLWFQZDokrego',
            # 'AIzaSyANA0B90NfKQQ7wZ_sID8B8T17_FY4fEVk',
            # 'AIzaSyC3FW5DtjnDXVh7OYV8qgaEXFJ8fYHHs5Y',
            # 'AIzaSyDvTktdV60mQJXZdl8bPuO_9BPEmgGeklM',
        ]

    def __str__(self):
        return "QA using Neo4j"
    
    def split_by_first_verb(self, query):
        normalized_text = text_normalize(query)
        sentences = sent_tokenize(normalized_text)
        results = []
        for sentence in sentences:
            if 'là' in sentence:
                results.append([sentence.split('là')[0][:-1], 'là ' + sentence.split('là')[1][1:]])
            elif 'có' in sentence:
                results.append([sentence.split('có')[0][:-1], 'có ' + sentence.split('có')[1][1:]])
            else:
                pos_tags = pos_tag(sentence)
                first_verb_index = -1
                for index, (word, pos) in enumerate(pos_tags):
                    if pos == 'V':
                        if index == 0:
                            continue
                        first_verb_index = index
                        break
                if first_verb_index != -1:
                    part1 = ' '.join(word for word, _ in pos_tags[:first_verb_index])
                    part2 = ' '.join(word for word, _ in pos_tags[first_verb_index:])
                    results.append([part1.strip(), part2.strip()])
                else:
                    results.append([sentence.strip()])
        return results

    def find_node_by_text(self, tx, text):
        query = """
        MATCH (n)
        WHERE n.id = $text
        RETURN n
        """
        result = tx.run(query, text=text)
        data = result.data()
        if len(data) > 0:
            return data
        query = """
        MATCH (n)
        WHERE n.id CONTAINS $text
        RETURN n
        """
        result = tx.run(query, text=text)
        return result.data()

    def query_to_objs_relations(self, query):
        input_data = self.split_by_first_verb(query)
        print("input_data", input_data)
        output_relationships_path = os.path.join(settings.BASE_DIR,'app','Module_Final','output_relationships.json')
        with open(output_relationships_path, 'r', encoding='utf-8') as f:
            relationship_pairs = json.load(f)

        # Lấy câu đầu tiên trong query
        sentence1 = input_data[0]
        
        driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        with driver.session() as session:
            objs = []
            relations = []
            for text in sentence1:
                if text.strip() == "":
                    continue
                text = text.replace(' ', '_').replace(',', '_').replace('\'', '_').lower()

                for k, v in relationship_pairs.items(): 
                    if k in text: 
                        text = text.replace(k, "")
                        if text.startswith("_"):
                            text = text[1:]
                        if text.endswith("_"):
                            text = text[:-1]
                        relations.append(v)

                if "bệnh" in text:
                    text = text.replace("bệnh_", "")+"_disease"

                # Tìm kiếm text có phải là một node trong đồ thị không
                node = session.execute_read(self.find_node_by_text, text)

                if len(node)==1:
                    print(f"'{text}' là một node trong đồ thị: {node}")
                    objs.append(node[0])
                elif len(node)>1: 
                    print(f"'{text}' thuộc id của các node trong đồ thị: {node[:5]}")
                    print("len(node)", len(node))
                    objs.extend(node)
                else:
                    print(f"'{text}' không phải là một node trong đồ thị.")
        driver.close()
        return objs, relations

    def query_subgraph(self, tx, objs, relations):
        ids = [obj['n']['id'] for obj in objs]

        # Nếu `relations` không rỗng, thêm điều kiện cho mối quan hệ
        if relations:
            query = """
            MATCH (n)-[r]-(related)
            WHERE n.id IN $ids AND type(r) IN $relations
            RETURN n.id AS node_id, r.text AS relationship_text, related.id AS related_id
            """
            result = tx.run(query, ids=ids, relations=relations)
        else:
            # Nếu `relations` rỗng, lấy tất cả các mối quan hệ 1 hop liên quan đến `objs`
            query = """
            MATCH (n)-[r]-(related)
            WHERE n.id IN $ids
            RETURN n.id AS node_id, r.text AS relationship_text, related.id AS related_id
            """
            result = tx.run(query, ids=ids)

        return [(record["node_id"], record["relationship_text"], record["related_id"]) for record in result]

    def cypher_subgraph(self, objs, relations):
        ids = [obj['n']['id'] for obj in objs]
        
        # Nếu `relations` không rỗng, thêm điều kiện cho mối quan hệ
        if relations:
            query = f"""
            MATCH (n)-[r]-(related)
            WHERE n.id IN {ids} AND type(r) IN {relations}
            RETURN n.id AS node_id, r.text AS relationship_text, related.id AS related_id
            """
        else:
            # Nếu `relations` rỗng, lấy tất cả các mối quan hệ 1 hop liên quan đến `objs`
            query = f"""
            MATCH (n)-[r]-(related)
            WHERE n.id IN {ids}
            RETURN n.id AS node_id, r.text AS relationship_text, related.id AS related_id
            """
        return query

    def objs_relations_to_fulltext(self, objs, relations):
        driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        with driver.session() as session:
            subgraph_data = session.execute_read(self.query_subgraph, objs, relations)
            full_text = []
            set_text = set()
            for node, relationship_text, related_node in subgraph_data:
                if relationship_text not in set_text:
                    set_text.add(relationship_text)
                    full_text.append(f"Head: {node}\tTail: {related_node}\tText: {relationship_text}")
        driver.close()
        return full_text
    
    def objs_relations_to_cypher(self, objs, relations):
        driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        with driver.session() as session:
            subgraph_data = session.execute_read(self.query_subgraph, objs, relations)
            full_text = []
            set_text = set()
            for node, relationship_text, related_node in subgraph_data:
                if relationship_text not in set_text:
                    set_text.add(relationship_text)
                    full_text.append(f"Head: {node}\tTail: {related_node}\tText: {relationship_text}")
        driver.close()
        return full_text
    
    def bm25_search(self, full_text, query, top_k=5):
        documents = [bm25_tokenizer(text) for text in full_text]
        bm25 = BM25Plus(documents, k1=0.4, b=0.6)
        tokenized_query = bm25_tokenizer(query)
        scores = bm25.get_scores(tokenized_query)
        top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[
            :top_k
        ]
        top_k_results = [(full_text[i], scores[i]) for i in top_k_indices]
        return top_k_results

    def configure_api(self):
        # global current_api_index
        # global GOOGLE_API_KEY
        self.current_api_index = (self.current_api_index + 1) % len(self.API_KEYS)
        self.GOOGLE_API_KEY = self.API_KEYS[self.current_api_index]
        genai.configure(api_key=self.GOOGLE_API_KEY)
        print(f"API switched to index {self.current_api_index}: {self.GOOGLE_API_KEY}")

    # def get_answer(self, prompt):
    #     # GOOGLE_API_KEY = 'AIzaSyCswsFvn0wX5Zi2fbUX0MS43_1RgUSim3Y'
    #     import random
    #     random.shuffle(self.API_KEYS)
    #     # current_api_index = -1
    #     self.configure_api()
    #     model = genai.GenerativeModel(
    #         model_name='models/gemini-1.5-flash-latest')
    #     while(1):
    #         try:
    #             result = model.generate_content(prompt)
    #         except:
    #             time.sleep(3)
    #             self.configure_api()
    #             continue
    #         break
    #     return result
    def get_answer(self, prompt):
        # GOOGLE_API_KEY = 'AIzaSyCswsFvn0wX5Zi2fbUX0MS43_1RgUSim3Y'
        import random
        random.shuffle(self.API_KEYS)
        # current_api_index = -1
        self.configure_api()
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-flash-latest',
            generation_config={
                "temperature": 0.3,
                "top_p": 0.5,
                "top_k": 1
            },
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ])
        max_count = 6
        count = 0
        while(1):
            try:
                result = model.generate_content(prompt)
            except Exception as e:
                print("Error generating content: " + str(e))
                count += 1
                if count > max_count:
                    break
                time.sleep(3)
                self.configure_api()
                continue
            break
        return result

    def answer_query(self, query, full_text):
        top_k = 10
        top_k_results = self.bm25_search(full_text, query, top_k)
        passage = ""
        for idx, (doc, score) in enumerate(top_k_results):
            passage += f"Top {idx+1}:\n" + f"Đoạn văn: {doc}\n"

        prompt = f"""Bạn là một thuật toán AI, nhiệm vụ của bạn là trả lời các câu hỏi dựa trên thông tin được cung cấp, không được sử dụng bất kì một thông tin bên ngoài nào.

Hãy trả lời câu hỏi sau sử dụng top 10 đoạn văn liên quan nhất đến câu hỏi: 
query = "{query}"
{passage}"""
        answer = self.get_answer(prompt=prompt)
        return answer

    def full_question_answer(self, query): 
        objs, relations =  self.query_to_objs_relations(query)
        if len(objs)==0:
            return "Rất tiết chúng tôi không tìm thấy thông tin đối tượng mà bạn đề cập trong câu hỏi."
        
        full_text = self.objs_relations_to_fulltext(objs, relations)
        answer = self.answer_query(query, full_text)
        return answer

    # def full_question_answer(self, query): 
    #     objs, relations =  self.query_to_objs_relations(query)

    #     if len(objs)==0:
    #         return "Rất tiết chúng tôi không tìm thấy thông tin đối tượng mà bạn đề cập trong câu hỏi."
        
    #     full_text = self.objs_relations_to_fulltext(objs, relations)
    #     answer = self.answer_query(query, full_text)
    #     return answer
    
    def query_to_cypher(self, query): 
        objs, relations = self.query_to_objs_relations(query)
        cypher = self.cypher_subgraph(objs, relations)
        return cypher

    