import streamlit as st
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

def divider_vertical():
    st.markdown(
        "<div style='border-left: 1px solid #888; height: 180px; margin: auto; width: 1px;'></div>",
        unsafe_allow_html=True,
    )

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
    BEARER_PATTERN = re.compile(r"Bearer [A-Za-z0-9\-._~+/]+=*")

    if not isinstance(value, str) or not BEARER_PATTERN.fullmatch(value):
        return 'FORMAT INVALID!'
    else:
        return value


def disburse(tc, case_type, service, scenario, response_code, response_message, keyword):
    if f'req_dis_{tc.replace('.','_')}' not in st.session_state:
        st.session_state[f'req_dis_{tc.replace('.','_')}'] = False
    if f'res_dis_{tc.replace('.','_')}' not in st.session_state:
        st.session_state[f'res_dis_{tc.replace('.','_')}'] = False

    if 'xx' not in response_code:
        rc = rf"\b{response_code}\b"
    else:
        rc = rf"\b{response_code[:3]}\d{{2}}{response_code[5:]}\b"

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
                ":material/fact_check: Expected Result": f":{info_color}-badge[{info_message} Code: {response_code} \\\n{info_message} Message: '{response_message}']",
            },
            border="horizontal",
            width="content",
        )
        if service == 'Any Services':
            divider_vertical()
            end_point = st.radio('Endpoint:', options=['Access Token', 'Account Inquiry', 'Transfer Interbank', 'Status', 'Balance Inquiry'], horizontal=False, key=f'radio_{tc.replace('.','_')}')
        else:
            end_point = service

        divider_vertical()
        st.radio('Flag:', options=['Pass', 'Not Tested', 'Fail'], horizontal=False, key=f'flag_{tc.replace('.','_')}', index=1)
        divider_vertical()

        if end_point == 'Access Token':
            req_body_lib = req_body_acc_token_lib
            res_body_lib = res_acc_token_lib
        elif end_point == 'Eksternal Account Inquiry':
            req_body_lib = req_body_account_inq_lib
            res_body_lib = res_account_inq_lib
        elif end_point == 'Interbank Trigger Transfer':
            req_body_lib = req_body_trf_inter_lib
            res_body_lib = res_trf_inter_lib
        elif end_point == 'Status':
            req_body_lib = req_body_trf_status_lib
            res_body_lib = res_trf_status_lib
        elif end_point == 'Balance Inquiry':
            req_body_lib = req_body_balance_inq_lib
            res_body_lib = res_balance_inq_lib

    with st.container(horizontal=True):
        with st.container():
            req_3_2 = st.text_area('Request', key=f'req_{tc.replace('.','_')}', width='stretch')
            if st.button('Check Request', key=f'btn_req_{tc.replace('.','_')}', width='stretch'):
                st.session_state[f'req_dis_{tc.replace('.','_')}'] = True

            if st.session_state[f'req_dis_{tc.replace('.','_')}']:
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
                            match = re.search(rf"{header}\s*+([^,\n]+)", temp)

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
                            else:
                                st.code(f"❌ {header} Not Found!")
                    with st.expander('Body'):
                        for body in req_body_lib:
                            match = re.search(rf"{body}\s*+([^,\n]+)", temp)
                            if match and body not in ['additionalInfo:', 'amount:', 'senderInfo:']:
                                token = match.group(1)
                                st.code(f'✅ {body} {token}')
                            elif match and body in ['additionalInfo:', 'amount:', 'senderInfo:']:
                                token = match.group(1)
                                st.write(f'✅ {body} Found!')
                            else:
                                st.code(f"❌{body} Not Found!")


        with st.container():
            res_3_2 = st.text_area('Response', key=f'res_{tc.replace('.','_')}', width='stretch')
            if st.button('Check Response', key=f'btn_res_{tc.replace('.','_')}', width='stretch'):
                st.session_state[f'res_dis_{tc.replace('.','_')}'] = True

            if st.session_state[f'res_dis_{tc.replace('.','_')}']:
                if res_3_2:
                    temp = res_3_2.replace('"','')
                    temp = temp.replace('{','')
                    temp = temp.replace('}','')
                    temp = temp.replace('[','')
                    temp = temp.replace(']','')
                    with st.expander('Body', width='stretch'):
                        for body in res_body_lib:
                            match = re.search(rf"{body}\s*+([^,\n]+)", temp)
                            if match:
                                token = match.group(1)
                                if body == 'responseCode:':
                                    if re.search(rc, token):
                                        st.code(f'✅ {body} {token}')
                                    else:
                                        st.code(f'❌ {body} {token} not pass')
                                elif body == 'responseMessage:':
                                    if all(k.lower() in token.lower() for k in keyword):
                                        st.code(f'✅ {body} {token}')
                                    else:
                                        st.code(f'❌ {body} {token} not pass')
                                else:
                                    st.code(f'✅ {body} {token}')
                            else:
                                st.code(f'❌ {body} not found!')
                                

def disbursement():
    st.title('Disbursement')

    st.markdown(
        """
        <style>
        /* tab list selebar container */
        div[data-baseweb="tab-list"] {
            width: 100%;
        }
        /* tiap tab dapat porsi lebar yang sama */
        button[data-baseweb="tab"] {
            flex: 1 1 0;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button('Back', width='stretch'):
        st.session_state.page = 'home'
        suffixes = [f"3_{i}" for i in range(1, 7)] + [f"8_{i}" for i in (1, 2, 3, 4, 5, 7, 10, 11, 12, 13)]

        for s in suffixes:
            for prefix in ("req", "res"):
                st.session_state[f"{prefix}_dis_{s}"] = False
        st.rerun()


    st.divider()
    # st.select_slider("Pick a size", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # st.segmented_control("Filter", ["Open", "Closed", 'hello', 'h', 'wdakowdwadoa', 'wdoakwdkawd', 'klklklklkk'], selection_mode="single", wrap=True)
    # if 'test' not in st.session_state: 
    #     st.session_state.test = 'CSV'

    # def set_val():
    #     st.session_state.test = st.session_state.helwrold
        
    # st.menu_button("Export", options=["CSV", "JSON", "PDF"], key='helwrold', on_click=set_val)


    # if st.session_state.test == 'CSV':
    #     st.write('ini CSV')
    # elif st.session_state.test == 'JSON':
    #     st.write('ini JSON')
    # elif st.session_state.test == 'PDF':
    #     st.write('ini PDF')

    # st.write(st.session_state.helwrold)
    # dwakdo = st.feedback("stars", default=2)
    # dwakdos = st.feedback("faces")
    # if dwakdo:
    #     st.write(int(dwakdo)+1)
    # st.pills("Tags", ["Sports", "Politics"])

    # st.button(':red[:material/star_rate_half:]')

    # @st.dialog('tadwjd')
    # def tedsadw():
    #     html_test = '''<div class="radial-menu">
    #         <button class="menu-selector" id="selector">
    #             <span class="selector-icon" id="selector-icon">?</span>
    #         </button>

    #         <div class="menu-backdrop" id="backdrop"></div>

    #         <div class="menu-overlay" id="overlay">
    #             <div class="menu-ring" id="ring">
    #                 <!-- Items generated dynamically from data.options -->
    #             </div>
    #         </div>
    #     </div>'''

    #     css_test = '''
    #     .radial-menu {
    #     --item-size: 2.25rem;   /* diameter tombol (dulu 3.25rem) */
    #     --icon-size: 1rem;      /* ukuran emoji/isi (dulu 1.5rem) */
    #     --ring-size: 8rem;      /* area lingkaran menu (dulu 13rem) */
    #     --radius: 3rem;      /* jarak item dari tengah (dulu 4rem) */

    #     position: relative;
    #     display: inline-block;
    #     font-family: var(--st-font);
    #     }

    #     /* The circular selector button and menu items*/
    #     .menu-selector,
    #     .menu-item {
    #     width: var(--item-size);
    #     height: var(--item-size);
    #     border-radius: 50%;
    #     border: 2px solid var(--st-border-color);
    #     cursor: pointer;
    #     background: var(--st-secondary-background-color);
    #     display: flex;
    #     align-items: center;
    #     justify-content: center;
    #     transition: all 0.2s ease;
    #     font-size: var(--icon-size);
    #     padding: 0;
    #     }

    #     .menu-selector:hover {
    #     transform: scale(1.05);
    #     border-color: var(--st-primary-color);
    #     }

    #     /* Overlay container */
    #     .menu-overlay {
    #     position: absolute;
    #     top: 50%;
    #     left: 50%;
    #     transform: translate(-50%, -50%);
    #     z-index: 100;
    #     pointer-events: none;
    #     }

    #     /* The ring of menu items */
    #     .menu-ring {
    #     position: relative;
    #     width: var(--ring-size);
    #     height: var(--ring-size);
    #     transform: scale(0);
    #     opacity: 0;
    #     transition:
    #         transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1),
    #         opacity 0.2s ease;
    #     }

    #     .menu-ring.open {
    #     transform: scale(1);
    #     opacity: 1;
    #     pointer-events: auto;
    #     }

    #     /* Menu items arranged in a circle */
    #     .menu-item {
    #     --angle: calc(var(--i) * (360deg / var(--total)) - 90deg);

    #     background: var(--st-background-color);
    #     position: absolute;
    #     top: 50%;
    #     left: 50%;
    #     margin: calc(var(--item-size) / -2);   /* otomatis setengah ukuran item */
    #     transform: rotate(var(--angle)) translate(var(--radius))
    #         rotate(calc(-1 * var(--angle)));
    #     }

    #     .menu-item:hover {
    #     transform: rotate(var(--angle)) translate(var(--radius))
    #         rotate(calc(-1 * var(--angle))) scale(1.15);
    #     border-color: var(--st-primary-color);
    #     background: var(--st-secondary-background-color);
    #     }

    #     .menu-item.selected {
    #     border-color: var(--st-primary-color);
    #     background: var(--st-secondary-background-color);
    #     }

    #     /* Backdrop when menu is open (must be outside .menu-overlay to avoid
    #     its transform creating a containing block for position: fixed) */
    #     .menu-backdrop {
    #     display: none;
    #     position: fixed;
    #     inset: 0;
    #     background: var(--st-background-color);
    #     opacity: 0;
    #     transition: opacity 0.3s ease;
    #     z-index: 99;
    #     }

    #     .menu-backdrop.open {
    #     display: block;
    #     opacity: 0.7;
    #     }

    #     /* Center decoration */
    #     .menu-ring::after {
    #     content: "";
    #     position: absolute;
    #     top: 50%;
    #     left: 50%;
    #     width: 1.5rem;
    #     height: 1.5rem;
    #     transform: translate(-50%, -50%);
    #     border-radius: 50%;
    #     background: var(--st-secondary-background-color);
    #     border: 2px dashed var(--st-border-color);
    #     opacity: 0.6;
    #     box-sizing: border-box;
    #     }
    #     '''

    #     js_test = '''
    #     export default function ({ parentElement, data, setStateValue }) {
    #     const selector = parentElement.querySelector("#selector");
    #     const selectorIcon = parentElement.querySelector("#selector-icon");
    #     const overlay = parentElement.querySelector("#overlay");
    #     const backdrop = parentElement.querySelector("#backdrop");
    #     const ring = parentElement.querySelector("#ring");

    #     let isOpen = false;
    #     const options = data?.options || {};
    #     let currentSelection = data?.selection || Object.keys(options)[0];
    #     const optionCount = Object.keys(options).length;

    #     // Set total item count for CSS angle calculation
    #     ring.style.setProperty("--total", optionCount);
    #     ring.style.setProperty("--steps", Math.max(optionCount - 1, 1)); 

    #     // Create the menu items from options
    #     Object.entries(options).forEach(([value, icon], index) => {
    #         const button = document.createElement("button");
    #         button.className = "menu-item";
    #         button.dataset.value = value;
    #         button.style.setProperty("--i", index);
    #         button.textContent = icon;

    #         button.onclick = () => {
    #         currentSelection = value;
    #         updateDisplay();
    #         toggleMenu();
    #         setStateValue("selection", currentSelection);
    #         };

    #         ring.appendChild(button);
    #     });
        
    #     // Update the selector icon and highlight selected item
    #     function updateDisplay() {
    #         selectorIcon.textContent = options[currentSelection] || "?";

    #         ring.querySelectorAll(".menu-item").forEach((item) => {
    #         item.classList.toggle(
    #             "selected",
    #             item.dataset.value === currentSelection,
    #         );
    #         });
    #     }

    #     // Calculate and apply viewport-safe position for the menu
    #     function updatePosition() {
    #         const selectorRect = selector.getBoundingClientRect();
    #         const menuRadius = ring.offsetWidth / 2;
    #         const toolbarHeight = 60; // Streamlit toolbar height

    #         // Center of selector in viewport
    #         const centerX = selectorRect.left + selectorRect.width / 2;
    #         const centerY = selectorRect.top + selectorRect.height / 2;

    #         // Calculate overflow on each side (account for toolbar at top)
    #         const overflowLeft = menuRadius - centerX;
    #         const overflowRight = centerX + menuRadius - window.innerWidth;
    #         const overflowTop = menuRadius - (centerY - toolbarHeight);
    #         const overflowBottom = centerY + menuRadius - window.innerHeight;

    #         // Apply offset to keep menu in viewport
    #         const offsetX = Math.max(0, overflowLeft) - Math.max(0, overflowRight);
    #         const offsetY = Math.max(0, overflowTop) - Math.max(0, overflowBottom);

    #         overlay.style.transform = `translate(calc(-50% + ${offsetX}px), calc(-50% + ${offsetY}px))`;
    #     }

    #     // Debounced resize handler for performance
    #     let resizeTimeout;
    #     function handleResize() {
    #         clearTimeout(resizeTimeout);
    #         resizeTimeout = setTimeout(updatePosition, 16); // ~60fps
    #     }

    #     // Toggle menu open/closed
    #     function toggleMenu() {
    #         isOpen = !isOpen;
    #         backdrop.classList.toggle("open", isOpen);
    #         overlay.classList.toggle("open", isOpen);
    #         ring.classList.toggle("open", isOpen);

    #         if (isOpen) {
    #         updatePosition();
    #         window.addEventListener("resize", handleResize);
    #         } else {
    #         window.removeEventListener("resize", handleResize);
    #         clearTimeout(resizeTimeout);
    #         // Reset position after close animation completes (400ms matches CSS transition)
    #         setTimeout(() => {
    #             if (!isOpen) overlay.style.transform = "";
    #         }, 400);
    #         }
    #     }

    #     // Initialize display
    #     updateDisplay();

    #     // Attach click handlers
    #     selector.onclick = toggleMenu;
    #     backdrop.onclick = () => toggleMenu();

    #     // Cleanup function
    #     return () => {
    #         clearTimeout(resizeTimeout);
    #         window.removeEventListener("resize", handleResize);
    #     };
    #     }
    #     '''

    #     radial_menu = st.components.v2.component(
    #         name="radial_menu",
    #         html=html_test,
    #         css=css_test,
    #         js=js_test,
    #     )

    #     st.header("Radial Menu Component")

    #     st.write("Click the button to open the menu. Select your favorite food!")

    #     options = {
    #         "Not Watched": "❌",
    #         "Watched": "✅",
    #         "Great": "🆗",
    #         "Goat": "🐐",
    #     }

    #     with st.container(horizontal=True, horizontal_alignment='center'):
    #         st.write('asad')
    #         result = radial_menu(
    #             data={"options": options, "selection": "Not Watched"},
    #             default={"selection": "Not Watched"},
    #             on_selection_change=lambda: None,
    #             key="food_menu",
    #         )

    #     if result.selection:
    #         icon = options.get(result.selection, "")
    #         st.write(f"You selected: **{icon} {result.selection.title()}**")

    # if st.button('dwakod'):
    #     tedsadw()
    # if st.button('rerun'):
    #     st.rerun()



    balance_tabs, transfer_tabs = st.tabs(['Balance Services', 'Interbank Transfer'])
    with balance_tabs:
        st.subheader('Balance Service')
        st.divider()
        disburse('3.1','Negative','Any Services', 'Access Token Invalid', '401xx01', 'Access Token Invalid', ['invalid', 'token'])
        st.divider()
        disburse('3.2','Negative','Any Services', 'Unauthorized . Signature', '401xx00', 'Unauthorized Signature', ['unauthorized'])
        st.divider()
        disburse('3.3','Negative','Any Services', 'Missing Mandatory Field {} …, etc', '400xx02', 'Invalid Mandatory Field {........}', ['invalid', 'mandatory', 'field'])
        st.divider()
        disburse('3.4','Negative','Any Services', 'Invalid Field Format {} .., etc', '400xx01', 'Invalid Field Format {........}', ['invalid', 'field', 'format'])
        st.divider()
        disburse('3.5','Negative','Any Services', 'Cannot use the same X-EXTERNAL-ID', '409xx00', 'Conflict', ['conflict'])
        st.divider()
        disburse('3.6','Positive','Balance Inquiry', 'Inquiry Saldo Utama (IDR and/or USD, etc) (termasuk saldo lainnya)', '2001100', 'Successful', ['successful'])
        st.divider()

    with transfer_tabs:
        st.subheader('Transfer Inquiry')
        st.divider()
        disburse('8.1','Negative','Any Services', 'Access Token Invalid', '401xx01', 'Access Token Invalid', ['invalid', 'token'])
        st.divider()
        disburse('8.2','Negative','Any Services', 'Unauthorized . Signature', '401xx00', 'Unauthorized Signature', ['unauthorized'])
        st.divider()
        disburse('8.3','Negative','Any Services', 'Missing Mandatory Field {} …, etc', '400xx02', 'Invalid Mandatory Field {........}', ['invalid', 'mandatory', 'field'])
        st.divider()
        disburse('8.4','Negative','Any Services', 'Invalid Field Format {} …, etc', '400xx01', 'Invalid Field Format {........}', ['invalid', 'field', 'format'])
        st.divider()
        disburse('8.5','Negative','Any Services', 'Cannot use the same X-EXTERNAL-ID', '409xx00', 'Conflict', ['conflict'])
        st.divider()
        disburse('8.7','Positive','Eksternal Account Inquiry', 'Inquiry Account via Switching X, with bank code', '2001600', 'Successful', ['successful'])
        st.divider()
        disburse('8.10','Positive','Interbank Trigger Transfer', 'Transfer to Account via Switching X, with bank code', '2001800', 'Successful', ['successful'])
        st.divider()
        disburse('8.11','Negative','Interbank Trigger Transfer', 'Insufficient Fund/Saldo tidak cukup', '4031814', 'Insufficient Fund', ['insufficient', 'funds'])
        st.divider()
        disburse('8.12','Negative','Interbank Trigger Transfer', 'Duplicate Customer Reference Number', '4091801', 'Duplicate Customer Reference Number', ['duplicate', 'partnerreferenceno'])
        st.divider()
        disburse('8.13','Positive','Transaction Status Inquiry', 'Inquiry Status atas transaksi Interbank Transfer berhasil\\\nField "serviceCode" diisi dengan value "18"\\\nField "latestTransactionStatus" diisi dengan value "00"', '2003600', 'Successful', ['successful'])
        st.divider()