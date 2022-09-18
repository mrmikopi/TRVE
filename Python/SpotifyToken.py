import requests as rq
import six
import base64

def main():
    client_id = 'f761219356424233973b191ecfa812a5'
    client_secret = 'ec22780b46c340988ebef5afc3fb8a40'

    authOptions = {

        'url':'https://accounts.spotify.com/api/token',
        'headers': {
            'Authorization':'Basic' + (client_id + ':' + client_secret)
        },
        'form': {
            'grant_type':'client_credentials'
        },
        'json':'true'
    }

    header = base64.b64encode(
        six.text_type(
            client_id + ':' + client_secret)
            .encode('ascii'))
    auth_header = header.decode('ascii')
    payload = {'grant_type': 'client_credentials'}

    x = rq.post('https://accounts.spotify.com/api/token', 
    data=payload,
    headers={'Authorization':"Basic %s" % auth_header},
    verify=True)

    print(x.json())
    return x.json()

if (__name__) == "__main__":
    main()