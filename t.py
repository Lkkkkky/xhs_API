import requests
body={
        "email": "18100273137@qq.com",
        "keyword": "关键词"
    }
    
res=requests.post("http://localhost:5000/api/monitor",json=body,headers={'Content-Type': 'application/json'})
print(res.text)




