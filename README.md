# Environments
- python 3.7
- Flask
- sqlite3

# Getting Started
## Run on Local
### Install requirements
```
$ pip install -r requirements.txt
```
### Running
```
$ cd search_company
$ python manage.py run
```
## Run with Docker
### Build Docker Image
```
$ cd build_script
$ ./docker_command.sh build `<tag_name>`
```
### Run Docker
```
$ cd build_script
$ ./docker_command.sh run `<tag_name>`
```
# APIs
[API Specification Document.](https://github.com/hyerim-kim/search_company/blob/master/app/docs/api_specification.md)