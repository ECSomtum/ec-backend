# ec-backend

This project was generated via [manage-fastapi](https://ycd.github.io/manage-fastapi/)! :tada:

## Project setup for local development
- Setup virtual environment
```bash
python3 -m venv /path/to/new/virtual/environment
```

- Activate the virtual enviroment
```bash
source env/bin/activate
```

- Install requirement
```bash
pip install -r requirements.txt
```

- Create your own MySQL database
    - Use `backup.sql` for importing schema and data.

- Setup environment file (.env) like below
```bash
PROJECT_NAME=
BACKEND_CORS_ORIGINS=[] #list of url allowed
DATABASE_URI=mysql://user:password@localhost/dbname # replace them with your user
API_KEY= #request personally for this key
GOV_ENDPOINT= #also this one
```

- Run the project (at root)
```
uvicorn app.main:app --reload
```

## License

This project is licensed under the terms of the MIT license.
