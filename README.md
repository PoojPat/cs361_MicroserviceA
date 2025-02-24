# CS361 Microservice A: Quiz Statistics Microservice
This microservice tracks and analyzes user performance on quizzes. It provides endpoints to record quiz scores, retrieve user-specific statistcs, and retrieve difficulty-based statistics.

## Communication Contract

### Requesting Data
To request data from the microservice, send HTTP requests to the appropriate endpoints. Below are the details for each endpoint. 

1.) Record a Quiz Score
- Endpoint: ```POST /record-score```
- Example Call:
```
import requests
data = {
    "user_id": 123,
    "quiz_id": 1,
    "score": 85.0,
    "difficulty": "Medium"
}
response = requests.post("http://localhost:5000/record-score", json=data)
print(response.json())
```

2.) Retrieve User Statistics
- Endpoint: ```GET /user-stats/<int:user_id>```
- Example Call:
```
import requests

user_id = 123
response = requests.get(f"http://localhost:5000/user-stats/{user_id}")
print(response.json())
```

3.) Retrieve Difficulty-Based Statistics
- Endpoint: ```GET /difficulty-stats/<string:difficulty>```
- Example Call:
```
import requests

difficulty = "Medium"
response = requests.get(f"http://localhost:5000/difficulty-stats/{difficulty}")
print(response.json())
```

### Receiving Data
The microservice responds with JSON data. Below are examples of responses for each endpoint. 

1.) Record a Quiz Score
- Response:
```
{
  "message": "Score recorded successfully"
}
```

2.) Retrieve User Statistics
- Response:
```
{
  "user_id": 123,
  "total_quizzes": 3,
  "average_score": 85.0,
  "highest_score": 95.0,
  "lowest_score": 75.0,
  "timestamp": "2025-02-23T12:34:56.789012"
}
```

3.) Retrieve Difficulty-Based Statistics
- Response:
```
{
  "difficulty": "Medium",
  "average_score": 80.0,
  "total_attempts": 5,
  "timestamp": "2024-02-23T12:34:56.789012"
}
```
