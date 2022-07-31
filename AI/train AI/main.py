import pandas as pd
from requests import *
from tqdm.notebook import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import re
from collections import Counter
import unicodedata
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
torch.manual_seed(1)
nlp = spacy.load("fr_core_news_sm")

def get_df(req):
    """
    Run an SQL Query on our dataset and return the result in the form of a Python dictionnary.
    """
    conn = psycopg2.connect(
        host="195.154.45.91",
        database="politicometre",
        user="politicometre",
        password="095a520b4023169a50fee97f1c4bb856fbf4e9a8a9ac1247",
        sslmode ='disable')
    c = conn.cursor()
    c.execute(req)
    cols = ([desc[0] for desc in c.description])
    data = {col:[] for col in cols}
    for it in c:
        for i in range(len(it)):
            data[cols[i]].append(it[i])
    return data

def test_df_loading():
    d = get_df("SELECT nom, text, x, y from deputes join texts on texts.deputes_id = deputes.id LIMIT 10")
    df = pd.DataFrame(d)
    print(df)

d = get_df("SELECT nom, text, x, y from deputes join texts on texts.deputes_id = deputes.id LIMIT 10")
df = pd.DataFrame(d)
corpus_a = "fr_dep_news_trf"
corpus_e = "fr_core_news_sm"


def separe_to_sentences(text, efficiency=True):
    corpus = corpus_e if efficiency else corpus_a
    nlp = spacy.load(corpus)
    doc = nlp(text)
    assert doc.has_annotation("SENT_START")
    return [unicodedata.normalize("NFKD", sent.text) for sent in doc.sents]


def process_text(text, efficiency=True):
    text = re.sub(r'\([^)]*\)', '', text)
    corpus = corpus_e if efficiency else corpus_a
    nlp = spacy.load(corpus)
    doc = nlp(text)
    t = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]
    return t


def create_lexic(d2, size=1000):
    df2 = pd.DataFrame(d2)
    df2["cleaned_text"] = df2["text"].apply(process_text)
    df2["n_words"] = df2["cleaned_text"].apply(len)
    df2 = df2[df2.n_words > 1]
    c = dict(Counter(df2["cleaned_text"].sum()))
    so = sorted(c.items(), key=lambda x: x[1], reverse=True)
    d = dict(so[:size])
    return list(d.keys())


def separe_dictionnary_by_sentences(d):
    d2 = {k: [] for k in d.keys()}
    for nom, text, x, y in tqdm(list(zip(d["nom"], d["text"], d["x"], d["y"]))):
        sentences = separe_to_sentences(text, efficiency=True)
        for sentence in sentences:
            if len(sentences) < 15:
                continue
            d2["nom"].append(nom)
            d2["x"].append(x)
            d2["y"].append(y)
            d2["text"].append(sentence)
    return d2

d = get_df("SELECT nom, text, x, y from deputes join texts on texts.deputes_id = deputes.id LIMIT 10")
df = pd.DataFrame(d)
lexic = create_lexic(d, size = 1000)
df["cleaned_text"] = df["text"].apply(process_text)
df["cleaned_text"] = df["cleaned_text"].apply(lambda x:[i for i in x if i in lexic])
df["text"] = df["cleaned_text"].apply(lambda x:" ".join(x))

d = get_df("SELECT nom, text, x, y from deputes join texts on texts.deputes_id = deputes.id LIMIT 100")
df = pd.DataFrame(d)
df["cleaned_text"] = df["text"].apply(process_text)
lexic = create_lexic(d, size = 1000)
df["cleaned_text"] = df["cleaned_text"].apply(lambda x:[i for i in x if i in lexic])
df["text"] = df["cleaned_text"].apply(lambda x:" ".join(x))

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(list(df["text"]))

vectorizer.transform([df["text"][0]])

class TFIDF_NN(nn.Module):

    def __init__(self, vect, hidden_size = 100):
        super(TFIDF_NN, self).__init__()
        self.vectorizer = vect
        vocab_size = vect.get_feature_names_out().shape[0]
        self.linear1 = nn.Linear(vocab_size, hidden_size)
        self.output = nn.Linear(hidden_size, 2)


    def forward(self, text):
        inputs = torch.tensor(self.vectorizer.transform(text).toarray()).float()
        h1 = F.relu(self.linear1(inputs))
        output = self.output(h1)
        return output


model = TFIDF_NN(vectorizer)

loss_fn = torch.nn.MSELoss(reduction='sum')
learning_rate = 1e-2
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for t in range(10000):
    y_pred = model(df["text"])
    y_true = torch.tensor(np.array(df[["x", "y"]])).float()
    loss = loss_fn(y_pred, y_true)
    if t % 250 == 0:
        print(t, loss.item())
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

torch.save(model.state_dict(), 'model_no_embeding.pth')

d = get_df("SELECT nom, text, x, y from deputes join texts on texts.deputes_id = deputes.id LIMIT 50000")
df = pd.DataFrame(d)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(list(df["text"]))
X.shape

model = TFIDF_NN(vectorizer)

loss_fn = torch.nn.MSELoss(reduction='sum')
learning_rate = 1e-2
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for t in tqdm(range(5000)):
    y_pred = model(df["text"])
    y_true = torch.tensor(np.array(df[["x", "y"]])).float()
    loss = loss_fn(y_pred, y_true)
    if t % 200 == 0:
        print(t)
        print("Training: ", loss.item())
        d2 = df.sample(n=100)
        yt = torch.tensor(np.array(d2[["x", "y"]])).float()
        pt = model(d2["text"])
        loss2 = loss_fn(yt, pt)
        print("Test: ", loss2.item())
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

torch.save(model.state_dict(), 'model_embeding.pth')