# Danesh Boom Backend

## Install requirements
```
$ pip install -r requirements.txt
```

## Change configs
change configs in `config.yml` file.
```
cp default-config.yml config.yml
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