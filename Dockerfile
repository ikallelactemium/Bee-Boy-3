FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip 
RUN pip3 install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["chatbot.py"