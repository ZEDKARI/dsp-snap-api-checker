import streamlit as st
import re
import json

req_header_token_lib = [
    'Content-Type:',
    'X-TIMESTAMP:',
    'X-CLIENT-KEY:',
    'X-SIGNATURE:'
]

req_header_lib = [
    'Authorization:', 
    'CHANNEL-ID:', 
    'Content-Type:', 
    'X-EXTERNAL-ID:', 
    'X-PARTNER-ID:', 
    'X-SIGNATURE:', 
    'X-TIMESTAMP:',
    'X-IP-ADDRESS:',
    'X-DEVICE-ID:',
    'X-LATITUDE:',
    'X-LONGITUDE:'
]

req_body_generate_mpm_lib = [
    'partnerReferenceNo:',
    'merchantId:',
    'terminalId:',
    'amount:',
    'value:',
]
def api():
    st.title('API')

    if st.button('Back', width='stretch'):
        st.session_state.page = 'home'
        st.rerun()


    st.divider()

    raw = '''
        "URL Endpoint: /v1.0/qr/qr-mpm-notify
        Header Request: ""Accept"": ""application/json, text/plain, */*"",
        ""Accept-Encoding"": ""gzip, deflate"",
        ""Accept-Language"": ""en-US,en;q=0.9"",
        ""Cache-Control"": ""no-cache"",
        ""Channel-Id"": ""DSP998"",
        ""Connection"": ""close"",
        ""Content-Length"": ""659"",
        ""Content-Type"": ""application/json"",
        ""Host"": ""svc-relay-q3n.dgti.co.id"",
        ""Pragma"": ""no-cache"",
        ""Sec-Fetch-Dest"": ""empty"",
        ""Sec-Fetch-Mode"": ""cors"",
        ""Sec-Fetch-Site"": ""same-origin"",
        ""User-Agent"": ""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"",
        ""X-External-Id"": ""621510479187"",
        ""X-Forwarded-For"": ""103.52.46.146, 103.52.46.146"",
        ""X-Forwarded-Proto"": ""https"",
        ""X-Forwarded-Scheme"": ""http"",
        ""X-Http-Method"": ""POST"",
        ""X-Partner-Id"": ""e6884e50-8bff-11f1-a7a4-9d5796fdbfe3"",
        ""X-Real-Ip"": ""103.52.46.146"",
        ""X-Relative-Url"": ""/v1.0/qr/qr-mpm-notify"",
        ""X-Signature"": ""PDZc1uDVfkG4j7iI9QR9tw5tLoS2vHiwMT9J3SzlvjbC4Ym4nIv0ARqGDZK2fJ6G3B8yiOjKA/jjv1cXG4BiOVSx4hXBBhscPHJCVtXteO/kh+X7QIdms+O4e8mJbSWwEFtriHGoJFxv2wZC0QIpMkcJH2FO/CxlQLmwSQ4FFvcPc8AwmRPeg13cXGU/fA3w0B/6wLuhp9e1IvLZEbo4vNwiBm6Pt4fxpRRmEjzjZWMiMX6UPLqBNHLrle135tHBNWArq/RpzqeI+mwjV7c06VMPYbxgZ/nM/5OapqoZLqwmJYQfNR28rj7aNboyor3LIgWwmhKZkDxycyA7QyUiUw=="",
        ""X-Timestamp"": ""2026-08-03T10:47:27+07:00""
        Request Body: 
        {
        ""amount"": {
            ""value"": ""47500.00"",
            ""currency"": ""IDR""
        },
        ""originalReferenceNo"": ""621510479187"",
        ""latestTransactionStatus"": ""00"",
        ""additionalInfo"": {
            ""invoiceNumber"": ""95756380979575638097"",
            ""merchantData"": {
            ""mpan"": ""9360099800000075105"",
            ""merchantId"": ""998026075104884"",
            ""terminalId"": ""DSP00001""
            },
            ""transactionDate"": ""2026-08-03T10:47:01+07:00"",
            ""transactionHash"": ""AFFD0F1B8CC5807BF0FE561054ABB07EBDC80C5A089DDEFF9F4E41D0BC7C8D24"",
            ""transactionId"": ""998026075104884.621510479187.0803104701"",
            ""issuerData"": {
            ""cPan"": ""9360011900000012291"",
            ""issInsCode"": ""119"",
            ""issInsName"": ""BANK RIAU KEPRI""
            }
        },
        ""originalPartnerReferenceNo"": ""1451-1785728721-1745-1495"",
        ""transactionStatusDesc"": ""PURCHASE_APPROVED""
        }"

    '''
    body = json.loads(raw)

    st.write(body)
    