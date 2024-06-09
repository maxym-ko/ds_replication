## Run instructions

### Setting up "Primary-Replica" replication
#### Step 1: Run Docker containers with Primary and Replica instances
```shell
chmod +x replica-entrypoint.sh
docker-compose up -d postgres_primary postgres_replica
watch -n1 "docker-compose ps"
```

#### Step 2: Connect to Primary instance and insert some data
```shell
psql postgres://user:password@localhost:5432/postgres <<EOF

CREATE TABLE cars (
  brand VARCHAR(255),
  model VARCHAR(255),
  year INT
);
  
INSERT INTO cars (brand, model, year)
VALUES ('Ford', 'Mustang', 1964);
EOF
```

#### Step 3: Connect to Replica instance and verify inserted data
```shell
psql postgres://user:password@localhost:5433/postgres -c \
"SELECT * FROM cars;"
```

#### Step 4: Stop Replica instance and add insert more data to Primary instance 
```shell
docker-compose stop postgres_replica
```

```shell
psql postgres://user:password@localhost:5432/postgres -c \
"INSERT INTO cars (brand, model, year) VALUES ('Volvo', 'p1800', 1968);"
```

#### Step 5: Start Replica instance and verify inserted data
```shell
docker-compose start postgres_replica
watch -n1 "docker-compose ps"
```
```shell
psql postgres://user:password@localhost:5433/postgres -c \
"SELECT * FROM cars;" 
```

#### Step 6: Kill Docker containers
```shell
docker-compose down -v
```

## References
- https://medium.com/@eremeykin/how-to-setup-single-primary-postgresql-replication-with-docker-compose-98c48f233bbf