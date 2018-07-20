FROM python
RUN pip install flask pymysql
COPY app.py app.py
ENV FLASK_APP=app.py FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["flask", "run"]
