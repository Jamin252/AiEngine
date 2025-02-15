import requests,jsonify

def check_elastic_is_up():
    res = requests.post('http://127.0.0.1:9200/', json={
        
    "prompt": "# hello world function\n\n",
    "language": "python"

    })
    return jsonify({'message': res.text})

ans = check_elastic_is_up()
print(ans)