def read_env(
        env_file_path: str = "ckns.env"
) -> dict:
    """
    Read environment variables from file
    :param env_file_path: path to env file
    :return: dictionary with environment variables as keys and their values as values
    """
    env_vars = {}
    try:
        with open(env_file_path, "r") as file:
            for line in file:
                if not line.strip().startswith("#") and "=" in line:
                    key, value = line.strip().split("=", 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Файл '{env_file_path}' не найден.")
    return env_vars


def write_env(
        env_vars: dict,
        env_file_path: str = "ckns.env"
) -> bool:
    """
    Write environment variables to file
    :param env_vars: dictionary with environment variables as keys and their values as values
    :param env_file_path: path to env file
    :return: True if successful, False otherwise
    """
    success = False
    try:
        with open(env_file_path, "w") as file:
            for key, value in env_vars.items():
                file.write(f"{key}={value}\n")
        success = True
    except Exception as e:
        print(f"Error writing to file: {e}")
    return success


def edit_env(
        env_vars: dict,
        env_file_path: str = "ckns.env"
) -> bool:
    """
    Edit environment variables in file
    :param env_vars: dictionary with environment variables to be updated as keys and their new values as values
    :param env_file_path: path to env file
    :return: True if successful, False otherwise
    """
    existing_env_vars = read_env(env_file_path)
    existing_env_vars.update(env_vars)

    success = write_env(existing_env_vars, env_file_path)
    return success


def check_token_in_env(
        token_name: str,
        env_file_path: str = "ckns.env"
) -> bool:
    """
    Check if token is in env file with given
    :param token_name: token name in env file with given
    :param env_file_path: path to env
    :return: True if token is in env file with
    """
    env_vars = read_env(env_file_path)
    if token_name in env_vars:
        return True
    return False
