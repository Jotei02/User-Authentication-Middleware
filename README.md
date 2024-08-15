pip install Flask PyJWT

How to Test:
python app.py
curl -u user1:password1 -X POST http://127.0.0.1:5000/login
curl -H "x-access-token: <your_token>" http://127.0.0.1:5000/protected


