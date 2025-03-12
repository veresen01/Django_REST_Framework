from requests import post


url = "http://127.0.0.1:8000/api/register/"
data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "age": 30,
    "job": "Developer"
}


response = post(url, data=data)


if response.status_code == 201:
    print("User created successfully:", response.json())
else:
    print("Error:", response.json())