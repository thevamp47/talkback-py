# TalkBackpy

![A fancy AI Image](assets/image.jpg)

A python script that uses TalkBack API to query the website and save the results in Excel file.

## Table of Contents

- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

- Create an account on [talkback.sh](https://talkback.sh/)
- Go to the profile section to get the API Token
- Add the value to the token varaible in the code 

### Git Clone

Git clone & install requirements

```bash
$ git clone https://github.com/thevamp47/talkback-py.git
$ cd talkback-py
$ pip install -r requirements.txt
$ python3 talkback.py -h
```
## How to Use

### Verify Token

Use this command to verify if the token is valid

```bash
$ python3 talkback.py verify
```
### Refresh Token

Use this command to get a new token if the previous one has expired, add the value to the token varaible in the code 

```bash
$ python3 talkback.py refresh
```

### Query

#### Help

Running query with help option

```bash
$ python3 talkback.py query -h
```
- ```-s, --search```: What to search for 
- ```-nor```: Set the number of results returned
- ```-da, --dateafter```: Set the date after 
- ```-db, --datebefore```: Set the date before
- ```--orderby```: 2 options(date, -date)
- ```--after```: Value of endCursor, this value us used to get the next page of results
- ```--type```: the Type of post
- ```--url```: Post from a specific URL
- ```--tag```: Tags like mal, net
- ``-o``: Filename to save the result
- ``-ovw``: Overwrite file

#### Usage Example

To search for posts with the title MoveIT and save the result in moveit.xlsx

```bash
$ python3 talkback.py query -s "title:MoveIT" -o moveit.xlsx
```
To search the next page of the results

```bash
$ python3 talkback.py query -s "title:MoveIT" -o moveit_2.xlsx --after YXJyYXljb25uZWN0aW9uOjQ5
```

To search post from a specific url
```bash
$ python3 talkback.py query --url "elttam.com" -o url_elttam.xlsx
```

## License

This project is licensed under the [GPL License](LICENSE) - see the [LICENSE](LICENSE) file for details.
