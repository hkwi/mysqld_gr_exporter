
```
docker run \
  -e MYSQL_HOST=dbhost \
  -e MYSQL_USER=test \
  -e MYSQL_PASSWORD=testpassword \
  -p 5000:5000 \
  hkwi/mysqld_gr_exporter
```
