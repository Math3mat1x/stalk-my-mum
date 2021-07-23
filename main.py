import os
from pyicloud import PyiCloudService
from findmyfriends import FindFriendsService
from credentials import username, password

cookie_directory = os.path.join(os.getcwd(), "cookies")
api = PyiCloudService(username, password, cookie_directory=cookie_directory)

if api.requires_2fa:
    code = input("Code 2FA: ")
    api.validate_2fa_code(code)

friends = FindFriendsService(api._get_webservice_url("fmf"), api.session, api.params)
print(friends.following)
