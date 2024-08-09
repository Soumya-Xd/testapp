# MEDICINE INFORMATION FOUNDER
# LINK
https://testapp-8v3q3eukn3sxpse8tbqob3.streamlit.app/

# Medicine Similarity Model

This repository contains a Python script to find the most similar medicine name from a list using TF-IDF and Nearest Neighbors.

## Functions

### `train_model(data)`
Trains a Nearest Neighbors model using TF-IDF features of medicine names.

**Parameters:**
- `data` (dict): Dictionary with a 'name' key containing a list of medicine names.

**Returns:**
- `(vectorizer, model)`: The trained vectorizer and model.

### `find_medicine(vectorizer, model, medicine_name)`
Finds the index of the most similar medicine to the given name.

**Parameters:**
- `vectorizer` (TfidfVectorizer): The vectorizer used for transforming text data.
- `model` (NearestNeighbors): The trained Nearest Neighbors model.
- `medicine_name` (str): The name of the medicine to find.

**Returns:**
- `int`: The index of the nearest medicine in the training data.





# dataset

https://www.kaggle.com/datasets/shudhanshusingh/250k-medicines-usage-side-effects-and-substitutes


