# Danesh Boom Backend

## Install required packages
```
$ sudo apt install libpq-dev
```

## Install requirements
```
$ pip install -r requirements.txt
```

## Change configs
change configs in `config.yml` file.
```
cp default-config.yml config.yml
```

## create DB using docker
```bash
docker run --name danesh-boom-postgres -e POSTGRES_PASSWORD=123 -e POSTGRES_DB='danesh-boom' -d -p=5432:5432 postgres:9
```

## Init DB
```
python manage.py migrate
```


## Run project
```
python manage.py runserver
```

## Generate graphql schema
```
python manage.py graphql_schema --indent 2
```
