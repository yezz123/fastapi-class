## Development 🚧

You should create a virtual environment and activate it:

```bash
python -m venv venv/
```

```bash
source venv/bin/activate
```

And then install the development dependencies:

```bash
pip install -r requirements.dev.txt
```

### Testing 🔬

We Provide `pytest` for testing the Code, just run:

```shell
pytest --cov=fastapi_class/
```

### Format the code 💅

Execute the following command to apply `pre-commit` formatting:

```bash
make lint
```