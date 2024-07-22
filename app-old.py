from flask import Flask, request, jsonify
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import init_db

app = Flask(__name__)

# Qdrant client configuration (modify as needed)
qdrant_client = QdrantClient(":memory:")

mycursor = init_db.mydb.cursor()

encoder = SentenceTransformer("all-MiniLM-L6-v2")



def create_collection():
    try:
        
       qdrant_client.recreate_collection(
        collection_name="conversation",
        vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),  # Vector size is defined by used model
        distance=models.Distance.COSINE,
            ),
        )
       print("Collection created successfully!")
        
    except Exception as e:
        print("Error creating collection:", e)

def upload_conversation():
    try:
        mycursor.execute("SELECT question, answer, voice FROM conversation")
        records = []
        x=0
        for (question, answer, voice) in mycursor:
            vector = encoder.encode(question).tolist()
            record = models.Record(id=x, vector=vector, payload={"question": question, "answer": answer, "voice": voice})
            records.append(record)
            x=x+1
        print("Collection uploaded successfully!")
        qdrant_client.upload_records(collection_name="conversation", records=records)
    except Exception as e:
        print("Error uploading conversation from MySQL:", e)


create_collection()
upload_conversation()


@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        user_query = request.json["sentence"]

        hits = qdrant_client.search(
            collection_name="conversation",
            query_vector=encoder.encode(user_query).tolist(),
            limit=1,
            score_threshold=0.5
        )

        if hits:
            best_answer = hits[0].payload["answer"]
            best_score = hits[0].score
            print(best_score)
            response = {"answer": best_answer}
        else:
            response = {"answer": "Sorry, I couldn't find an answer to your question."}

        return jsonify(response)

    except Exception as e:
        print("Error in chatbot function:", e)
        return jsonify({"error": "Something went wrong. Please try again later."})
    


@app.route("/recreate", methods=["GET"])
def re_upload_conversation():
    upload_conversation()
    response = {"response": "Collection uploaded successfully!"}
    return response



if __name__ == "__main__":
    app.run()
