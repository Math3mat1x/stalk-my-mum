import os
from pyicloud import PyiCloudService
from .findmyfriends import FindFriendsService
from .infos import iPhone
from settings import username, password, lookup_dict

def init():
    """
    Initialize and provide basic data.

    Returns:
        - iphone_api: PyiCloud object
        - fmf_api: Find My Friend object
        - following (dict): Apple Find My friend who have shared their location with you.
    """

    # Create a cookie directory in which the PyiCloud session is stored
    cookie_directory = os.path.join(os.getcwd(), "cookies")
    iphone_api = PyiCloudService(username, password, cookie_directory=cookie_directory)
    
    if iphone_api.requires_2fa:
        code = input("2FA Code: ")
        iphone_api.validate_2fa_code(code)
    
    # Create Find My Friend object
    fmf_api = FindFriendsService(iphone_api._get_webservice_url("fmf"), iphone_api.session, iphone_api.params)

    return iphone_api, fmf_api, \
            {friend["invitationAcceptedByEmail"]:friend["id"] for friend in fmf_api.following}

iphone_api, fmf_api, following = init()

# Using defaults here.
iphone = iPhone(iphone_api)
from .strategy import DefaultStrategy
