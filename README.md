# fastapi asgi setup

## pre-requisite
pyenv - install multiple python version and virtual environments

[How to Setup](https://www.freecodecamp.org/news/manage-multiple-python-versions-and-virtual-environments-venv-pyenv-pyvenv-a29fb00c296f/)

python verson:  3.11.x

[Poetry](https://python-poetry.org/docs) - python advanced package management system.

why you should use : [read here](https://community.sap.com/t5/application-development-blog-posts/why-you-should-use-poetry-instead-of-pip-or-conda-for-python-projects/ba-p/13545646)

[How to install](https://python-poetry.org/docs/#installing-with-the-official-installer)

## run with uvicorn

`poetry run uvicorn src.main:app --reload`

## run with gunicorn

`gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py src.main:app`

## debug

Ensure you call the command to move the virtual env that poetry create within your workspace in vscode, and then check
the launch.json for path.

`poetry config virtualenvs.in-project true`

## Test
set the testdb and modify the conftest.py to use that.

`pytest "path/to/tests"`
