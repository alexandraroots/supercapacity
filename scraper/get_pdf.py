from pathlib import Path
import requests
import pandas as pd
from tqdm import tqdm


def get_pdf_from_url(url, filename):
    filepath = Path('data/pdf/' + filename)
    response = requests.get(url)
    filepath.write_bytes(response.content)


if __name__ == "__main__":
    df = pd.read_csv('data/article_with_url.csv')
    for i in tqdm(range(df.shape[0])):
        url = df.iloc[i].url
        filename = str(i + 1) + '.pdf'
        get_pdf_from_url(url, filename)