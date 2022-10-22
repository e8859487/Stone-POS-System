
from imgurpython import ImgurClient
import GlobalSettings as GlobalSettings
# client = ImgurClient(client_id, client_secret)

client = ImgurClient(GlobalSettings.client_id, GlobalSettings.client_secret, GlobalSettings.access_token, GlobalSettings.refresh_token)
# Authorization flow, pin example (see docs for other auth types)
# authorization_url = client.get_auth_url('token')
# https://api.imgur.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&response_type=REQUESTED_RESPONSE_TYPE&state=APPLICATION_STATE
# ... redirect user to `authorization_url`, obtain pin (or code or token) ...
# https://imgur.com/#access_token=a007e7a0fe609cce03840bd6e495fe4284af0831&expires_in=315360000&token_type=bearer&
# refresh_token=b3623ec40274fa25597f050b293d9ac96c2d49d7&account_username=e88594877&account_id=45080435

# credentials = client.authorize('PIN OBTAINED FROM AUTHORIZATION', 'pin')
# client.set_user_auth(credentials['access_token'], credentials['refresh_token'])


def getImages():
    imageMapList = []
    for i in range(0, 10):
        images = client.get_account_images("e88594877", i)
        print("page : {}, total photos: image: {}".format(i, len(imageMapList)))

        for image in images:
            imageMapList.append({'name': image.name, 'webContentLink': image.link})
    print("total photos: image: {}".format(len(imageMapList)) )
    import common_tools
    common_tools.saveToPickle(imageMapList)


def getAlbum():
    # Example request
    for album in client.get_account_albums('me'):
        album_title = album.title if album.title else 'Untitled'
        print('Album: {0} ({1})'.format(album_title, album.id))

        for image in client.get_album_images(album.id):
            image_title = image.title if image.title else 'Untitled'
            print('\t{0}: {1}'.format(image_title, image.link))

    # Save some API credits by not getting all albums
        break

getImages()