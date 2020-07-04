import requests

url = "https://messages-sandbox.nexmo.com/v0.1/messages"

payload = "{\n    \"from\": { \"type\": \"whatsapp\", \"number\": \"14157386170\" },\n    \"to\": { \"type\": \"whatsapp\", \"number\": \"6281252174013\" },\n    \"message\": {\n      \"content\": {\n        \"type\": \"text\",\n        \"text\": \"tes\"\n      }\n    }\n}"
headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg',
  'Content-Type': 'application/json',
  'Cookie': '__cfduid=dc0f71c7e05d662225bd04d0e565f0d441593584216'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))