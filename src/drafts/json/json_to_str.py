import json

# Словарь Python
data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

print(type(data))
print(data)

# Преобразование словаря в строку JSON
json_data = json.dumps(data)

print(type(json_data))
print(json_data)    # json

from_json_data = json.loads(json_data)

print(type(from_json_data))
print(from_json_data)
