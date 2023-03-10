## setup

install dependancies
```bash
python3 -m pip install -r requirements.txt
```

### Database

set the database uri in `instance/config.toml`

initialize the database
```bash
flask db init
```

generate initilal migration
```bash
flask db migrate -m "Initial migration."
```

apply changes
```bash
flask db upgrade
```

[flask migrate docs]("https://flask-migrate.readthedocs.io/en/latest/")
