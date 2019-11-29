# genealogie

Family tree visualization.

## Setup

### Create the database

```
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```

### Prepare your family data

1. Create `arbre/data/persons.csv` with the following fields:
  * `id`
  * `first_name`
  * `middle_name`
  * `last_name`
  * `birth_date`
  * `birth_place`
  * `death_date`
  * `death_place`
  * `gender`
  * `comments`

2. Create `arbre/data/edges.csv`, with the following fields:

  * `child_id`: References a person `id`.
  * `parent_id`: References a person `id`.

### Load data into the database:

```
python3 manage.py load_persons --path=arbre/data/persons.csv --truncate=True
python3 manage.py load_edges --path=arbre/data/edges.csv --truncate=True
```
