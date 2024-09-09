import praw
import os
import shutil
from PIL import Image  
import requests

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


if __name__ == '__main__':
    cred,_ = create_auth()
    reddit = praw.Reddit(
        client_id= cred['client-id'],
        client_secret= cred['client_secret'],
        user_agent= cred['user_agent'],
        #A user agent header is a string of text that is sent with HTTP requests to 
        #identify the program making the request (the program is called a "user agent")
    )
    reddit.read_only = True

    post_if_exists = False
    while post_if_exists == False:
        try:
            gallery_url = input("Enter Reddit URL:")
            response = requests.head(gallery_url, allow_redirects=True)
            if response.status_code == 200:
                post = reddit.submission(url = gallery_url)
                post_if_exists = True
            else:
                post_if_exists = False
        except requests.RequestException as e:
            post_if_exists = False


    image_urls = []
    for item in sorted(post.gallery_data['items'], key=lambda x: x['id']):
        media_id = item['media_id']
        meta = post.media_metadata[media_id]
        if meta['e'] == 'Image':
            source = meta['s']
            image_urls.append(source['u'].replace('preview','i'))

    foldername = 'images'
    filename = 'image'
    i = 0
    os.makedirs(foldername,exist_ok=True)
    for link in image_urls:
        res = requests.get(link).content
        # Save the image
        file = os.path.join(foldername, f"{filename}{i}.jpg")
        with open(file, "wb") as f:
            f.write(res)
        i += 1
    print("Done")

    images = [
        Image.open("images/" + f)
        for f in [f"image{x}.jpg" for x in range(i)]
    ]

    pdf_path = f"{post.title}.pdf"
        
    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )
    shutil.rmtree(foldername, ignore_errors=True)
    