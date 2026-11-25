import streamlit as st
import pandas as pd
import re
from datetime import datetime

req_header_lib = [
    'Authorization:', 
    'CHANNEL-ID:', 
    'Content-Type:', 
    'X-EXTERNAL-ID:', 
    'X-PARTNER-ID:', 
    'X-SIGNATURE:', 
    'X-TIMESTAMP:'
]

req_body_acc_token_lib = [
    'grant_type:', 
    'additionalInfo:',
    'clientSecret:'
]

req_body_account_inq_lib = [
    'partnerReferenceNo:', 
    'beneficiaryBankCode:', 
    'beneficiaryAccountNo:', 
    'additionalInfo:', 
    'transferService:', 
    'amount:', 
    'value:', 
    'currency:', 
    'dspsign:'
]

req_body_trf_inter_lib = [
    'partnerReferenceNo:', 
    'sourceAccountNo:', 
    'beneficiaryBankCode:', 
    'beneficiaryAccountNo:', 
    'beneficiaryAccountName:', 
    'transactionDate:', 
    'amount:', 
    'value:', 
    'currency:',
    'additionalInfo:',
    'msgId:',
    'disbDescription:',
    'disbCategory:',
    'senderInfo:',
    'name:',
    'accountType:',
    'accountInstId:',
    'country:',
    'city:',
    'identificationType:',
    'identificationNumber:',
    'dspsign:'
]

req_body_trf_status_lib = [
    'originalPartnerReferenceNo:',
    'serviceCode:',
    'additionalInfo:',
    'msgId:',
    'dspsign:'
]

req_body_balance_inq_lib = [
    'accountNo:',
    'additionalInfo:',
    'dspsign:'
]

res_acc_token_lib = [
    'accessToken:',
    'tokenType:',
    'expiresIn:',
    'responseCode:',
    'responseMessage:'
]

res_account_inq_lib = [
    'responseCode:',
    'responseMessage:',
    'beneficiaryAccountName:',
    'beneficiaryAccountNo:',
    'referenceNo:',
    'additionalInfo:',
    'msgId:',
    'isoResponseCode:',
    'isoResponseMessage:'
]

res_trf_inter_lib = [
    'responseCode:',
    'responseMessage:',
    'referenceNo:',
    'beneficiaryAccountNo:',
    'additionalInfo:',
    'isoResponseCode:',
    'isoResponseMessage:'
]

res_trf_status_lib = [
    'responseCode:',
    'responseMessage:',
    'originalReferenceNo:',
    'referenceNumber:',
    'beneficiaryAccountNo:',
    'serviceCode:',
    'sourceAccountNo:',
    'latestTransactionStatus:',
    'transactionStatusDesc:',
    'additionalInfo:',
    'isoResponseCode:',
    'isoResponseMessage:'
]

res_balance_inq_lib = [
    'responseCode:',
    'responseMessage:',
    'accountInfos:',
    'balanceType:',
    'availableBalance:',
    'value:',
    'currency:'
]

expected_balance = [
    {
        "case" : "3.1",
        "code" : "401xx01",
        "message" : ["invalid", 'token'],
        "type" : "negative"
    },
    {
        "case" : "3.2",
        "code" : "401xx00",
        "message" : ["unauthorized"],
        "type" : "negative"
    },
    {
        "case" : "3.3",
        "code" : "400xx02",
        "message" : ["invalid", "mandatory", "field"],
        "type" : "negative"
    },
    {
        "case" : "3.4",
        "code" : "400xx01",
        "message" : ["invalid", "format", "field"],
        "type" : "negative"
    },
    {
        "case" : "3.5",
        "code" : "409xx00",
        "message" : ["conflict"],
        "type" : "negative"
    },
    {
        "case" : "3.6",
        "code" : "2001100",
        "message" : ["successful"],
        "type" : "positive"
    }
]

expected_transfer = [
    {
        "case" : "8.1",
        "code" : "401xx01",
        "message" : ["invalid", 'token'],
        "type" : "negative"
    },
    {
        "case" : "8.2",
        "code" : "401xx00",
        "message" : ["unauthorized"],
        "type" : "negative"
    },
    {
        "case" : "8.3",
        "code" : "400xx02",
        "message" : ["invalid", "mandatory", "field"],
        "type" : "negative"
    },
    {
        "case" : "8.4",
        "code" : "400xx01",
        "message" : ["invalid", "format", "field"],
        "type" : "negative"
    },
    {
        "case" : "8.5",
        "code" : "409xx00",
        "message" : ["conflict"],
        "type" : "negative"
    },
    {
        "case" : "8.7",
        "code" : "2001600",
        "message" : ["successful"],
        "type" : "positive"
    },
    {
        "case" : "8.10",
        "code" : "2001800",
        "message" : ["successful"],
        "type" : "positive"
    },
    {
        "case" : "8.11",
        "code" : "4031814",
        "message" : ["insufficient", "fund"],
        "type" : "negative"
    },
    {
        "case" : "8.12",
        "code" : "4091801",
        "message" : ["duplicate", 'partnerreferenceno'],
        "type" : "negative"
    },
    {
        "case" : "8.13",
        "code" : "2003600",
        "message" : ["successful"],
        "type" : "positive"
    }
]

def is_valid_timestamp(value: str) -> bool:
    PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")

    if not isinstance(value, str) or not PATTERN.match(value):
        return 'FORMAT INVALID!'
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
        return value
    except ValueError:
        return 'FORMAT INVALID!'

def is_valid_authorize(value: str) -> bool:
    BEARER_PATTERN = re.compile(r"^Bearer ([0-9a-f]{54})$")

    if not isinstance(value, str) or not BEARER_PATTERN.fullmatch(value):
        return 'FORMAT INVALID!'
    else:
        return value


def disburse_check_summary(df, case):

    req_temp = df['Request']
    req_temp = req_temp.replace('"','')
    req_temp = req_temp.replace('{','')
    req_temp = req_temp.replace('}','')
    req_temp = req_temp.replace('[','')
    req_temp = req_temp.replace(']','')
    req_temp = req_temp.replace('\\','')
    url = re.search(r"https?://\S+", req_temp)
    if url:
        st.write(f':green-background[:green[URL Endpoint : {url.group(0)}]]')
    else:
        st.write(':red-background[:red[URL Not Found!]]')
    url = url.group(0)
    endpoint = url.split("/")[-1]
    if df['Service'] == 'Any Service':
        if endpoint == 'balance-inquiry':
            req_body_lib = req_body_balance_inq_lib
            res_body_lib = res_balance_inq_lib
        elif endpoint == 'b2b':
            req_body_lib = req_body_acc_token_lib
            res_body_lib = res_acc_token_lib
        elif endpoint == 'account-inquiry-external':
            req_body_lib = req_body_account_inq_lib
            res_body_lib = res_account_inq_lib
        elif endpoint == 'transfer-interbank':
            req_body_lib = req_body_trf_inter_lib
            res_body_lib = res_trf_inter_lib
        elif endpoint == 'status':
            req_body_lib = req_body_trf_status_lib
            res_body_lib = res_trf_status_lib
        # elif endpoint == 'notify':
        #     req_body_lib = req_body_
        #     res_body_lib = res_trf_status_lib

    elif df['Service'] == 'Balance Inquiry':
        req_body_lib = req_body_balance_inq_lib
        res_body_lib = res_balance_inq_lib
    elif df['Service'] == 'Eksternal Account Inquiry':
        req_body_lib = req_body_account_inq_lib
        res_body_lib = res_account_inq_lib
    elif df['Service'] == 'Interbank Trigger Transfer':
        req_body_lib = req_body_trf_inter_lib
        res_body_lib = res_trf_inter_lib
    elif df['Service'] == 'Transaction Status Inquiry':
        req_body_lib = req_body_trf_status_lib
        res_body_lib = res_trf_status_lib

    tb_header = []
    for header in req_header_lib:
        match = re.search(rf"{header}\s*+([^,\n]+)", req_temp)

        if match:
            token = match.group(1)
            if header == 'Authorization:':
                val = is_valid_authorize(token)
            elif header == 'X-TIMESTAMP:':
                val = is_valid_timestamp(token)
            elif header in ['CHANNEL-ID:', 'X-EXTERNAL-ID:', 'X-PARTNER-ID:', 'X-SIGNATURE:']:
                val = token
            elif header == 'Content-Type:':
                if token.lower() == 'application/json':
                    val = token
                else:
                    val = 'INVALID FORMAT!'
            else:
                val = 'Value Not Found!'
                
            st.code(f'✅ {header} {val}')
            tb_header.append({
                'Header' : header,
                'Value' : val,
                'Check' : '✅'
            })
        else:
            st.code(f"❌ {header} Not Found!")
            tb_header.append({
                'Header' : header,
                'Value' : '--',
                'Check' : '❌'
            })

    st.table(tb_header)
    st.divider()

def disburse_check_detailed(df, case):
    if case['type'] == 'positive':
        info_color = 'green'
        info_message = 'Response'
    else:
        info_color = 'red'
        info_message = 'Error'
    st.table(
        {
            ":material/lists: Test Case": f":gray-badge[**{case['case']}**]",
            ":material/api: Endpoint": f":blue-badge[{df['Service']}]",
            ":material/bug_report: Scenario": f":yellow-badge[{df['Scenario']}]",
            ":material/fact_check: Expected Result": f":{info_color}-badge[{info_message} Code: {case['code']} \\\n{info_message} Message:]",
        },
        border="horizontal",
        width="content",
    )
def new_disburse():
    state = st.session_state

    st.title('NEW DISBURSE')

    excel_file = st.file_uploader("Upload an Excel file", type=["xlsx"])


    if excel_file:
        
        balance_df = pd.read_excel(excel_file, sheet_name='Balance Services', header=8)  # reads the first sheet
        transfer_df = pd.read_excel(excel_file, sheet_name='Interbank Transfer', header=8)  # reads the first sheet

        balance_df = balance_df[:6]
        transfer_df = pd.concat([
            transfer_df.iloc[0:5],    # baris 1-3
            transfer_df.iloc[6:7],    # baris 5-6
            transfer_df.iloc[9:13],   # baris 9-12
        ]).reset_index(drop=True)

        summary, detailed = st.tabs(['Summary', 'Detailed'])

        with summary:
            for index, row in balance_df.iterrows():
                disburse_check_summary(row, expected_balance[index])

            for index, row in transfer_df.iterrows():
                disburse_check_summary(row, expected_transfer[index])

        with detailed:
            for index, row in balance_df.iterrows():
                disburse_check_detailed(row, expected_balance[index])

            for index, row in transfer_df.iterrows():
                disburse_check_detailed(row, expected_transfer[index])