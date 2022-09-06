import pandas as pd


def save_to_csv(result):
    df = pd.DataFrame(result, columns=['doi', 'url', 'name', 'description'])
    df.to_csv('data/articles.csv')
