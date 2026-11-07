import streamlit as st
import re
import json
from datetime import datetime


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

req_body_acc_token_lib = [
    '1grant_type:',
    '1additionalInfo:',
    '2clientSecret:',
    '1}'
]

req_body_generate_mpm_lib = [
    '1partnerReferenceNo:',
    '1merchantId:',
    '1terminalId:',
    '1amount:',
    '2value:',
    '2currency:',
    '1}',
    '1additionalInfo:',
    '2productType:',
    '2isWebview:',
    '2billingId:',
    '1}',
    '1validityPeriod:',
    '1callbackUrl:'
]

req_body_notify_mpm_lib = [
    '1originalPartnerReferenceNo:',
    '1originalReferenceNo:',
    '1latestTransactionStatus:',
    '1transactionStatusDesc:',
    '1amount:',
    '2value:',
    '2currency:',
    '1}',
    '1additionalInfo:',
    '2transactionHash:',
    '2transactionDate:',
    '2invoiceNumber:',
    '2transactionId:',
    '2issuerData:',
    '3cPan:',
    '3issInsCode:',
    '3issInsName:',
    '2}',
    '2merchantData:',
    '3merchantId:',
    '3terminalId:',
    '3mpan:',
    '2}',
    '1}'
]

req_body_mpm_status_lib = [
    '1originalPartnerReferenceNo:',
    '1originalExternalId:',
    '1transactionDate:',
    '1serviceCode:',
    '1additionalInfo:',
    '2transactionHash:',
    '2merchantId:',
    '1}'
]

req_body_mpm_refund_lib = [
    '1partnerRefundNo:',
    '1originalPartnerReferenceNo:',
    '1originalReferenceNo:',
    '1originalExternalId:',
    '1merchantId:',
    '1refundAmount:',
    '2value:',
    '2currency:',
    '1}',
    '1reason:'
]

res_acc_token_lib = [
    '1accessToken:',
    '1tokenType:',
    '1expiresIn:',
    '1responseCode:',
    '1responseMessage:'
]

res_mpm_generate_lib = [
    '1responseCode:',
    '1responseMessage:',
    '1partnerReferenceNo:',
    '1qrContent:',
    '1redirectUrl:',
    '1additionalInfo:',
    '2transactionHash:',
    '1}'
]

res_mpm_notify_lib = [
    '1responseCode:',
    '1responseMessage:'
]

res_mpm_status_lib = [
    '1responseCode:',
    '1responseMessage:',
    '1originalPartnerReferenceNo:',
    '1originalReferenceNo:',
    '1latestTransactionStatus:',
    '1transactionStatusDesc:',
    '1transactionDate:',
    '1serviceCode:',
    '1amount:',
    '2value:',
    '2currency:',
    '1}',
    '1additionalInfo:',
    '2transactionHash:',
    '2invoiceNumber:',
    '2transactionId:',
    '2issuerData:',
    '3cPan:',
    '3issInsCode:',
    '3issInsName:',
    '2}',
    '2merchantData:',
    '3merchantId:',
    '3terminalId:',
    '3mpan:',
    '2}',
    '1}'
]

res_mpm_refund_lib = [
    '1responseCode:',
    '1responseMessage:',
    '1originalPartnerReferenceNo:',
    '1originalReferenceNo:',
    '1originalExternalId:',
    '1partnerRefundNo:',
    '1refundNo:',
    '1refundTime:',
    '1refundAmount:',
    '2value:',
    '2currency:'
]

def is_valid_timestamp(value: str) -> bool:
    PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")

    if not isinstance(value, str) or not PATTERN.match(value):
        return '⚠️ FORMAT INVALID! ⚠️! '
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
        return value
    except ValueError:
        return '⚠️ FORMAT INVALID! ⚠️'

def is_valid_authorize(value: str) -> bool:
    BEARER_PATTERN = re.compile(r"Bearer [A-Za-z0-9\-._~+/]+=*")

    if not isinstance(value, str) or not BEARER_PATTERN.fullmatch(value):
        return '⚠️ FORMAT INVALID! ⚠️'
    else:
        return value

def divider_vertical():
    st.markdown(
        "<div style='border-left: 1px solid #888; height: 180px; margin: auto; width: 1px;'></div>",
        unsafe_allow_html=True,
    )

def snap_api(tc, case_type,  service, scenario, code, message, keyword):
    if 'xx' not in code:
        rc = rf"\b{code}\b"
    else:
        rc = rf"\b{code[:3]}\d{{2}}{code[5:]}\b"

    if case_type == 'Positive':
        info_message = 'Response'
        info_color = 'green'
    elif case_type == 'Negative':
        info_message = 'Error'
        info_color = 'red'


    with st.container(horizontal=True):
        divider_vertical()
        st.table(
            {
                ":material/lists: Test Case": f":gray-badge[**{tc}**]",
                ":material/api: Endpoint": f":blue-badge[{service}]",
                ":material/bug_report: Scenario": f":yellow-badge[{scenario}]",
                ":material/fact_check: Expected Result": f":{info_color}-badge[{info_message} Code: {code} \\\n{info_message} Message: '{message}']",
            },
            border="horizontal",
            width="content",
        )

        if service == 'Any Service':
            divider_vertical()
            end_point = st.radio('Endpoint:', options=['Access Token', 'QR MPM - Generate QR', 'Payment Notification', 'Transaction Status Inquiry', 'Refund Payment'], horizontal=False, key=f'radio_{tc.replace(".","_")}')
        else:
            end_point = service

        divider_vertical()
        st.radio('Flag:', options=['Pass', 'Not Tested', 'Fail'], horizontal=False, key=f'flag_{tc.replace(".","_")}', index=1)
        divider_vertical()

        if end_point == 'Access Token':
            req_body_lib = req_body_acc_token_lib
            res_body_lib = res_acc_token_lib
        elif end_point == 'QR MPM - Generate QR':
            req_body_lib = req_body_generate_mpm_lib
            res_body_lib = res_mpm_generate_lib
        elif end_point == 'Payment Notification':
            with st.container(width='content'):
                st.code('Untuk Notify Tidak ada header\n- AUTHORIZATION\n- X-DEVICE-ID')
            req_body_lib = req_body_notify_mpm_lib
            res_body_lib = res_mpm_notify_lib
        elif end_point == 'Transaction Status Inquiry':
            req_body_lib = req_body_mpm_status_lib
            res_body_lib = res_mpm_status_lib
        elif end_point == 'Refund Payment':
            req_body_lib = req_body_mpm_refund_lib
            res_body_lib = res_mpm_refund_lib

    with st.container(horizontal=True):
        with st.container():
            req = False
            req_3_2 = st.text_area('Request', key=f'req_{tc.replace(".","_")}', width='stretch')
            if st.button('Check Request', key=f'btn_req_{tc.replace(".","_")}', width='stretch'):
                req = True

            if req:
                if req_3_2:
                    temp = req_3_2.replace('"','')
                    temp = temp.replace('{','')
                    temp = temp.replace('}','')
                    temp = temp.replace('[','')
                    temp = temp.replace(']','')
                    temp = temp.replace('\\','')
                    url = re.search(r"https?://\S+", temp)
                    if url:
                        st.write(f':green-background[:green[URL Endpoint : {url.group(0)}]]')
                    else:
                        st.write(':red-background[:red[URL Not Found!]]')
                    with st.expander('Header'):
                        for header in req_header_lib:
                            match = re.search(rf"{header}\s*+([^,\n]+)", temp, re.IGNORECASE)
                            if match:
                                token = match.group(1)
                                if header == 'Authorization:':
                                    val = is_valid_authorize(token)
                                elif header.upper() == 'X-TIMESTAMP:':
                                    val = is_valid_timestamp(token)
                                elif header.upper() in ['CHANNEL-ID:', 'X-EXTERNAL-ID:', 'X-PARTNER-ID:', 'X-SIGNATURE:', 'X-DEVICE-ID:']:
                                    val = token
                                elif header.upper() in ['X-IP-ADDRESS:', 'X-LATITUDE:', 'X-LONGITUDE:']:
                                    val = '(Optional)' + token
                                elif header == 'Content-Type:':
                                    if token.lower() == 'application/json':
                                        val = token
                                    else:
                                        val = 'INVALID FORMAT!'
                                else:
                                    val = 'Value Not Found!'
                                    
                                st.code(f'✅ {header} {val}')
                            elif header.upper() in ['X-IP-ADDRESS:', 'X-LATITUDE:', 'X-LONGITUDE:']:
                                st.code(f"❌ (Optional) {header} Not Found!")
                            else:
                                st.code(f"❌ {header} Not Found!")

                    with st.expander('Body'):
                        text_json = '{\n'
                        for index in range(len(req_body_lib)):
                            body_raw = req_body_lib[index]
                            body = body_raw[1:]
                            indent = int(body_raw[:1])
                            if body != '}':
                                match = re.search(rf"{body}\s*+([^,\n]+)", temp)
                                if match and body not in ['additionalInfo:', 'amount:', 'senderInfo:', 'merchantData:', 'issuerData:']:
                                    token = match.group(1)
                                    if body == 'validityPeriod:':
                                        st.code(f'✅ {body} {is_valid_timestamp(token)}')
                                    else:
                                        st.code(f'✅ {body} {token}')
                                    text_json += f'{indent*" "}"{body[:-1]}": "{token}"'
                                    if index + 1 != len(req_body_lib) and req_body_lib[index+1][1:] != '}' and re.search(rf"{req_body_lib[index+1][1:]}\s*+([^,\n]+)", temp):
                                        text_json += ',\n'
                                    else:
                                        text_json += '\n'
                                elif match and body in ['additionalInfo:', 'amount:', 'senderInfo:', 'merchantData:', 'issuerData:']:
                                    token = match.group(1)
                                    st.write(f'✅ {body} Found!')
                                    text_json += f'{int(body_raw[:1])*" "}"{body[:-1]}": {{\n'
                                else:
                                    st.code(f"❌ {body} Not Found!")
                            else:
                                text_json += f'{indent*" "}}}'
                                if index + 1 != len(req_body_lib) and re.search(rf"{req_body_lib[index+1][1:]}\s*+([^,\n]+)", temp) and req_body_lib[index+1][1:] != '}':
                                    text_json += ',\n'
                                else:
                                    text_json += '\n'

                        text_json += '}'

                        st.code(text_json)


        with st.container():
            res = False
            res_3_2 = st.text_area('Response', key=f'res_{tc.replace(".","_")}', width='stretch')
            if st.button('Check Response', key=f'btn_res_{tc.replace(".","_")}', width='stretch'):
                res = True

            if res:
                if res_3_2:
                    temp = res_3_2.replace('"','')
                    temp = temp.replace('{','')
                    temp = temp.replace('}','')
                    temp = temp.replace('[','')
                    temp = temp.replace(']','')
                    temp = temp.replace('\\','')

                    with st.expander('Body', width='stretch'):
                        text_json = '{\n'
                        for index in range(len(res_body_lib)):
                            body_raw = res_body_lib[index]
                            body = str(body_raw[1:])
                            indent = int(body_raw[:1])
                            if body != '}':
                                match = re.search(rf"{body}\s*+([^,\n]+)", temp)
                                if match:
                                    token = match.group(1)
                                    if body == 'responseCode:':
                                        if re.search(rc, token):
                                            st.code(f'✅ {body} {token}')
                                        else:
                                            st.code(f'❌ {body} {token} not pass')
                                        text_json += f'{indent*" "}"{body[:-1]}": "{token}"'
                                        if index + 1 != len(res_body_lib) and res_body_lib[index+1][1] != '}' and re.search(rf"{res_body_lib[index+1][1:]}\s*+([^,\n]+)", temp):
                                            text_json += ',\n'
                                        else:
                                            text_json += '\n'
                                    elif body == 'responseMessage:':
                                        if all(k.lower() in token.lower() for k in keyword):
                                            st.code(f'✅ {body} {token}')
                                        else:
                                            st.code(f'❌ {body} {token} not pass')
                                        text_json += f'{indent*" "}"{body[:-1]}": "{token}"'
                                        if index + 1 != len(res_body_lib) and res_body_lib[index+1][1] != '}' and re.search(rf"{res_body_lib[index+1][1:]}\s*+([^,\n]+)", temp):
                                            text_json += ',\n'
                                        else:
                                            text_json += '\n'
                                    elif body in ['additionalInfo:', 'accountInfos:', 'availableBalance:', 'merchantData:', 'issuerData:', 'amount:', 'refundAmount:']:
                                        st.write(f'✅ {body} Found!')
                                        text_json += f'{int(body_raw[:1])*" "}"{body[:-1]}": {{\n'
                                    else:
                                        st.code(f'✅ {body} {token}')
                                        text_json += f'{indent*" "}"{body[:-1]}": "{token}"'
                                        if index + 1 != len(res_body_lib) and res_body_lib[index+1][1] != '}' and re.search(rf"{res_body_lib[index+1][1:]}\s*+([^,\n]+)", temp):
                                            text_json += ',\n'
                                        else:
                                            text_json += '\n'

                                else:
                                    st.code(f'❌ {body} not found!')
                            else:
                                if index + 1 != len(res_body_lib) and res_body_lib[index+1][1] != '}' and re.search(rf"{res_body_lib[index+1][1:]}\s*+([^,\n]+)", temp):
                                    text_json += f'{indent*" "}}}'
                                    text_json += ',\n'
                                else:
                                    text_json += '\n'
                        
                        text_json += '}'
                        st.code(text_json)

def api():
    st.title('API')

    if st.button('Back', width='stretch'):
        st.session_state.page = 'home'
        st.rerun()

    st.divider()
    snap_api('18.1', 'Negative', 'Any Service', 'Access Token Invalid', '401xx01', 'Access Token Invalid', ['invalid', 'token'])
    st.divider()
    snap_api('18.2', 'Negative', 'Any Service', 'Unauthorized . Signature', '401xx00', 'Unauthorized Signature', ['unauthorized'])
    st.divider()
    snap_api('18.3', 'Negative', 'Any Service', 'Missing Mandatory Field {} …, etc', '400xx02', 'Invalid Mandatory Field {........}', ['invalid', 'mandatory', 'field'])
    st.divider()
    snap_api('18.4', 'Negative', 'Any Service', 'Invalid Field Format {} .., etc', '400xx01', 'Invalid Field Format {........}', ['invalid', 'format', 'field'])
    st.divider()
    snap_api('18.5', 'Negative', 'Any Service', 'Cannot use the same X-EXTERNAL-ID', '409xx00', 'Conflict', ['conflict'])
    st.divider()
    snap_api('18.6', 'Positive', 'QR MPM - Generate QR', 'Show QR Code', '2004700', 'Successful', ['successful'])
    st.divider()
    snap_api('18.7', 'Negative', 'QR MPM - Generate QR', 'Invalid Merchant. Merchant tidak ada/tidak terdaftar', '4044708', 'Invalid Merchant', ['invalid', 'merchant'])
    st.divider()
    snap_api('18.18', 'Positive', 'Payment Notification', 'Notification for Successful Transaction\\\nField "latestTransactionStatus" diisi dengan value "00"', '2005200', 'Successful', ['successful'])
    st.divider()
    snap_api('18.19', 'Positive', 'Payment Notification', 'Notification for Failed Transaction\\\nField "latestTransactionStatus" diisi dengan value "06"', '2005200', 'Successful', ['successful'])
    st.divider()
    snap_api('18.24', 'Positive', 'Transaction Status Inquiry', 'Inquiry Status atas transaksi  berhasil\\\nField "latestTransactionStatus" diisi dengan value "00"', '2005300', 'Successful', ['successful'])


    
    