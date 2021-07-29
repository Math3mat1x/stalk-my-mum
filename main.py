import os
from pyicloud import PyiCloudService
from findmyfriends import FindFriendsService
from credentials import username, password
from infos import Coordinates

cookie_directory = os.path.join(os.getcwd(), "cookies")
iphone_api = PyiCloudService(username, password, cookie_directory=cookie_directory)

if iphone_api.requires_2fa:
    code = input("Code 2FA: ")
    iphone_api.validate_2fa_code(code)

fmf_api = FindFriendsService(iphone_api._get_webservice_url("fmf"), iphone_api.session, iphone_api.params)
fmf_api.refresh_client()

following = {friend["invitationAcceptedByEmail"]:friend["id"] for friend in fmf_api.following}

# Using defaults here.

from strategy import Default
from alert import alert

# Test
friend = list(following.keys())[0]
friend_id = following[friend]

check = Default(iphone_api, fmf_api, friend_id)

while True:
    if check.alert():
        alert(friend)
