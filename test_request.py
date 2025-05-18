import requests

while True:
    text = input("Press Enter to send a request...")
    msg = {"message": text}
    res = requests.post("http://localhost:5000/chat", json=msg)
    print(res.json())
    if input("Do you want to continue? (y/n): ").lower() != 'y':
        break
    print("Continuing...")  
