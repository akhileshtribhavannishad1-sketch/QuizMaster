
# QuizMaster

A beginner-friendly quiz application built with Python (Flask) and JavaScript.

## Project overview

QuizMaster lets a student pick a quiz, enter a name, answer questions one at a time and see a score. Scores are saved and shown on a leaderboard. No login is needed.

This project is made for students who want to practice open source contributions. The code is small and simple, and there are many small improvements waiting to be done as issues.

## Tech used

- Python 3.11+ with Flask and Flask-SQLAlchemy
- SQLite by default, MySQL optional
- Plain HTML, CSS and JavaScript (Fetch API)
- pytest for tests
- GitHub Actions to run the tests

## Requirements

- Python 3.11 or newer
- Git

## Quick start on Windows

1. Install Python from [Python downloads](https://www.python.org/downloads/) and tick "Add Python to PATH" during installation.

2. Clone the repository:

   ```bash
   git clone https://github.com/NxtLabTech/QuizMaster.git
   cd QuizMaster
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   python run.py
   ```

6. Open http://127.0.0.1:5000 in your browser.

The database file is created automatically on the first run, and 3 sample quizzes are added.

## Optional: Use MySQL

1. Create an empty database, for example `quizmaster`.
2. Install the MySQL driver:

   ```bash
   pip install pymysql
   ```

3. Copy `.env.example` to `.env` and set the connection string:

   ```env
   DATABASE_URL=mysql+pymysql://username:password@localhost/quizmaster
   ```

4. Run the application:

   ```bash
   python run.py
   ```

If `DATABASE_URL` is not set, SQLite is used.

## Running tests

Run the following command:

```bash
pytest
```

The tests use an in-memory SQLite database, so your real data is not touched.

## API endpoints

All endpoints are under `/api` and use JSON.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/quizzes` | List quizzes. Optional `category` and `difficulty` filters |
| GET | `/api/quizzes/<id>` | Get one quiz with its questions (without correct answers) |
| POST | `/api/quizzes` | Create a quiz |
| POST | `/api/quizzes/<id>/questions` | Add a question to a quiz |
| POST | `/api/quizzes/<id>/submit` | Submit answers and get the result |
| GET | `/api/quizzes/<id>/leaderboard` | Get the top 10 attempts for a quiz |
| GET | `/api/stats` | Get total quizzes, total attempts, and average score per quiz |
| GET | `/api/health` | Check database health |

### Example request body for submitting answers

The answer keys are question IDs.

```json
{
  "player_name": "Asha",
  "answers": {
    "1": "B",
    "2": "C"
  },
  "time_taken_seconds": 42
}
```

### Error response example

```json
{
  "error": "Quiz not found"
}
```

## Troubleshooting

### Port 5000 is already in use

Close the other program using the port, or change the port in `run.py`, for example:

```python
app.run(debug=True, port=5001)
```

### Virtual environment does not activate in PowerShell

PowerShell may block scripts. Run this command in PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the virtual environment:

```powershell
venv\Scripts\activate
```

### ModuleNotFoundError

For example, if you see `No module named flask`, make sure your virtual environment is active and install the packages:

```bash
pip install -r requirements.txt
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before starting a contribution.

## License

MIT. See the [LICENSE](LICENSE) file.
