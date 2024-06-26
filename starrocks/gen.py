import json

data = [
    {"studentID": 205, "firstName": "Natalie", "lastName": "Jones", "gender": "Female", "subject": "Maths", "score": 3.8, "timestampInEpoch": 1571900400000},
    {"studentID": 205, "firstName": "Natalie", "lastName": "Jones", "gender": "Female", "subject": "History", "score": 3.5, "timestampInEpoch": 1571900400000},
    {"studentID": 207, "firstName": "Bob", "lastName": "Lewis", "gender": "Male", "subject": "Maths", "score": 3.2, "timestampInEpoch": 1571900400000},
    {"studentID": 207, "firstName": "Bob", "lastName": "Lewis", "gender": "Male", "subject": "Chemistry", "score": 3.6, "timestampInEpoch": 1572418800000},
    {"studentID": 209, "firstName": "Jane", "lastName": "Doe", "gender": "Female", "subject": "Geography", "score": 3.8, "timestampInEpoch": 1572505200000},
    {"studentID": 209, "firstName": "Jane", "lastName": "Doe", "gender": "Female", "subject": "English", "score": 3.5, "timestampInEpoch": 1572505200000},
    {"studentID": 209, "firstName": "Jane", "lastName": "Doe", "gender": "Female", "subject": "Maths", "score": 3.2, "timestampInEpoch": 1572678000000},
    {"studentID": 209, "firstName": "Jane", "lastName": "Doe", "gender": "Female", "subject": "Physics", "score": 3.6, "timestampInEpoch": 1572678000000},
    {"studentID": 211, "firstName": "John", "lastName": "Doe", "gender": "Male", "subject": "Maths", "score": 3.8, "timestampInEpoch": 1572678000000},
    {"studentID": 211, "firstName": "John", "lastName": "Doe", "gender": "Male", "subject": "English", "score": 3.5, "timestampInEpoch": 1572678000000},
    {"studentID": 211, "firstName": "John", "lastName": "Doe", "gender": "Male", "subject": "History", "score": 3.2, "timestampInEpoch": 1572854400000},
    {"studentID": 212, "firstName": "Nick", "lastName": "Young", "gender": "Male", "subject": "History", "score": 3.6, "timestampInEpoch": 1572854400000}
]

for item in data:
    print(json.dumps(item))
