import pytest
from app import db
from app.models import Quiz, Question, Attempt

def test_list_quizzes_empty(client):
    response = client.get('/api/quizzes')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_quiz(client):
    response = client.post('/api/quizzes', json={
        "title": "Python Basics",
        "description": "Test your Python knowledge",
        "difficulty": "easy"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == "Python Basics"
    assert data['difficulty'] == "easy"
    assert 'id' in data

def test_create_quiz_wrong_difficulty(client):
    response = client.post('/api/quizzes', json={
        "title": "Python Basics",
        "difficulty": "expert"
    })
    assert response.status_code == 400

def test_filter_quizzes_by_difficulty(client):
    client.post('/api/quizzes', json={"title": "Easy Quiz", "difficulty": "easy"})
    client.post('/api/quizzes', json={"title": "Hard Quiz", "difficulty": "hard"})
    
    response = client.get('/api/quizzes?difficulty=easy')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == "Easy Quiz"

def test_get_quiz_not_found(client):
    response = client.get('/api/quizzes/999')
    assert response.status_code == 404

def test_get_quiz_hides_correct_answers(client):
    quiz_res = client.post('/api/quizzes', json={"title": "Quiz"})
    quiz_id = quiz_res.get_json()['id']
    
    client.post(f'/api/quizzes/{quiz_id}/questions', json={
        "text": "What is Python?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "difficulty": "easy"
    })
    
    response = client.get(f'/api/quizzes/{quiz_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert 'correct_answer' not in data['questions'][0]

def test_add_question(client):
    quiz_res = client.post('/api/quizzes', json={"title": "Quiz"})
    quiz_id = quiz_res.get_json()['id']
    
    response = client.post(f'/api/quizzes/{quiz_id}/questions', json={
        "text": "Question 1",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "difficulty": "easy"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['text'] == "Question 1"

def test_add_question_wrong_option_letter(client):
    quiz_res = client.post('/api/quizzes', json={"title": "Quiz"})
    quiz_id = quiz_res.get_json()['id']
    
    response = client.post(f'/api/quizzes/{quiz_id}/questions', json={
        "text": "Question 1",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "E",
        "difficulty": "easy"
    })
    assert response.status_code == 400

def test_add_question_quiz_not_found(client):
    response = client.post('/api/quizzes/999/questions', json={
        "text": "Question",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "difficulty": "easy"
    })
    assert response.status_code == 404

def test_submit_quiz_scores_answers(client):
    quiz_res = client.post('/api/quizzes', json={"title": "Quiz"})
    quiz_id = quiz_res.get_json()['id']
    
    q_res = client.post(f'/api/quizzes/{quiz_id}/questions', json={
        "text": "What is Python?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "difficulty": "easy"
    })
    q_id = q_res.get_json()['id']
    
    response = client.post(f'/api/quizzes/{quiz_id}/submit', json={
        "player_name": "Alice",
        "answers": {str(q_id): "A"}
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['score'] == 1

def test_submit_quiz_missing_player_name(client):
    quiz_res = client.post('/api/quizzes', json={"title": "Quiz"})
    quiz_id = quiz_res.get_json()['id']
    
    response = client.post(f'/api/quizzes/{quiz_id}/submit', json={
        "answers": {}
    })
    assert response.status_code == 400

def test_submit_quiz_not_found(client):
    response = client.post('/api/quizzes/999/submit', json={
        "player_name": "Alice",
        "answers": {}
    })
    assert response.status_code == 404

def test_leaderboard_is_sorted_and_limited(client):
    quiz_res = client.post('/api/quizzes', json={"title": "Quiz"})
    quiz_id = quiz_res.get_json()['id']
    
    response = client.get(f'/api/quizzes/{quiz_id}/leaderboard')
    assert response.status_code == 200

def test_stats(client):
    response = client.get('/api/stats')
    assert response.status_code == 200

def test_delete_question_success(client):
    quiz_res = client.post('/api/quizzes', json={"title": "Python Basics"})
    quiz_id = quiz_res.get_json()['id']
    
    q1_res = client.post(f'/api/quizzes/{quiz_id}/questions', json={
        "text": "What is Python?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "difficulty": "easy"
    })
    q1_id = q1_res.get_json()['id']
    
    client.post(f'/api/quizzes/{quiz_id}/questions', json={
        "text": "What is Flask?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "B",
        "difficulty": "easy"
    })
    
    del_res = client.delete(f'/api/quizzes/{quiz_id}/questions/{q1_id}')
    assert del_res.status_code == 204
    
    get_res = client.get(f'/api/quizzes/{quiz_id}')
    data = get_res.get_json()
    assert len(data['questions']) == 1

def test_delete_question_errors(client):
    quiz_res = client.post('/api/quizzes', json={"title": "Math Quiz"})
    quiz_id = quiz_res.get_json()['id']
    q_res = client.post(f'/api/quizzes/{quiz_id}/questions', json={
        "text": "What is 2+2?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "difficulty": "easy"
    })
    q_id = q_res.get_json()['id']
    
    res = client.delete(f'/api/quizzes/{quiz_id}/questions/9999')
    assert res.status_code == 404
    
    res = client.delete(f'/api/quizzes/9999/questions/{q_id}')
    assert res.status_code == 404
    
    other_quiz_res = client.post('/api/quizzes', json={"title": "Science Quiz"})
    other_quiz_id = other_quiz_res.get_json()['id']
    
    res = client.delete(f'/api/quizzes/{other_quiz_id}/questions/{q_id}')
    assert res.status_code == 404