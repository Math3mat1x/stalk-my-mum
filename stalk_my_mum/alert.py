class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

async def alert(friend):
    """
    Alert the user using a service of you choice. 
    This has to be filled manually.

    Input:
        friend (str) : the email or phone_number of the friend near you.
    """

    # Example
    print(bcolors.WARNING + "{} is near you.".format(friend) + bcolors.ENDC)
