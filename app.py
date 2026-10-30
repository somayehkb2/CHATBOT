import streamlit as st
import utils

# prompt = st.chat_input('Enter your prompt')
# if prompt:
#     st.write(f'prompt: {prompt}')

# st.chat_message('ai').write('How can I help you')
# st.chat_message('user').write('tell me about food')
# #role --> ai / user
# #content --> message

# st.write(st.session_state)
# if 'count' not in st.session_state:
#     st.session_state['count']=0

# #count = 0

# if st.button('ADD'):
#     st.session_state['count'] = st.session_state['count'] + 1 
#     st.write(f'count: {st.session_state['count']}')

# import time
# with st.spinner('Generating...'):
#     time.sleep(3)

import streamlit as st
import utils

st.title('STREAMLIT CHATBOT')


if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role': 'ai', 'content': 'How Can I Help You?'}]

if 'stop_requested' not in st.session_state:
    st.session_state['stop_requested'] = False

model = 'gemma3:1b'

col1, col2, col3 = st.columns(3)

with col1:
    stop_btn = st.button('توقف مدل', use_container_width=True)

with col2:
    clear_btn = st.button('پاک کردن تاریخچه', use_container_width=True)

with col3:
    summary_btn = st.button('خلاصه و ذخیره چت', use_container_width=True)


if stop_btn:
    st.session_state['stop_requested'] = True
    st.warning('درخواست توقف ثبت شد. تا پایان پاسخ فعلی صبر کنید...')


if clear_btn:
    st.session_state['messages'] = [{'role': 'ai', 'content': 'How Can I Help You?'}]
    st.session_state['stop_requested'] = False
    st.success('تاریخچه پاک شد.')
    st.rerun()


for msg in st.session_state['messages']:
    st.chat_message(msg['role']).write(msg['content'])


prompt = st.chat_input('Enter Your Question')

if prompt and not st.session_state['stop_requested']:
    new_prompt = prompt + ' Describe your answer with detail and images'

    st.chat_message('user').write(prompt)
    st.session_state['messages'].append({'role': 'user', 'content': prompt})

    with st.spinner('Generating Response...'):
        response = utils.call_ollama_model(new_prompt, model)

   
    if st.session_state['stop_requested']:
        st.info('پاسخ لغو شد.')
        st.session_state['stop_requested'] = False
    else:
        st.chat_message('ai').write(response)
        st.session_state['messages'].append({'role': 'ai', 'content': response})


if summary_btn:
    
    full_chat = ""
    for msg in st.session_state['messages']:
        role_name = 'کاربر' if msg['role'] == 'user' else 'دستیار'
        full_chat += f"{role_name}: {msg['content']}\n\n"

    
    with open('chat_history.txt', 'w', encoding='utf-8') as f:
        f.write(full_chat)
    st.success('کل چت در فایل chat_history.txt ذخیره شد.')

    
    summary_prompt = f"""You are a professional summarizer.
Summarize the following conversation in Persian (Farsi) in a clear and structured way.
Include these sections:
1. موضوع اصلی گفتگو
2. نکات کلیدی مطرح‌شده
3. نتیجه‌گیری نهایی
Keep it concise but complete.

Conversation:
\"\"\"
{full_chat}
\"\"\"

Summary (in Persian):"""

    with st.spinner('در حال خلاصه‌سازی چت...'):
        summary = utils.call_ollama_model(summary_prompt, model)

   
    with open('chat_summary.txt', 'w', encoding='utf-8') as f:
        f.write("=== خلاصه گفتگو ===\n\n")
        f.write(summary)

    st.success('خلاصه چت در فایل chat_summary.txt ذخیره شد.')
    st.subheader('خلاصه چت')
    st.write(summary)