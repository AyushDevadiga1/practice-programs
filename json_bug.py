# import json
# model_config = {
#     "model_name": "RandomForest",
#     "grid_dimensions": (100, 50)  # This is a TUPLE (immutable)
# }

# with open("config.json","w") as f:
#     json.dump(model_config,f)

# # The tuple converts to list which is mutable

# with open("config.json","r") as f:
#     loaded_config = json.load(f)

# print(f"Loaded type: {type(loaded_config['grid_dimensions'])}")

# try:
#     # Your pipeline treats it as an immutable dictionary key (tuples can be keys, lists cannot!)
#     test_dict = {loaded_config['grid_dimensions']: "Active Grid"}
#     print("Success!")
# except TypeError as e:
#     print(f"\n❌ CRASHED IN PRODUCTION! Error: {e}")
#     print("Why? Because JSON converted our tuple into a mutable LIST, and lists cannot be dictionary keys!")


import joblib

model_config = {
    "model_name": "RandomForest",
    "grid_dimensions": (100, 50)  # The exact same tuple
}

# Fix: Use joblib instead of JSON to save exact Python types
joblib.dump(model_config, "config.joblib")

# Load it back
loaded_config = joblib.load("config.joblib")

print(f"Loaded type: {type(loaded_config['grid_dimensions'])}")

# Test the pipeline logic again
test_dict = {loaded_config['grid_dimensions']: "Active Grid"}
print("✅ FIXED! The tuple stayed a tuple, and the production pipeline didn't crash.")
