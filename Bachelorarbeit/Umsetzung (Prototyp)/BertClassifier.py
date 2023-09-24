import torch
from transformers import BertTokenizer, BertForSequenceClassification
import json



class BertClassifier:
    """
    This class contains the name of the currently used BERT model, the name of the BERT model used by this model,
     the reference on which device (CPU or GPU) the model is executed, an instance of the
     BERT tokenizer of the base BERT model and an instance of a BertForSequenceClassification model with
     the weights from the training.
    """
    def __init__(self, name, base_bert_name, train_snapshot_url, label_dict_url):

        with open(label_dict_url) as jsonFile:
            self.model_label_dict = json.load(jsonFile)
            jsonFile.close()

        self.name = name
        self.base_bert_name = base_bert_name
        self.device = torch.device("cpu")
        #print("loading tokenizer.....")
        self.tokenizer = BertTokenizer.from_pretrained(self.base_bert_name)
        #print("loading model......")
        self.model = BertForSequenceClassification.from_pretrained(self.base_bert_name,
                                                                   num_labels=len(self.model_label_dict),
                                                                   return_dict=True)
        #print("initialize state_dict......")
        self.model.load_state_dict(torch.load(train_snapshot_url, map_location=self.device))

    def get_prediction(self, text: str) -> dict:
        """
        The method requires a text in English. This is processed with the BERT model stored in this class.
         The output of the model is normalized with a softmax layer and the results are stored in a copy of Label_dict
         and used as return value.
        :param text: Text in english
        :return: Label dictionary with all information available for the individual output node.
        """
        input = self.tokenizer.encode_plus(text,
                                           add_special_tokens=True,
                                           return_attention_mask=True,
                                           truncation=True,
                                           padding=True,
                                           max_length=512,
                                           return_tensors='pt')
        output = self.model(**input)
        logits = output.logits
        soft = torch.nn.Softmax(dim=0)
        soft_tensor = soft(logits[0])
        probs = soft_tensor.detach().numpy()
        #print(probs)
        probabilities = {}

        for k, v in self.model_label_dict.items():
            probabilities[k] = v
            probabilities[k]["probability"] = probs[v["index"]]

        return probabilities


if __name__ == '__main__':

    with open("all_models_dict.json") as jsonFile:
        amd = json.load(jsonFile)
        jsonFile.close()
    text = "Comprehensive care of lower urinary tract infections"
    m = BertClassifier(amd["Modell 3: SIWF"]["name"], amd["Modell 3: SIWF"]["base_bert_name"], amd["Modell 3: SIWF"]["train_snapshot_url"],
                       amd["Modell 3: SIWF"]["label_dict_url"])
    preds = m.get_prediction(text)
    print(preds)
