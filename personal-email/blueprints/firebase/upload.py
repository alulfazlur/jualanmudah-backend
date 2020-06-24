from blueprints import app
import pyrebase


# import configuration from config.py 
config = app.config['FIREBASECONFIG']

# initiate configuration for firebase storage
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

class UploadToFirebase : 
    def __init__(self) :
        pass
    
    # upload image recieve two parameters, first is imagefile, then is folder name inside images folder without /
    def UploadImage(self, image, folder) :

        try:
            file = image
            filename = file.filename
            folder_name = 'images/'+folder+'/'

            cloud_path = folder_name + filename

            do_upload = storage.child(cloud_path).put(file)

            link = storage.child(cloud_path).get_url(do_upload["downloadTokens"])

            # if not eror when sending image it will return link of image uploaded
            return link

        except Exception as error:
            
            link = storage.child('images/error/default_picture.png').get_url('42cff136-91ec-4d47-8abc-a609e5e6808d')
            print('warning !!!! Something error !!!!')
            print(error)

            # if eror it will return link of default image inside folder images/error/
            return link