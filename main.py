import requests
import json

import pandas as pd


def download_file(url_file: str, file_name: str) -> None:
    """
    Скачивание через API
    :param url_file:
    :param file_name:
    """
    with open(file_name, "wb") as file:
        response = requests.get(url_file)
        file.write(response.content)


def read_xlsx_pos(file_name: str):
    """
    Создание DataFrame
    :param file_name:
    :return:
    """
    with open(file_name, "r") as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    return df[['userId', 'id']].rename(columns={'id': 'postId'})


def read_xlsx_com(file_name: str):
    """
    Создание DataFrame
    :param file_name:
    :return:
    """
    with open(file_name, "r") as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    return df[['postId', 'id']].groupby('postId').count()


if __name__ == '__main__':
    url_post = 'http://jsonplaceholder.typicode.com/posts'
    url_com = 'http://jsonplaceholder.typicode.com/comments'
    name_file_post = 'post.json'
    name_file_com = 'com.json'

    download_file(url_post, name_file_post)
    download_file(url_com, name_file_com)

    pos = (read_xlsx_pos(name_file_post))
    com = (read_xlsx_com(name_file_com))

    new_df = pd.merge(pos, com, on=["postId", "postId"], how="outer")
    agg_func_math = {'postId': ['count'], 'id': ['sum']}
    qw = new_df.groupby('userId').agg(agg_func_math)

    qw['sr'] = qw[('id', 'sum')] / qw[('postId', 'count')]

    print(dict(qw['sr']))
