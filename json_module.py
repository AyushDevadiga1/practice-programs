import json 
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

y = ['apple','mango','kiwi']

z = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(json.dumps(x))
print(json.dumps(y))
print(json.dumps(z))

# if we are saving to a json file than we can use json.dump

with open('json_file.json','w') as f:
    json.dump(z,f)