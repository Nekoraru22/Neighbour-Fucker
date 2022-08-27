# Neighbour-Fucker
Screw your neighbor in the smartest way. Give his phone number to the GPT-3 AI and enjoy watching him talk to strangers posing as a girl and broadcasting the number.

# How to use
The script initiates conversations and sends your neighbor's number. It also stores the images sent by strangers in `strangerPics` and the conversations in `conversations`.

- Create an account on https://openai.com/api/, get your api key and insert it into
```py
__API_KEY__ = "key" # main.py
```
- Edit the first bot message
```py
FIRST_MESSAGE = "Hi, F 21" # main.py
```
- Edit `IA/prompt` to tailor AI to your liking.
- Start `main.py`
- Add a few images of a person in `images` (For legal reasons I must advise you that you must have a consent for this).
<br><br>

# Remembering
You can replay the saved conversations by starting the `viewer.py` script

If you have an account on the site you can add your user name so that the viewer can detect who you are.

```py
__NAME__ = "Valeria2001" # IA/mainAI.py
```

# Problems :(
Currently the site has fixed the captcha and requires manual verification every 20 minutes or so, perhaps in the future I will add a captcha solver.
