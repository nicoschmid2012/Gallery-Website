import socket as sk
import threading as th
import json
import os

IP_Addr = "0.0.0.0"
PORT = 5500

def throw_error(error) -> bytes:
    global response
    if not response:
        response = f"HTTP/1.1 404 NOT FOUND\r\ntext/html\r\n\r\n<h1>{error} not found</h1>"
        print("Error: " + error)
        return response.encode()


def make_socket(IP, PORT):
    s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen()
    return s

def get_img_by_query(query):
    querys = query.split("&")
    response = None

    for request in querys:
        if request.startswith("s="):
            status = "200 OK"
            query_info = "finding picture"
            search = request.removeprefix("s=")
            try:
                with open("picture_search_file.json","r") as search_file:
                    json_search = json.load(search_file)
            except:
                throw_error("files")

            for picture_id, info in json_search.items():
                print(info)
                print(search)
                if info["name"] == search or info["id"] == str(search):
                    picture = info["file"]
                    description = info["description"]

        else:
            response = throw_error("querry")
            status = "500 Internal Server Error"
            info = "the query is invalid"
            data = None
    try:
        content = {
            "status": status,
            "info": query_info,
            "data": {
                "picture": picture,
                "description": description
            }
        }
    except:
        response = throw_error("info")

    if response:
        return response
    else:
        return json.dumps(content).encode()

def get_response_by_path(path, query):
    response = None
    use_length = False
    print(query)

    if path == "/":
        status = "200 OK"
        content_type = "text/html"
        try:
            with open("webpage/index.html","rb") as html:
                content = html.read()
        except:
            response = throw_error("html")

    elif path == "/style":
        status = "200 OK"
        content_type = "text/css"
        try:
            with open("webpage/style.css","rb") as style:
                content = style.read()
        except:
            response = throw_error("style")

    elif path == "/script":
        status = "200 OK"
        content_type = "text/javascript"
        try:
            with open("webpage/script.js","rb") as script:
                content = script.read()
        except:
            response = throw_error("script")

    elif path == "/picture":
        status = "200 OK"
        content_type = "image/png"
        picture_id = 0

        try:
            picture_id = int(query.removeprefix("p="))
        except:
            response = throw_error("query")

        try:
            with open("picture_search_file.json","r") as search_file:
                search = json.load(search_file)
                for ids, info in search.items():
                    if info["id"] == picture_id:
                        picture = info["file"]

        except:
            response = throw_error("picture id")

        try:
            with open("pictures/" + picture + ".png","rb") as picture:
                content = picture.read()
        except:
            response = throw_error("picture")

        try:
            content_length = len(content)
            use_length = True
        except:
            pass

    elif path == "/search":
        status = "200 OK"
        content_type = "application/json"
        if query:
            content = get_img_by_query(query)
        else:
            content = throw_error("query")

        if content == bytes:
            response = content

    elif path == "/description":
        status = "200 OK"
        content_type = "application/json"
        content = {
            "status": status,
            "info": "description is send",
            "data": {
                "desc1": "This shows about 18 Mobs on a PNG background",
                "desc2": "This picture shows a wandering trader exploring with his snifer",
                "desc3": "This is a cut clipart of a slime and a bee"
            }
        }

    else:
        response = throw_error("path")

    if not response:
        response = f"HTTP/1.1 {status}\r\n"
        response += f"COntent-Type: {content_type}\r\n"
        if use_length:
            response += f"Content-Length: {content_length}\r\n"
        response += "\r\n"
        response = response.encode() + content

    return response

backend = make_socket(IP_Addr, PORT)



if __name__ == "__main__":
    print(f"Running with port {PORT}")
    while True:
        conn, addr = backend.accept()
        request = conn.recv(1024).decode()
        info = []
        for line in request.split("\n"):
            info.append(line.strip("\r"))

        querry :str = None
        path1 = info[0]
        path2 = path1.split()
        print(path2)
        try:
            path3 = path2[1].split("?")
            path = path3[0]
            querry = path3[1]
        except:
            throw_error("path")

        response = get_response_by_path(path, querry)

        conn.send(response)
        conn.close()
