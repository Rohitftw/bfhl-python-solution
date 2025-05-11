import requests

#Webhook generation
gen_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
user_payload = {
    "name": "Rohit Sharma",
    "regNo": "0827AL221115",
    "email": "rohitsharma220887@acropolis.in"
}

resp = requests.post(gen_url, json=user_payload)
if resp.status_code != 200:
    print("Failed to generate webhook:", resp.text)
    exit()

data = resp.json()
webhook_url = data.get("webhook")
access_token = data.get("accessToken")

print("Webhook URL:", webhook_url)
print("Access Token:", access_token)

#Final SQL query
final_sql = """
SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    TIMESTAMPDIFF(YEAR, e.DOB, CURDATE()) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE DAY(p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;
"""

#Submit the answer
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}
answer_payload = {
    "finalQuery": final_sql.strip()
}

submit_resp = requests.post(webhook_url, headers=headers, json=answer_payload)
if submit_resp.status_code == 200:
    print("Submission successful!")
else:
    print("Submission failed:", submit_resp.text)
