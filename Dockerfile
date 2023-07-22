FROM python:3.11.3
RUN mkdir -p /usr/src/react_bot
WORKDIR /usr/src/react_bot
COPY . /usr/src/react_bot
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "bot.py"]