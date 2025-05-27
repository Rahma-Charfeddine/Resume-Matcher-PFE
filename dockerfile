FROM python:3.11.0-slim
WORKDIR /data/Resume-Matcher
RUN apt-get update
RUN apt-get install -y build-essential python-dev git
RUN pip install -U pip setuptools wheel
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.7.1/en_core_web_trf-3.7.1-py3-none-any.whl
RUN python -m spacy download en_core_web_md
COPY . .
EXPOSE 8501
RUN python run_first.py
ENTRYPOINT [ "streamlit", "run", "streamlit_app.py"]