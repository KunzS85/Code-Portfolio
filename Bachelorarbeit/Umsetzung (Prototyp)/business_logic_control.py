#from flask import Flask, request
import json
import deepl

from BertClassifier import BertClassifier

"""
app = Flask(__name__)
"""
DEEPL_AUTH_KEY = "8b33be93-e346-7390-78c1-66431e2e9ec5:fx"


def get_amd():
    """
    Each model must be stored in the all_label_dict. This is in JSON format.
    For each model the name of the model is used as key value.
    As value each model contains a dictionary which must contain the following elements:
    Name of the model (Must be identical to the key),
    a description of the model,
    the project path of the label_dictionary for the model,
    the path for the image of the weights of the trained model
    and the name of the base Bert model with which the weights were trained.
    :return: A dictionary with keys consisting of the model names and the value is a dictionary with "name",
     "description", "base_bert_name", "train_snapshot_url" and "label_dict_url" as keys.
    """
    with open("all_models_dict.json") as jsonFile:
        amd = json.load(jsonFile)
        jsonFile.close()
    return amd


def translate_input(text) -> str:
    """
    This method translates the German input text into English using DeepL API
    :param text: String with German text
    :return: Input string in english
    """
    if len(DEEPL_AUTH_KEY) > 2:
        translator = deepl.Translator(DEEPL_AUTH_KEY)
    else:
        translator = deepl.Translator(DEEPL_AUTH_KEY)

    # Check account usage
    usage = translator.get_usage()
    if usage.character.limit_exceeded:
        print("Character limit exceeded.")
    else:
        print(f"Character usage: {usage.character}")

    text_EN = translator.translate_text(text, source_lang="DE", target_lang="EN-GB")
    #print(text_EN)

    return text_EN.text


def init_model(name):
    """
    Initializes a BertClassifier class, within the scope of the supplied name. The name must be contained in the
    all_models_dict and its key in the value must match the key contained in this method.
    :param name: name of the model which should be initialized
    :return: The reference to the instance of the BertClassifier class
    """
    amd = get_amd()
    a_model = BertClassifier(amd[name]["name"], amd[name]["base_bert_name"], amd[name]["train_snapshot_url"],
                             amd[name]["label_dict_url"])
    return a_model


# @app.route('/')
def get_models_names() -> dict:
    """
    This method returns a dictionary with all names and descriptions
    of the available models as part of the all_models_dict.
    :return: A dictionary with keys consisting of the model names and the value is a
    dictionary with "name" and "description" as keys.
    """
    models = {}
    amd = get_amd()
    for k, v in amd.items():
        models[k] = {
            "name": v["name"],
            "description": v["description"]
        }
    return models


# @app.route(/<name>)
def get_prediction(name, text) -> dict:
    """
    The method first translates the text into English, initializes a BertClassifier of the appropriate type with the
    key of the named, and executes the get_prediction method of the BertClassifier with the translated text.
    :param name: Name of the model to be instantiated. This must be contained in the all_models_dict
    :param text: German text which is the basis for the calculation
    :return: A dictionary whose keys are the labels trained in this model and whose value consists of a dictionary
    with the keys "name", "synonym", "code", "index" and "probability".
    """
    #print(f"in get_prediction mit {name}, {text}")
    translated_text = translate_input(text)
    #print(f"translated text: {translated_text}")
    model = init_model(name)
    prediction = model.get_prediction(translated_text)
    #print(f"prediction: {prediction}")
    return prediction


if __name__ == '__main__':
    print("start business logic control")
    options = get_models_names()
    for k, v in options.items():
        print(k)
        print(v)
    name = "model3"
    text = "Comprehensive care of lower urinary tract infections"
    m = init_model(name)
    prediction = m.get_prediction(text)
    print(prediction)
