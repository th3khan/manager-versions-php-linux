import os
import decimal
from getpass import getuser
from colorama import Fore, Style

LAST_VERSION = 8.1
DISTRO_OPTIONS = {
    'debian': 1,
    'ubuntu': 2
}

def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start += decimal.Decimal(step)

def print_message(text, type):
    if type == 'success':
        print(Style.BRIGHT + Fore.GREEN + text + Style.RESET_ALL)
    elif type == 'error':
        print(Style.BRIGHT + Fore.RED + text + Style.RESET_ALL)
    else:
        print(text)
    

def clear_console():
    command = 'clear'
    os.system(command)

def get_path_file_version():
    user = getuser()
    path_home = '/home/'
    file_name = 'php_versions.txt'
    if os.path.exists(f'{path_home}/{user}'):
        file = f'{path_home}/{user}/{file_name}'
    else:
        file = f'{path_home}/{file_name}'
    return file

def save_versions_in_file(text):
    file_path = get_path_file_version()
    file = open(file_path, "w")
    file.write(text)
    file.close()
    

def sync_versions():
    php_main = 'php'
    from_version = 5
    to_version = LAST_VERSION
    folder_bin = '/usr/bin/'
    main_php_path = f'{folder_bin}{php_main}'
    versions_text = None
    if os.path.exists(main_php_path):
        range_versions = list(float_range(from_version, to_version + 0.1, 0.1))
        print(range_versions)
        for version in range_versions:
            php_version = f'{php_main}{version}'
            print(php_version)
            if os.path.exists(f'{folder_bin}{php_version}'):
                if versions_text is None:
                    versions_text = str(php_version)
                else:
                    versions_text += str(php_version)
                versions_text += '\n'
        save_versions_in_file(versions_text)
        clear_console()
        print_message("*** Sync Successful ***", "success")
        print_message("*** Your list new is ***", "success")
        show_list_versions(False)
    else:
        clear_console()
        print_message("*** You haven't installed any PHP version in your system ***", "error")

def update_repo_php_debian():
    if os.path.exists('/etc/apt/sources.list.d/php-change-verions-script.list') is False:
        os.system('sudo apt update')
        os.system('sudo apt install software-properties-common ca-certificates lsb-release apt-transport-https')
        os.system('sudo sh -c \'echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php-change-verions-script.list\'')
        os.system('wget -qO - https://packages.sury.org/php/apt.gpg | sudo apt-key add - ')
        os.system('sudo apt update ')

def update_repo_php_ubuntu():
    os.system('sudo apt update')
    os.system('sudo add-apt-repository ppa:ondrej/php')
    os.system('sudo apt update')

def install_version():
    version = None
    distro = None
    while distro is None:
        try:
            distro = int(input(f'Enter your Distro\n1) Debian\n2) Ubuntu\n-> : '))
        except ValueError:
            distro = None
            clear_console()
            print_message("***Invalid Option! Try again***", 'error')
    while version is None:
        try:
            version = float(input(f'Enter the version ({LAST_VERSION}): ' or LAST_VERSION))
        except ValueError:
            version = None
            clear_console()
            print_message("***Invalid Option! Try again***", 'error')
    if distro == DISTRO_OPTIONS['debian']:
        update_repo_php_debian()
    elif distro == DISTRO_OPTIONS['ubuntu']:
        update_repo_php_ubuntu()
    os.system(f'sudo apt install php{version} php{version}-zip php{version}-xmlrpc php{version}-xml php{version}-readline php{version}-opcache php{version}-mysql php{version}-mbstring php{version}-json php{version}-intl php{version}-gd php{version}-fpm php{version}-curl php{version}-common php{version}-cli php{version}-bcmath')
    print_message('*** Finished ***', 'success')

def get_all_versions(path_file, in_list = False):
    file = open(path_file)
    if in_list:
        versions = file.readlines()
    else:
        versions = file.read()
    file.close()
    return versions

def show_list_versions(clear = True):
    path_file  = get_path_file_version()
    if (os.path.exists(path_file)):
        versions = get_all_versions(path_file)
        if clear: clear_console()
        print_message(versions, 'success')
        input('Press enter to continue!')
        clear_console()
        return
    print_message('*** You need to sync php version information on your system ***', 'error')
    return

def change_version():
    path_file  = get_path_file_version()
    if (os.path.exists(path_file)):
        versions = get_all_versions(path_file, True)
        if len(versions) > 0:
            clear_console()
            i = 0
            list_versions = []
            for version in versions:
                i += 1
                text = f'{i}-) {version.rstrip()}'
                print_message(text, 'success')
                list_versions.append(version.rstrip())
            text = f'{i+1}-) <- Back'
            print_message(text, 'success')
            while True:
                try:
                    op = int(input(f'Choose an option ({i}): ') or i)
                    if op == i+1:
                        break
                    version_selected = list_versions[op - 1]
                    os.system(f'sudo update-alternatives --set php /usr/bin/{version_selected}')
                    clear_console()
                    print_message(f"*** Updated to php version {version_selected} successful **", "success")
                    break
                except ValueError:
                    print_message("***Invalid Option! Try again***", "error")
            return
    print_message('*** You need to sync php version information on your system ***', 'error')
    return


def bye_bye():
    print_message('*** Until next time ***', 'success')
    print_message('*** Goodbye! ***', 'success')
    exit()

def show_main_menu():
    if os.path.exists('/usr/bin/php'):
        text_verison = os.popen('php --version').read()
        print_message('Your current php version is: ', 'success')
        print_message(text_verison, 'success')
    text = '''
    Hi, What would you like to do:
    1) Sync list PHP verisons
    2) Show list PHP verisons 
    3) Install PHP verison
    4) Change PHP version current
    5) Exit
    '''
    try:
        op = int(input(text))
    except ValueError:
        clear_console()
        print_message("***Invalid Option! Try again***", "error")
        op = show_main_menu()
    return op

def run():
    clear_console()
    while True:
        op = show_main_menu()
        if op == 1:
            sync_versions()
        elif op == 2:
            show_list_versions()
        elif op == 3:
            install_version()
        elif op == 4:
            change_version()
        elif op == 5:
            bye_bye()
        continue


if __name__ == '__main__':
    run()