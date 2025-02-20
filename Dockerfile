FROM python:3.10.0
WORKDIR /app
COPY ./ /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["chatbot.py"]
