import os
from pyicloud import PyiCloudService
from .findmyfriends import FindFriendsService
from credentials import username, password

def init():
    cookie_directory = os.path.join(os.getcwd(), "cookies")
    iphone_api = PyiCloudService(username, password, cookie_directory=cookie_directory)
    
    if iphone_api.requires_2fa:
        code = input("2FA Code: ")
        iphone_api.validate_2fa_code(code)
    
    fmf_api = FindFriendsService(iphone_api._get_webservice_url("fmf"), iphone_api.session, iphone_api.params)
    fmf_api.refresh_client()

    return iphone_api, fmf_api, \
            {friend["invitationAcceptedByEmail"]:friend["id"] for friend in fmf_api.following}

iphone_api, fmf_api, following = init()

# Using defaults here.
from .strategy import DefaultStrategy
from .alert import alert
