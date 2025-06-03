import requests

url = "https://github.com/Brainstorm-Nonsense/chal-collection/commit/"
hex_chars = "0123456789abcdef"

count = 0

for i in hex_chars:
    for j in hex_chars:
        for k in hex_chars:
            for l in hex_chars:
                count += 1
                if count % 100 == 0:
                    print(f"Checked {count} combinations so far...")
                full_url = f"{url}{i}{j}{k}{l}"
                response = requests.get(full_url)
                if response.status_code == 200:
                    print(f"Found valid commit url : {full_url}")
                    with open("found_commit.txt", "a") as f:
                        f.write(full_url + "\n")
                    break