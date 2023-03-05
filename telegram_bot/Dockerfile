FROM python:3.10
WORKDIR /code
COPY ./requirement.txt /code/requirement.txt
COPY bot.session /code/bot.session
RUN pip install --no-cache-dir --upgrade -r /code/requirement.txt
COPY ./main.py /code/main.py
CMD ["python", "main.py"]
