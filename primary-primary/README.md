## Run instructions

### Setting up "Multi-Master" replication
#### Step 1: Run Docker containers with Node1 and Node2
```shell
docker-compose up -d postgres_node1 postgres_node2
watch -n1 "docker-compose ps"
```

#### Step 2: Connect to Node1 instance and insert some data
```shell
psql postgres://user:password@localhost:5432/postgres <<EOF

CREATE SEQUENCE cars_id_seq
    START 1
    INCREMENT 2;

CREATE TABLE cars (
    id INT NOT NULL DEFAULT nextval('cars_id_seq') PRIMARY KEY,
    brand VARCHAR(255),
    model VARCHAR(255),
    year INT
);
  
INSERT INTO cars (brand, model, year)
VALUES ('Ford', 'Mustang', 1964);
EOF
```

#### Step 3: Connect to Node2 instance and insert some data
```shell
psql postgres://user:password@localhost:5433/postgres <<EOF

CREATE SEQUENCE cars_id_seq
    START 2
    INCREMENT 2;

CREATE TABLE cars (
    id INT NOT NULL DEFAULT nextval('cars_id_seq') PRIMARY KEY,
    brand VARCHAR(255),
    model VARCHAR(255),
    year INT
);
EOF
```

#### Step 4: Create replication user and publication for both instances
```shell
psql postgres://user:password@localhost:5432/postgres <<EOF

CREATE ROLE repuser WITH REPLICATION LOGIN PASSWORD 'welcome1';
GRANT all ON all tables IN schema public TO repuser;

CREATE PUBLICATION carpub1 FOR TABLE cars;
EOF
```
```shell
psql postgres://user:password@localhost:5433/postgres  <<EOF 

CREATE ROLE repuser WITH REPLICATION LOGIN PASSWORD 'welcome1';
GRANT all ON all tables IN schema public TO repuser;

CREATE PUBLICATION carpub2 FOR TABLE cars;
EOF
```

#### Step 5: Create subscription for created publications
```shell
psql postgres://user:password@localhost:5432/postgres <<EOF

CREATE SUBSCRIPTION carsub1
    CONNECTION 'host=postgres_node2 port=5432 user=repuser password=welcome1 dbname=postgres'
    PUBLICATION carpub2
    WITH (origin = none, copy_data = false);
EOF
```
```shell
psql postgres://user:password@localhost:5433/postgres <<EOF

CREATE SUBSCRIPTION carsub2
    CONNECTION 'host=postgres_node1 port=5432 user=repuser password=welcome1 dbname=postgres'
    PUBLICATION carpub1
    WITH (origin = none, copy_data = true);
EOF
```

#### Step 6: Connect to Node2 instance and verify inserted data
```shell
psql postgres://user:password@localhost:5433/postgres -c \
"SELECT * FROM cars;"
```

#### Step 7: Stop Node2 instance and add insert more data to Node1 instance 
```shell
docker-compose stop postgres_node2
```

```shell
psql postgres://user:password@localhost:5432/postgres -c \
"INSERT INTO cars (brand, model, year) VALUES ('Volvo', 'p1800', 1968);"
```

#### Step 8: Start Node2 instance and verify inserted data
```shell
docker-compose start postgres_node2
watch -n1 "docker-compose ps"
```
```shell
psql postgres://user:password@localhost:5433/postgres -c \
"SELECT * FROM cars;" 
```

#### Step 9: Kill Docker containers
```shell
docker-compose down -v
```

## References
- https://www.crunchydata.com/blog/active-active-postgres-16#publication