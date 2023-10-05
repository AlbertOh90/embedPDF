def get_api_key_from_config(file_path="config.txt"):
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("OPENAI_API_KEY="):
                return line.strip().split("=")[1]
    return None
