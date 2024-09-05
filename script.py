import praw
import os


def create_auth():
    credentials = {}
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as file:
            print("Reading file.....")
            credentials['client-id'] = file.readline().split('\n')[0]
            credentials['client_secret'] = file.readline().split('\n')[0]
            credentials['user_agent'] = file.readline().split('\n')[0]
            print("Done")
    elif os.path.exists("data.txt") == False:
        credentials['client-id'] = input('client_id:')
        credentials['client_secret'] = input('client_secret:')
        credentials['user_agent'] = input('user_agent:')
        with open("data.txt", "w") as file:
            file.write(credentials['client-id'] + "\n")
            file.write(credentials['client_secret'] + "\n")
            file.write(credentials['user_agent'] + "\n")
    login = True if input('Do you want to login(Y/N)? ').capitalize() == 'Y' else False
    if login == 'Y':
        credentials['username'] = input('username:')
        credentials['password'] = input('password:')
    else:
        credentials['username'] = ""
        credentials['password'] = ""
    
    return (credentials,login)


cred,_ = create_auth()
print(cred)