MySQL group replication is a new feature and we need cluster health metrics, while standard mysqld_exporter covers most of the use case.

If you want to run in docker, invoke like this.

```
docker run \
  -e MYSQL_HOST=dbhost \
  -e MYSQL_USER=test \
  -e MYSQL_PASSWORD=testpassword \
  -p 5000:5000 \
  hkwi/mysqld_gr_exporter
```

Environment variables
------
- MYSQL_HOST : remote mysql host
- MYSQL_USER : user having SELECT privilage on performance_schma.replication_group_members
- MYSQL_PASSWORD : password for that user


Metrics
------
`replication_group_members` will be exported with member states and roles in metric labels.
This is suitable for table format, which was [added in grafana 4.3](http://docs.grafana.org/guides/whats-new-in-v4-3/#prometheus-table-data-column-per-label).
Value for `replication_group_members` is row count for now.

We use integer index for role and state value in label value.

| role value | metric label value |
| :--: | :--: |
| PRIMARY | 1 |
| SECONDARY | 2 |

| state value | metric label value |
| :--: | :--: |
| ONLINE | 0 |
| OFFLINE | 1 |
| RECOVERING | 2 |
| ERROR | 3 |
| UNREACHABLE | 4 |

Example

```
replication_group_members{nodeA_role="1",nodeB_role="2",nodeC_role="2",nodeA_state="0",nodeB_state="0",nodeC_state="0"} 3
```
