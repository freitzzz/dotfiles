import os

# Local user folder path
__user_home_path__ = os.path.expanduser('~')

# Location of user session environment configuration file (i.e., ~/.profile)
user_session_environment_path = f'{__user_home_path__}/.profile'

# Default directory where dotfiles configuration files live
configuration_directory_path = os.path.expanduser(f'{__user_home_path__}/.dotfiles')

# Location of barrel file that sources all dotfiles configuration files
dotfiles_init_path = f'{configuration_directory_path}/init'

# Location of file that exports PATH variables
exported_paths_path = f'{configuration_directory_path}/paths'

# Location of directory that lists installed modules
installed_modules_path = f'{configuration_directory_path}/installed'
