# Flask blog app

[app is deployed here](https://blogapp-0z78.onrender.com)

## about
This app is a blogging app that allows you to use github flavoured markdown 
to edit your blog, it features an online editor with live preview, syntax highlighting for your code blocks and table of contents just by adding `[TOC]` anywhere in your file.

To create a post first sign in and click New Post on the navigation bar


### schema
The project has 3 tables

```python3
class User:
    id: Integer
    username: String
    password: String
    posts: Relationship<Post>
    drafts: Relationship<Draft>

class Post:
    id: Integer
    title: Text
    body: Text
    created: DateTime
    modified: DateTime
    author: Relationship<User>
    author_id: ForeignKey<User.id>

class Draft:
    id: Integer
    title: Text
    body: Text
    author_id: ForeignKey<User.id>
    author: Relationship<User>
```

all relationships are one to many as the two latter tables depend on users

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

## running the app locally

creating a virtual environment is recomended

run the app
```bash
flask run
```

