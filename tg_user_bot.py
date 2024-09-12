from pyrogram import Client
import asyncio, time, json

ID = '@EducationBoard_bot'
BOARD = 'যশোর'
YEAR = 2019
# with open('rolls.json') as f: ROLLS = json.loads(f.read())

ROLLS = range(100000, 999999 + 1)

api_id = '21274686'
api_hash = '624016c8a4317bb5821f71e276036bf3'
output_file = f'SSC_Result_{int(time.time())}.json'
with open(output_file, 'w') as f: pass

app = Client("user_session", api_id=api_id, api_hash=api_hash)

def append_result(result:dict):
    with open(output_file) as f: d = f.read()
    try: d = json.loads(d)
    except json.JSONDecodeError: d = []
    d.append(result)
    with open(output_file, 'w') as f: f.write(json.dumps(d, indent=4))

class string(str): pass

async def click_message_button(msg, btn_text):
    inline_button = None
    for row in msg.reply_markup.inline_keyboard:
        for button in row:
            if btn_text in button.text: inline_button = button
            if inline_button: break
        if inline_button: break
    return await app.request_callback_answer(msg.chat.id, msg.id, inline_button.callback_data)

async def receive_message(last_msg=None):
    if not last_msg:
        async for msg in app.get_chat_history(ID, limit=1):
            last_msg = msg

    required_text = ["কোন বোর্ডের পরীক্ষার্থী", "কত সালের পরীক্ষার্থী", "পরীক্ষার রোল নম্বর", "রেজাল্ট বের করা", "Exam: SSC", "আপনার দেয়া তথ্য সঠিক নয়"]

    while True:
        all_msg = []
        async for msg in app.get_chat_history(ID, limit=5): all_msg.append(msg)
        all_msg.reverse()
        for msg in all_msg:
            if msg.id > last_msg.id:
                if True in [ t in msg.text for t in required_text ]:
                    return msg
            await asyncio.sleep(1)

async def get_result(roll:int, from_self:bool=False):
    M1 = await app.send_message(ID, '↪️ Get Education Result 🔀')
    M2 = await receive_message(M1)
    await click_message_button(M2, BOARD)
    await receive_message(M2)
    M3 = await app.send_message(ID, str(YEAR))
    M4 = await receive_message(M3)
    M5 = await app.send_message(ID, str(roll))
    M6 = await receive_message(M5)
    M7 = await receive_message(M6)
    result_text = M7.text
    if "আপনার দেয়া তথ্য সঠিক নয়" in result_text:
        if from_self: return None
        else: return await get_result(roll, True)
    atob = {'নাম:': 'Name:', 'Fathername:': 'Father:', 'Mothername:': 'Mother:', 'Dob:': 'DOB:', 'Gpa:': 'GPA:', 'Eiin:': 'EIIN:'}
    for k, v in atob.items(): result_text = string(result_text.replace(k, v))
    result_text.json = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in result_text.strip().split('\n')}
    for k, v in result_text.json.items():
        try: result_text.json[k] = int(v)
        except:
            try: result_text.json[k] = float(v)
            except: pass
    return result_text

async def main():
    await app.start()
    nec = 0 # Non Exists Count
    for roll in ROLLS:
        if nec > 10:
            print(f'Assuming end of students after 10 rolls not being existed. Skipping from {roll} to {ROLLS[-1]}', flush=True)
            break
        while 1:
            print(f'Trying to get result for Roll: {roll}', flush=True)
            try: result = await asyncio.wait_for(get_result(roll), 60)
            except: continue
            if result:
                nec = 0
                append_result(result.json)
                print(f'Got Result! Roll: {result.json.get("Roll")} Name: {result.json.get("Name")}', flush=True)
            else:
                nec += 1
                print(f'Result for Roll: {roll} does not exists!', flush=True)
            break
    await app.stop()


app.run(main())

