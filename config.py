def read_env(env_file_path: str = "config.env") -> dict:
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


def write_env(env_vars: dict, env_file_path: str = "config.env") -> None:
    with open(env_file_path, "w") as file:
        for key, value in env_vars.items():
            file.write(f"{key}={value}\n")


def edit_env(env_vars: dict, env_file_path: str = "config.env") -> None:
    existing_env_vars = read_env(env_file_path)

    existing_env_vars.update(env_vars)

    write_env(existing_env_vars, env_file_path)

