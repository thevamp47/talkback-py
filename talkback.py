import requests
from argparse import ArgumentParser
from colorama import Fore, Style, init
import pandas as pd
from pathlib import Path

info = Fore.YELLOW + Style.BRIGHT
success = Fore.GREEN + Style.BRIGHT
error = Fore.RED + Style.BRIGHT

# API Key here
token = "API-KEY"
url = 'https://talkback.sh/api/v1/'

header = {
    "Authorization": f'JWT {token}',
    "Content-Type": "application/json"
}

# overwrite variable
ovw = False

def savetofile(d_list, filename):

    if Path(filename).is_file() == False or ovw == True:
        table_headers = [
            'Date',
            'Title',
            'URL',
            'Rank'
        ]
        df = pd.DataFrame(d_list, columns=table_headers)
        df.to_excel(filename, index=False)
        print(f'{success}[+][+] Data has been saved in {filename}')
    else:
        print(f'{error}[-] Filename already exists!, use -ovw to overwrite')


def verify_func():

    payload = {
        "query":"query{me{email}}"
    }
    
    resp = requests.post(url, headers=header, json=payload).json()
    try:    
        print(f'{success}[+][+] The token for the user {resp['data']['me']['email']} is valid')
    except:
        for resp_error in resp['errors']:
            print(f'{error}[-] Message: {resp_error["message"]}\n[-] Location: {resp_error["locations"]}')
    

def refresh_token():

    payload = {
        "query": 'mutation{refreshToken(token:"'+ token +'"){token}}'
    }

    resp = requests.post(url, headers=header, json=payload).json()
    print(f'{success}[+][+] The new token is {resp['data']['refreshToken']['token']}')


def search_func(query, filename):

    data_list = []

    payload = {
        "query": 'query{resources('+ query +'){edges{node{createdDate,title,url,rank}cursor}pageInfo{endCursor,hasNextPage}}}'
    }

    print(f'{info}[+] Searching for "{query}" in https://talkback.sh')

    resp = requests.post(url, headers=header, json=payload).json()

    for edge in resp['data']['resources']['edges']:
        #print(f"{info}{edge['node']['title']}")
        #print(edge['node']['url'])
        #print('-'*100)
        data_list.append([edge['node']['createdDate'], edge['node']['title'], edge['node']['url'], edge['node']['rank']])

    if resp['data']['resources']['pageInfo']['hasNextPage'] == True:
        print(f'{info}[+] EndCursor: {resp['data']['resources']['pageInfo']['endCursor']}, use --after {resp['data']['resources']['pageInfo']['endCursor']} to see next page, or change the value of NoR with -nor')

    savetofile(data_list, filename)


def main():
    init(autoreset=True)

    print(fr'''{Fore.LIGHTBLUE_EX + Style.BRIGHT}
___________      .__   __   __________                __                  
\__    ___/____  |  | |  | _\______   \_____    ____ |  | ________ ___.__.
  |    |  \__  \ |  | |  |/ /|    |  _/\__  \ _/ ___\|  |/ /\____ <   |  |
  |    |   / __ \|  |_|    < |    |   \ / __ \\  \___|    < |  |_> >___  |
  |____|  (____  /____/__|_ \|______  /(____  /\___  >__|_ \|   __// ____|
               \/          \/       \/      \/     \/     \/|__|   \/     

Version 1.0''')

    global ovw

    parser = ArgumentParser(description='A python script to search https://talkback.sh/ using its API')
    
    subparsers = parser.add_subparsers(title="Subcommands", help="Subcommand Help", dest='subcommand')

    # Verify Tokens
    verify_sub = subparsers.add_parser('verify', help="Check if your token is valid")

    # Refresh Tokens
    refresh_sub = subparsers.add_parser('refresh', help="Renew a token before it expires, but for no more than 7 days")

    # Search
    search_sub = subparsers.add_parser('query', help="Query https://talkback.sh/")
    search_sub.add_argument('-s', '--search', help="What to search for", type=str)
    search_sub.add_argument('-nor', help="Number of results, default=50", default='50', type=str)
    search_sub.add_argument('-da', '--dateafter', type=str, help="Format: YYYY-MM-DD")
    search_sub.add_argument('-db', '--datebefore', type=str, help="Format: YYYY-MM-DD")
    search_sub.add_argument('--orderby', choices=('date', '-date'), type=str)
    search_sub.add_argument('--after', help="Value of endCursor, this value us used to get the next page of results", type=str)
    search_sub.add_argument('--type', help="Type of post", type=str)
    search_sub.add_argument('--url', help="Post from a specific URL", type=str)
    search_sub.add_argument('--tag', help="Tag of post like mal, net", type=str)
    search_sub.add_argument('-o', '--output', help="Filename to save the result", type=str, required=True)
    search_sub.add_argument('-ovw', help="Overwrite file", action='store_true')


    args = parser.parse_args()

    if args.subcommand == 'verify':
        verify_func()
    elif args.subcommand == 'refresh':
        refresh_token()
    elif args.subcommand == 'query':
        search = args.search
        nor = args.nor
        dateafter = args.dateafter
        datebefore = args.datebefore
        orderby = args.orderby
        after = args.after
        typef = args.type
        urlf = args.url
        tag = args.tag
        output = args.output
        if args.ovw:
            ovw = True

        # Building the Query
        query_builder = f'first:{nor}'

        if search is not None:
            query_builder += f', q:"{search}"'
        if dateafter is not None:
            query_builder += f', createdDateAfter:"{dateafter}"'
        if datebefore is not None:
            query_builder += f', createdDateBefore:"{datebefore}"'
        if orderby is not None:
            query_builder += f', orderBy:"{orderby}"'
        if after is not None:
            query_builder += f', after:"{after}"'
        if typef is not None:
            query_builder += f', type:"{typef}"'
        if urlf is not None:
            query_builder += f', url:"{urlf}"'
        if tag is not None:
            query_builder += f', tag:"{tag}"'

        ult_query = f'q:"{search}", first:{nor}, createdDateAfter:{dateafter}, createdDateBefore:{datebefore}, orderBy:{orderby}, after:{after}, type:{typef}, url:{urlf}, tag:{tag}'

        search_func(query_builder, output)




if __name__ == "__main__":
    main()
