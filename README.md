# TOC-Project-2018

Chatbot on Telegram

## Introduction
### Idea
The student usually confuses what to eat when the eating dining time is coming. So I thought that maybe we could design a chatbot to make some suggestion for us.
I design the easy chatbot to help me.

### Reference Restaurent
The referene restaurents I chose are my favorite stores around the NCKU. Maybe somebody would dislike the restaurent chosen by the chatbot.

### What Did the Chatbot Do
It will give the location of the restaurent, what to eat and some dishes' or restaurent's picture for you. 

### Interact
User can enter "breakfast", "lunch" and "dinner" to the chatbot in chinese. And it will show the message to guide you to continue.

### Run the Chatbot on Local
    
```
$ ./ngrok http 5000
$ python3 app.py
```
I had parsed the URL generated by `ngrok` to `parsed-https-URL/hook` in my `app.py` code.

### Platform
Telegram

## Finite State Machine
![FSM](https://github.com/rwe0214/TOC-project-2018/blob/master/img/show-fsm.png)

## Author
[rwe0214](https://github.com/rwe0214)
