FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip -m spacy download fr_core_news_sm
COPY ./app /code/app
CMD ["python", "./main.py"]
