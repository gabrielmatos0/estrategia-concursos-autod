from os import getenv, path, mkdir


def get_chrome_profile_path(profile_name=''):
    win_username = getenv('USERNAME')
    profile_path = fr'C:\Users\{win_username}\AppData\Local\Google\Chrome\User Data\{profile_name}'

    if not path.exists(profile_path):
        mkdir(profile_path)

    return profile_path


if __name__ == '__main__':
    print(get_chrome_profile_path('WebAutomation'))
