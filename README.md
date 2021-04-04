# Coffee Shop API 

This is a practice API made using flask, feel free to make any modifications to it.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install flask_sqlalchemy.

```bash
pip install flask_sqlalchemy
```

## Usage

```python
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
```


### GET GET/all
This endpoint returns all the records of the cafes in the database
```bash
http://127.0.0.1:5000/all
```

### GET GET/random
This endpoint returns a random record from the cafe database
```bash
http://127.0.0.1:5000/random
```

### GET GET /search
This endpoint returns a random record from the cafe database
```bash
http://127.0.0.1:5000/search?loc=Shoreditch
```

### POST POST /add
add new cafe to the database
```bash
http://127.0.0.1:5000/add
```

### PATCH PATCH /update_price/<id>
Make things easier for your teammates with a complete request description.
```bash 
http://127.0.0.1:5000/update_price/1
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)