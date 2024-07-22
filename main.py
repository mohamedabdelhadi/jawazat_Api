import logging
import logging_config
from easygoogletranslate import EasyGoogleTranslate
from mqtt_helper import connect_mqtt, publish_message
from flask import Flask, request, jsonify
from flask_cors import CORS
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import init_db
import mysql.connector
import time
import json
import re
from datetime import date

app = Flask(__name__)    
CORS(app, origins=['*'],methods=['GET', 'POST','PUT','DELETE'])  # Allow specific methods





logger = logging.getLogger(__name__)
mqtt_client = connect_mqtt()  # Connect on application startup
mqtt_client.loop_start()

qdrant_client = QdrantClient(":memory:")
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# mqtt = qss_api.qss()
# mqtt.stop_mic()

# Open a connection pool to avoid creating a new one for every request
db_pool = mysql.connector.pooling.MySQLConnectionPool(pool_reset_session=True,
                                                      **init_db.config)
# API Key
jawazat_api_key = '@J2w1_z!@T?zz'

# API Key Validation Middleware
def authorize_api_key(function):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('apikey')
        if not api_key or api_key != jawazat_api_key:
            print('Unauthorized access for route:', request.path)
            return jsonify({'message': 'Unauthorized'}), 401
        return function(*args, **kwargs)
    return decorated_function


def init_update_collection():
    try:
        qdrant_client.recreate_collection(
            collection_name="conversation",
            vectors_config=models.VectorParams(
                size=encoder.get_sentence_embedding_dimension(), 
                distance=models.Distance.COSINE,
            ),
        )

        # 2. Fetch data from MySQL
        connection = db_pool.get_connection()
        mycursor = connection.cursor()
        mycursor.execute("SELECT question, answer,answer_ar,answer_fr,answer_zh FROM conversation")
        records = []
        x = 0
        for (question, answer,answer_ar,answer_fr,answer_zh) in mycursor:
            vector = encoder.encode(question).tolist()
            record = models.Record(id=x, vector=vector, payload={"question": question, "answer": answer, "answer_ar": answer_ar, "answer_fr": answer_fr, "answer_zh": answer_zh})
            records.append(record)
            x = x + 1

        # 3. Upload records  
        qdrant_client.upload_records(collection_name="conversation", records=records)
        logger.info("Collection updated successfully!")

    except Exception as e:
        logger.error("Error updating collection:", e)
    finally:
        if mycursor:
            mycursor.close()
        if connection:  
            connection.close()


init_update_collection()


def run():


    app.run(host="0.0.0.0",debug=True)



def extract_link_and_text(text):

    # Enhanced regex covering more link types
    link_pattern = r"""
        (?i)\b(?:  
            https?://|  
            www\d?\.|  
            [\w-]+(?:\.[\w-]+)+\.? 
        ) 
        (?:     
            [\w.,@?^=%&:/~+#-]* 
        )?
        \b  # Word boundary (end) 
    """

    match = re.search(link_pattern, text, flags=re.VERBOSE) 

    if match:
        link = match.group(0)
        text = text.replace(link, "")  # Remove link from the original text
    else:
        link = "0"

    return text, link

@app.route("/sentence", methods=["POST"]) 
def process_sentence():

    data = request.get_json()
    print(data)
    lang = data["lang"]
    sentence = data["sentence"]

    if sentence:
        response = get_answer(sentence,lang)
        try:
            publish_message(mqtt_client, "zbos/CA019UBT20000010/dialog/set", response.json['answer'],lang)
            return response
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500 
    else:
        logger.error("Missing Sentence Or Lang")
        return jsonify({"error": "Missing Sentence Or Lang"}), 400



def translate(sentence,src,dest):
    translator = EasyGoogleTranslate(source_language=src,target_language=dest,timeout=10)
    result = translator.translate(sentence)
    return result

def get_answer(sentence,lang):
    try:
        if lang!="en-US":
            sentence = translate(sentence,lang[:2],"en",)

        hits = qdrant_client.search(
            collection_name="conversation",
            query_vector=encoder.encode(sentence).tolist(),
            limit=1,
            score_threshold=0.5)
        if hits:
            best_answer = hits[0].payload["answer"]
            #best_score = hits[0].score
            
            if lang=="en-US":
                txt_answer,link_answer = extract_link_and_text(best_answer)
                response=  {"answer": txt_answer,"link":link_answer}
            elif lang=="ar-SA":
                txt_answer,link_answer = extract_link_and_text(hits[0].payload["answer_ar"])
                response=  {"answer": txt_answer,"link":link_answer}
            elif lang=="fr-FR":
                txt_answer,link_answer = extract_link_and_text(hits[0].payload["answer_fr"])
                response=  {"answer": txt_answer,"link":link_answer}
            elif lang=="zh-CN":
                txt_answer,link_answer = extract_link_and_text(hits[0].payload["answer_zh"])
                response=  {"answer": txt_answer,"link":link_answer}

            else:
                response=  {"answer":translate(best_answer,lang[:2],"en")}
        elif lang=="ar-SA":
           response = {"answer":"عذراً لم افهمك يرجى طرح السؤال بصيغة أخرى","link":"0"}  
        elif lang=="en-US":
           response = {"answer":"Sorry, I did not understand you. Please ask the question in another form","link":"0"}  
        elif lang=="fr-FR":
           response = {"answer":"Désolé, je ne vous ai pas compris. Veuillez poser la question sous une autre forme","link":"0"}  
        elif lang=="zh-CN":
           response = {"answer":"抱歉，我没听懂你的意思。 请以其他形式提出问题","link":"0"}  

        return jsonify(response)

    except Exception as e:
        logger.error("Error in get_answer function:", e)
        return jsonify({"error": "Something went wrong. Please try again later."})






################### Survey API ################

@app.route('/survey', methods=['POST']) 
def survey():
    def generate_id():  # ID generation function
        timestamp = str(int(time.time() * 1000))
        return timestamp[-12:]

    connection = None
    cursor = None
    try:
        survey = request.json

        # Validate numbers
        if not all(str(key).isdigit() for key in survey.keys()) or \
           not all(str(value).isdigit() for value in survey.values()):
            return jsonify({'error': 'Invalid request body'}), 400

        # Get a connection from the pool
        connection = db_pool.get_connection()
        cursor = connection.cursor()

        session_id = generate_id()
        values = [(session_id, questionId, answerId,date.today()) for questionId, answerId in survey.items()]

        try:
            cursor.executemany("INSERT INTO surveys (session_id, question_id, answer_id,date) VALUES (%s, %s, %s,%s)", values)
            connection.commit()
            logger.info('Survey answers saved successfully')
            return jsonify({'message': 'Answers saved successfully'}), 201
        except mysql.connector.Error as error:
            logger.error('Error inserting recordssss:', error)
            return jsonify({'message': 'Error inserting records'}), 500
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    except Exception as e:  # General exception handling
        print('Error processing request:', e)
        return jsonify({'error': 'Failed to process request'}), 500


########## get robot functions status #########
@app.route('/getRobotFunctions',methods=['GET'])
def get_robot_functions():
    connection = None
    cursor = None
    query = 'SELECT name, status FROM robot_functions'

    try:
        connection = db_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()  
        data = [dict(zip([column[0] for column in cursor.description], row)) 
                for row in results]  # Convert query results to JSON 

        return jsonify(data), 200

    except mysql.connector.Error as error:
        logger.error('Error getting records:', error.msg)
        return jsonify({'error': str(error)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/getSurveyQuestions', methods=['GET'])
def getSurveyQuestions():
    connection = None
    cursor = None
    query = 'SELECT id,question,question_ar,question_fr,question_zh FROM questions'
    update_query = 'UPDATE functions_update_flag SET is_updated = 0 WHERE name = "survey"'

    try:
        isupdated=check_update_flag("survey")
        if not isupdated:
            return json.dumps([])
        connection = db_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall() 
        data = [dict(zip([column[0] for column in cursor.description], row)) 
                for row in results]  
        cursor = connection.cursor() 
        cursor.execute(update_query)
        connection.commit()

        return jsonify("options", data), 200

    except mysql.connector.Error as error:
        logger.error("Database error occurred: %s", error)
        return jsonify({'error': "An unexpected error occurred"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def check_update_flag(function_name):
    connection = None
    cursor = None
    query = 'SELECT is_updated FROM functions_update_flag WHERE name =%s'

    try:
        connection = db_pool.get_connection()
        cursor = connection.cursor(dictionary=True)  # Return results as dictionaries
        cursor.execute(query, (function_name,))
        result = cursor.fetchone()  # Fetch only the first row

        if result:
            return result['is_updated']  # Access the value directly
        else:
            return False

    except mysql.connector.Error as error:
        logger.error("Database error occurred: %s", error)
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



######## Dashboard api's #########

@app.route('/delete', methods=['DELETE'])
def delete_data():
    connection = None
    cursor = None 
    try:
        id = request.args.get('id')
        type = request.args.get('type')
        if id is None or type is None:
            return jsonify({'error': 'incorrect request body'}), 400
        

        connection = db_pool.get_connection()
        cursor = connection.cursor()

        if type == 'ask_me':
            delete_query = "DELETE FROM conversation WHERE id = %s" 
        elif type == 'survey':
            delete_query = "DELETE FROM questions WHERE id = %s" 
        else:
            return jsonify({'error': 'Invalid type'}), 400

        cursor.execute(delete_query, (id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'Data not found'}), 404  
        else:
            on_database_update(type)
            return jsonify({'message': 'Data deleted successfully'}), 200

    except mysql.connector.Error as error:
        logger.error("Database error occurred: %s", error)
        return jsonify({'error': "An unexpected error occurred"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
            
            
            
@app.route('/add', methods=['POST']) 
def add_data():
    connection = None
    cursor = None 
    try:
        data = request.get_json()
       
        if not data or 'type' not in data:
            return jsonify({'error': 'incorrect request body'}), 400
        
        type = data.get('type')
        connection = db_pool.get_connection()
        cursor = connection.cursor()
        bulktranslator = EasyGoogleTranslate()

        if type == 'ask_me':
            insert_query = "INSERT INTO conversation (question, question_ar, question_fr, question_zh,answer,answer_ar,answer_fr,answer_zh,category) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s)"
            translated_question = bulktranslator.translate(text=data['arqst'], target_language=['en', 'fr', 'zh-TW'])
            if data['enqst']=="":
                data['enqst']=translated_question[0]
            if data['frqst']=="":
                data['frqst']=translated_question[1]
            if data['chqst']=="":
                data['chqst']=translated_question[2]
                
            translated_answer = bulktranslator.translate(text=data['arans'], target_language=['en', 'fr', 'zh-TW'])
            if data['enans']=="":
                data['enans']=translated_answer[0]
            if data['frans']=="":
                data['frans']=translated_answer[1]
            if data['chans']=="":
                data['chans']=translated_answer[2]
                
                
            values = (data['enqst'], data['arqst'], data['frqst'], data['chqst'], data['enans'], data['arans'], data['frans'], data['chans'],data['cat_id'])
            
        elif type == 'survey':
            insert_query = "INSERT INTO questions (question, question_ar, question_fr, question_zh) VALUES (%s, %s, %s, %s)"
            translated_survey = bulktranslator.translate(text=data['artxt'], target_language=['en', 'fr', 'zh-TW'])
            if data['entxt']=="":
                data['entxt']=translated_survey[0]
            if data['frtxt']=="":
                data['frtxt']=translated_survey[1]
            if data['chtxt']=="":
                data['chtxt']=translated_survey[2]
            values = (data['entxt'], data['artxt'], data['frtxt'], data['chtxt'])

        else:
            return jsonify({'error': 'Invalid type'}), 400

        cursor.execute(insert_query, values)
        connection.commit()
        

        if cursor.rowcount == 0:
            return jsonify({'message': 'failed to insert'}), 404  
        else:
            on_database_update(type)
            return jsonify({'message': 'Data inserted successfully'}), 200

    except mysql.connector.Error as error:
        logger.error("Database error occurred: %s", error)
        return jsonify({'error': "An unexpected error occurred"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
            
            
            
            
@app.route('/update', methods=['PUT'])
def update_data():
    connection = None
    cursor = None 
    try:
        data = request.get_json()
       
        if not data or 'type' not in data or 'id' not in data:
            return jsonify({'error': 'incorrect request body'}), 400
        
        type = data.get('type')
        update_id = data.get('id')
        connection = db_pool.get_connection()
        cursor = connection.cursor()
        bulktranslator = EasyGoogleTranslate()

        if type == 'ask_me':
                       
            required_keys = ['enqst', 'frqst', 'chqst', 'arqst','enans', 'frans', 'chans', 'arans','cat_id']
            if not all(key in data for key in required_keys):
                return jsonify({'error': 'incorrect request body'}), 400
            
            update_query = "UPDATE conversation set question=%s, question_ar=%s, question_fr=%s, question_zh=%s,answer=%s,answer_ar=%s,answer_fr=%s,answer_zh=%s,category=%s WHERE id=%s"
            translated_question = bulktranslator.translate(text=data['arqst'], target_language=['en', 'fr', 'zh-TW'])
            if data['enqst']=="":
                data['enqst']=translated_question[0]
            if data['frqst']=="":
                data['frqst']=translated_question[1]
            if data['chqst']=="":
                data['chqst']=translated_question[2]
                
            translated_answer = bulktranslator.translate(text=data['arans'], target_language=['en', 'fr', 'zh-TW'])
            if data['enans']=="":
                data['enans']=translated_answer[0]
            if data['frans']=="":
                data['frans']=translated_answer[1]
            if data['chans']=="":
                data['chans']=translated_answer[2]
                
                
            values = (data['enqst'], data['arqst'], data['frqst'], data['chqst'], data['enans'], data['arans'], data['frans'], data['chans'],data['cat_id'],update_id)
            
        elif type == 'survey':
            
            required_keys = ['entxt', 'frtxt', 'chtxt', 'artxt']
            if not all(key in data for key in required_keys):
                return jsonify({'error': 'incorrect request body'}), 400
            
            update_query = "UPDATE questions set question=%s, question_ar=%s, question_fr=%s, question_zh=%s WHERE id=%s"
            translated_survey = bulktranslator.translate(text=data['artxt'], target_language=['en', 'fr', 'zh-TW'])
            if data['entxt']=="" or not data['entxt']:
                data['entxt']=translated_survey[0]
            if data['frtxt']=="":
                data['frtxt']=translated_survey[1]
            if data['chtxt']=="":
                data['chtxt']=translated_survey[2]
            values = (data['entxt'], data['artxt'], data['frtxt'], data['chtxt'],update_id)
        elif type == 'toggle':
            update_query = "UPDATE robot_functions set status=NOT status WHERE id=%s"
            values = (update_id,)

        else:
            return jsonify({'error': 'Invalid type'}), 400

        cursor.execute(update_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'failed to update'}), 404  
        else:
            on_database_update(type)
            return jsonify({'message': 'Data updated successfully'}), 200

    except mysql.connector.Error as error:
        logger.error("Database error occurred: %s", error)
        return jsonify({'error': "An unexpected error occurred"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
            
            
def on_database_update(function_name):
    if function_name == 'survey':
        update_connection = None
        update_cursor = None 
        try:
            update_connection = db_pool.get_connection()
            update_cursor = update_connection.cursor()
            update_query = 'UPDATE functions_update_flag SET is_updated = 1 WHERE name = %s'
            update_cursor.execute(update_query, (function_name,))
            update_connection.commit()
        except mysql.connector.Error as error:
            logger.error('Error on_database_update:', error.msg)

            return jsonify({'error': str(error)}), 500

        finally:
            if update_cursor:
                update_cursor.close()
            if update_connection:
                update_connection.close()
    elif function_name == 'ask_me':
        init_update_collection()
        

@app.route('/add_robot_usage', methods=['POST'])
def add_robot_usage():
    connection = None
    cursor = None 
    try:
        data = request.get_json()
       
        if not data or 'name' not in data or 'lang' not in data:
            logger.error('incorrect request body')
            return jsonify({'error': 'incorrect request body'}), 400
        
        lang = data.get('lang')
        allowed_languages = ["ar", "en", "fr", "zh"]  # Define allowed lang codes

        if lang not in allowed_languages:
            logger.error('Invalid language code :'+lang)
            return jsonify({'error': 'Invalid language code'}), 400        
        
        function_name = data.get('name')
        allowed_function_names = ["ask_me", "procedures", "sugg_comp", "support","survey"]  # Define allowed function names

        if function_name not in allowed_function_names:
            logger.error('Invalid function name :'+function_name)
            return jsonify({'error': 'Invalid function name'}), 400
        
        connection = db_pool.get_connection()
        cursor = connection.cursor()

        insert_query = "INSERT INTO robot_usage (name, lang) VALUES (%s, %s)"
        values = (function_name, lang)

        cursor.execute(insert_query, values)
        connection.commit()
        
        logger.info('Robot usage inserted successfully')
        return jsonify({'message': 'Robot usage inserted successfully'}), 201

    except mysql.connector.Error as error:
        logger.error("Database error occurred: %s", error)
        return jsonify({'error': "An unexpected error occurred"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
          
          
          
@app.route('/status', methods=['GET']) 
def getstatus():
    return "Robot server is running"  
            
            
app.view_functions['process_sentence'] = authorize_api_key(app.view_functions['process_sentence'])
app.view_functions['survey'] = authorize_api_key(app.view_functions['survey'])
app.view_functions['get_robot_functions'] = authorize_api_key(app.view_functions['get_robot_functions'])
app.view_functions['getSurveyQuestions'] = authorize_api_key(app.view_functions['getSurveyQuestions'])
app.view_functions['delete_data'] = authorize_api_key(app.view_functions['delete_data'])
app.view_functions['add_data'] = authorize_api_key(app.view_functions['add_data'])
app.view_functions['update_data'] = authorize_api_key(app.view_functions['update_data'])
app.view_functions['add_robot_usage'] = authorize_api_key(app.view_functions['add_robot_usage'])



