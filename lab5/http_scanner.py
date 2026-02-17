import requests #type: ignore

base_url = "http://localhost:3000"

endpoints = [
    {"path": "/rest/products/search?q=apple", "method": "GET"},
    {"path": "/api/Feedbacks/", "method": "POST", "data": {"comment": "test"}},
    {"path": "/rest/admin/application-version", "method": "GET"},
    {"path": "/api/Challenges", "method": "GET"}
]

# PArt 5
reqgired_headers = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options"
]

def run_scanner():

    print("\n")
    print(f"{'Endpoint':<40} | {'Method':<6} | {'Status':<6} | {'Warnings':<8}")
    print("-"*75)

    for items in endpoints:
        url = f"{base_url}{items['path']}"
        method = items['method']

        try:
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json=items.get("data", {}), timeout=5)
            
            endpoint_name = items['path']
            status = response.status_code
            # length = len(response.text)

            # Part 5
            missing_headers = []
            for header in reqgired_headers:
                if header not in response.headers:
                    missing_headers.append(header)

            if missing_headers:
                warningg = f"Low Severity: Missing {', '.join(missing_headers)}"
            else:
                warningg = "None"

            print(f"{endpoint_name:<40} | {method:<6} | {status:<6} | {warningg}")
            
        
        except Exception as e:
            print("Error")


if __name__ == "__main__":
    run_scanner()
    print("\n")
