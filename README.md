
```
docker run -e FLASK_APP=app.py \
  -e MYSQL_HOST=localhost \
  -e MYSQL_USER=test \
  -e MYSQL_PASSWORD=testpassword \
  -p 8080:8080 \
  imagename flask run -h 0.0.0.0 -p 8080
```
