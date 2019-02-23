FROM continuumio/anaconda3:4.4.0
MAINTAINER UNP, https://unp.education
COPY ./flask_demo /usr/local/python/
WORKDIR /usr/local/python/
RUN pip install -r requirements.txt
CMD python flask_predict_api.py
ENV AWS_ACCESS_KEY=AKIAIFV2JCUD63OVL43Q
ENV AWS_SECRET_KEY=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
EXPOSE 8080