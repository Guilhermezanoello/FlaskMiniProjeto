import datetime
import uuid
from flask import Flask, redirect, render_template, url_for, request, jsonify
from azure.cosmos import CosmosClient

app = Flask(__name__)

# Configurações para conectar ao Cosmos DB
#ENDPOINT = 'https://cosmo-guilherme-miniprojeto.documents.azure.com:443/'
ENDPOINT = 'https://miniprojeto-edu-gui-joao-1.documents.azure.com:443/'
#KEY = '54d3zT0rS5ACZJl35atKzJOB4Wgxq0tZ3WkhbYofE8GOdRGeikCaAk8MGQ8GHxQPp3DLbMhq6VaMACDb1Pbymg=='
KEY = 'yh2sa1coqqzqgmZAZqdJDaZ70rEjozc4QNh86oWcjap8gmRzPBA807v84xs0uYzMtn7nKuifgAyIACDb5Olb5A=='
DATABASE_ID = 'QuizGami'
CONTAINER_ID = 'Questions'
SCORES_CONTAINER_ID = 'Scores'

# Inicializa o cliente do Cosmos DB
client = CosmosClient(ENDPOINT, KEY)
database = client.get_database_client(DATABASE_ID)
container = database.get_container_client(CONTAINER_ID)
scores_container = database.get_container_client(SCORES_CONTAINER_ID)

@app.route('/')
def index():
    query = 'SELECT DISTINCT c.category FROM c'
    items = list(container.query_items(query, enable_cross_partition_query=True))
    categories = {item['category'] for item in items}
    return render_template('index.html', categories=categories)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        category = request.form.get('category')
        query = f"SELECT * FROM c WHERE c.category = '{category}'"
        items = list(container.query_items(query, enable_cross_partition_query=True))

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
                },
                "correct": item["correct"]
            }
            questions.append(question)

        return render_template('quiz.html', category=category, questions=questions)
    return redirect(url_for('index'))

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    question_id = data.get('question_id')
    user_answer = data.get('user_answer')

    query = f"SELECT * FROM c WHERE c.id = '{question_id}'"
    items = list(container.query_items(query, enable_cross_partition_query=True))

    if not items:
        return jsonify({'error': 'Invalid question ID'}), 400

    question = items[0]
    correct_answer = question['correct']
    feedback_message = "Você ganhou 10 pontos!" if user_answer == correct_answer else "Você não pontuou nesta pergunta."
    points = 10 if user_answer == correct_answer else 0

    return jsonify({'feedback': feedback_message, 'points': points})

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    category = data.get('category')
    score = data.get('score')
    username = data.get('username')

    # Criar um item de pontuação
    score_item = {
        "id": str(uuid.uuid4()),  # Gera um id único
        "username": username,
        "category": category,
        "score": score,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    # Inserir o item no contêiner "Scores"
    container_scores = database.get_container_client("Scores")
    container_scores.create_item(body=score_item)

    return jsonify({"message": "Score saved successfully"}), 201

@app.route('/ranking')
def ranking():
    category = request.args.get('category')
    
    # Ajuste a consulta SQL para acessar o contêiner "Scores"
    query = f"SELECT * FROM c WHERE c.category = '{category}' ORDER BY c.score DESC"
    container_scores = database.get_container_client("Scores")
    items = list(container_scores.query_items(query, enable_cross_partition_query=True))

    return render_template('ranking.html', category=category, scores=items)

@app.route('/top_scores')
def top_scores():
    # Primeiro, vamos obter todas as categorias
    category_query = "SELECT DISTINCT c.category FROM c"
    categories = scores_container.query_items(query=category_query, enable_cross_partition_query=True)

    top_scores = {}

    # Para cada categoria, obtemos os três melhores scores
    for category in categories:
        category_name = category['category']
        score_query = f"""
        SELECT c.username, c.score
        FROM c
        WHERE c.category = '{category_name}'
        ORDER BY c.score DESC
        OFFSET 0 LIMIT 3
        """
        scores = scores_container.query_items(query=score_query, enable_cross_partition_query=True)
        top_scores[category_name] = list(scores)

    return render_template('top_scores.html', top_scores=top_scores)

if __name__ == '__main__':
    app.run(debug=True)
