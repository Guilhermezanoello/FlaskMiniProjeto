from flask import Flask, render_template, request, url_for
import os
from azure.cosmos import CosmosClient

app = Flask(__name__)

# Configurações para conectar ao Cosmos DB
ENDPOINT = 'https://miniprojeto-edu-gui-joao1.documents.azure.com:443/'
KEY = '6Jf1yWhVGBCV3RVQLN1dW88SxWQguWT8pIHnPGUmKUTpo50KK5t6gtnSn7y2m1VUlatkkOurLR3GACDbwB8zHA=='
DATABASE_ID = 'QuizGami'
CONTAINER_ID = 'Questions'

# Inicializa o cliente do Cosmos DB
client = CosmosClient(ENDPOINT, KEY)
database = client.get_database_client(DATABASE_ID)
container = database.get_container_client(CONTAINER_ID)

@app.route('/', methods=['POST'])
def quiz():
    if request.method == 'POST':
        category = request.form['category']

        # Consulta ao Cosmos DB
        query = f"SELECT * FROM c WHERE c.category = '{category}'"
        items = list(container.query_items(query, enable_cross_partition_query=True))

        # Processamento das perguntas recuperadas
        questions = []
        for item in items:
            question = {
                "id": item["id"],
                "question": item["question"],
                "options": {
                    "a": item["options"]["a"],
                    "b": item["options"]["b"],
                    "c": item["options"]["c"],
                    "d": item["options"]["d"],
                }
            }
            questions.append(question)

    # Renderização do template do quiz com as perguntas recuperadas
    return render_template('quiz.html', category=category, questions=questions)
if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=True)
