import requests
body={
        "email": "luyao-operate@lucy.ai",
        "keyword": "关键词"
    }
    
res=requests.post("http://localhost:5000/api/monitor",json=body,headers={'Content-Type': 'application/json'})
print(res.text)