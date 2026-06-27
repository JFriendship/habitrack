from datetime import date

def test_complete_habit(client, auth_headers, created_habit):
    response = client.post(f"/api/habits/{created_habit.id}/complete", headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["habit_id"] == created_habit.id

def test_habits_completion_history(client, auth_headers, created_habit):
    client.post(f"/api/habits/{created_habit.id}/complete", headers=auth_headers)

    response = client.get(f"/api/habits/{created_habit.id}/completions", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1

def test_completion_status(client, auth_headers, created_habit):
    today = date.today().isoformat()

    response = client.get(f"/api/habits/{created_habit.id}/completed-on/{today}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == {"completed": False}

def test_habit_completion_deletion(client, auth_headers, created_habit):
    today = date.today().isoformat()

    client.post(f"/api/habits/{created_habit.id}/complete", headers=auth_headers)

    response = client.delete(f"/api/habits/{created_habit.id}/complete/{today}", headers=auth_headers)

    assert response.status_code == 204