FROM python
RUN pip install flask pymysql
COPY app.py app.py
