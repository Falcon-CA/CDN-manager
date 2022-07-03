import json
import requests

URL   = "https://cdn.falconca.ca/"
TOKEN = None
with open("token.txt") as tok_f:
    TOKEN = tok_f.read()


def create_file():
    name = input("File name: ")
    directory = input("Directory (Empty for root): ")
    private = input("Private (0/1): ")
    file = input("Local file name: ")

    try:
        private = int(private)
    except ValueError:
        print("Invalid private argument, must be 0 or 1")
        return
    
    try:
        headers = {"FCA-Token": TOKEN}
        data    = {"FCA-Name": name,
                   "FCA-Directory": directory, 
                   "FCA-Private": private}
        files   = {"FCA-File": open(file, "rb")}
    except FileNotFoundError:
        print("Unknown local file")
        return
    
    ret = requests.post(
        URL + "api?operation=create_file",
        headers=headers,
        data=data,
        files=files
    )
    print(f"{ret.content.decode()} - Status: {ret.status_code}")


def create_directory():
    name = input("Directory name: ")
    directory = input("Directory (Empty for root): ")
    private = input("Private (0/1): ")

    try:
        private = int(private)
    except ValueError:
        print("Invalid private argument, must be 0 or 1")
        return
    
    headers = {"FCA-Token": TOKEN}
    data    = {"FCA-Name": name,
               "FCA-Directory": directory, 
               "FCA-Private": private}
    
    ret = requests.post(
        URL + "api?operation=create_directory",
        headers=headers,
        data=data
    )
    print(f"{ret.content.decode()} - Status: {ret.status_code}")


def delete_file():
    file = input("File ID: ")

    headers = {"FCA-Token": TOKEN}
    data    = {"FCA-File": file}

    ret = requests.delete(
        URL + "api?operation=delete_file",
        headers=headers,
        data=data
    )
    print(f"{ret.content.decode()} - Status: {ret.status_code}")
    

def delete_directory():
    directory = input("Directory ID: ")

    headers = {"FCA-Token": TOKEN}
    data    = {"FCA-Directory": directory}

    ret = requests.delete(
        URL + "api?operation=delete_directory",
        headers=headers,
        data=data
    )
    print(f"{ret.content.decode()} - Status: {ret.status_code}")


def list_assets():
    directory = input("Directory (Empty for root): ")
    headers = {"FCA-Token": TOKEN}

    if directory != "":
        directory = f"directory/{directory}"
    
    ret = requests.get(
        URL + directory + "?mode=json",
        headers=headers
    )
    if ret.status_code != 200:
        print(f"{ret.content.decode()} - Status: {ret.status_code}")
    else:
        json_data = json.loads(ret.content.decode())
        dirs = ", ".join(json_data["directories"])
        files = ", ".join(json_data["files"])
        print(f"Directories: {dirs}")
        print(f"Files: {files}")


def file_info():
    file = input("File ID: ")
    headers = {"FCA-Token": TOKEN}

    ret = requests.head(
        URL + f"file/{file}/tmp",
        headers=headers
    )
    if ret.status_code != 200:
        print(f"{ret.content.decode()} - Status: {ret.status_code}")
    else:
        id_     = ret.headers['FCA-ID']
        name    = ret.headers['FCA-Name']
        size    = ret.headers['FCA-Size']
        created = ret.headers['FCA-Created']
        private = bool(ret.headers['FCA-Private'])
        print((f"ID: {id_}\n"
               f"Name: {name}\n"
               f"Size: {size}B\n"
               f"Created: {created}\n"
               f"Private: {private}"))


def directory_info():
    directory = input("Directory: ")
    headers = {"FCA-Token": TOKEN}

    ret = requests.head(
        URL + f"directory/{directory}",
        headers=headers
    )
    if ret.status_code != 200:
        print(f"{ret.content.decode()} - Status: {ret.status_code}")
    else:
        id_     = ret.headers['FCA-ID']
        name    = ret.headers['FCA-Name']
        created = ret.headers['FCA-Created']
        private = ret.headers['FCA-Private']
        assets  = ret.headers['FCA-Asset-Amount']
        print((f"ID: {id_}\n"
               f"Name: {name}\n"
               f"Created: {created}\n"
               f"Private: {private}\n"
               f"Asset Amount: {assets}"))


def edit_file():
    file_id = input("File ID: ")
    file_name = input("New file name: ")
    file_f = input("New local file: ")
    
    try:
        headers = {"FCA-Token": TOKEN}
        data    = {"FCA-FileID": file_id, "FCA-Name": file_name}
        files   = {"FCA-File": open(file_f, "rb")}
    except FileNotFoundError:
        print("Unknown local file")
        return
    
    ret = requests.put(
        URL + "api?operation=edit_file",
        headers=headers,
        data=data,
        files=files
    )
    print(f"{ret.content.decode()} - Status: {ret.status_code}")


if __name__ == "__main__":
    print("FalconCA CDN Manager")

    operations = {
        "create_file": create_file,
        "create_directory": create_directory,
        "delete_file": delete_file,
        "delete_directory": delete_directory,
        "list_assets": list_assets,
        "file_info": file_info,
        "directory_info": directory_info,
        "edit_file": edit_file
    }
    while True:
        op = input("\nOperation: ").lower()

        if op not in operations.keys():
            print(f"Unknown operation: {op}")
        else:
            operations[op]()