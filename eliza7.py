import re
import dbm
import random
import datetime

from flask import Flask, request,session
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse
from callers import callers


# program name = eliza8.py october 21
# added dbm logic
 
reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}
 
psychobabble = [
    [r'I need (.*)',
     ["Why do you need {0}?",
      "Would it really help you to get {0}?",
      "Are you sure you need {0}?"]],
 
    [r'Why don\'?t you ([^\?]*)\??',
     ["Do you really think I don't {0}?",
      "Perhaps eventually I will {0}.",
      "Do you really want me to {0}?"]],
 
    [r'Why can\'?t I ([^\?]*)\??',
     ["Do you think you should be able to {0}?",
      "If you could {0}, what would you do?",
      "I don't know -- why can't you {0}?",
      "Have you really tried?"]],
 
    [r'I can\'?t (.*)',
     ["How do you know you can't {0}?",
      "Perhaps you could {0} if you tried.",
      "What would it take for you to {0}?"]],
 
    [r'I am (.*)',
     ["Did you come to me because you are {0}?",
      "How long have you been {0}?",
      "OK so why do you think that you have you been {0}?",
      "How do you feel about being {0}?"]],
 
    [r'I\'?m (.*)',
     ["How does being {0} make you feel?",
      "Do you enjoy being {0}?",
      "Why do you tell me you're {0}?",
      "Why do you think you're {0}?"]],
 
    [r'Are you ([^\?]*)\??',
     ["Why does it matter whether I am {0}?",
      "Would you prefer it if I were not {0}?",
      "Perhaps you believe I am {0}.",
      "I may be {0} -- what do you think?"]],
 
    [r'What (.*)',
     ["Why do you ask?",
      "How would an answer to that help you?",
      "What do you think?"]],
 
    [r'How (.*)',
     ["How do you suppose?",
      "Perhaps you can answer your own question.",
      "What is it you're really asking?"]],
 
    [r'Because (.*)',
     ["Is that the real reason?",
      "What other reasons come to mind?",
      "Does that reason apply to anything else?",
      "If {0}, what else must be true?"]],
 
    [r'(.*) sorry (.*)',
     ["There are many times when no apology is needed.",
      "What feelings do you have when you apologize?"]],
 
    [r'Hello(.*)',
     ["Hello... I'm glad you could drop by today.",
      "Hi there... how are you today?",
      "Hello, how are you feeling today?"]],
 
    [r'I think (.*)',
     ["Do you doubt {0}?",
      "Do you really think so?",
      "But you're not sure {0}?"]],
 
    [r'(.*) friend (.*)',
     ["Tell me more about your friends.",
      "When you think of a friend, what comes to mind?",
      "Why don't you tell me about a childhood friend?"]],
 
    [r'Yes',
     ["You seem quite sure.",
      "OK, but can you elaborate a bit?"]],
 
    [r'(.*) computer(.*)',
     ["Are you really talking about me?",
      "Does it seem strange to talk to a computer?",
      "How do computers make you feel?",
      "Do you feel threatened by computers?"]],
 
    [r'Is it (.*)',
     ["Do you think it is {0}?",
      "Perhaps it's {0} -- what do you think?",
      "If it were {0}, what would you do?",
      "It could well be that {0}."]],
 
    [r'It is (.*)',
     ["You seem very certain.",
      "If I told you that it probably isn't {0}, what would you feel?"]],
 
    [r'Can you ([^\?]*)\??',
     ["What makes you think I can't {0}?",
      "If I could {0}, then what?",
      "Why do you ask if I can {0}?"]],
 
    [r'Can I ([^\?]*)\??',
     ["Perhaps you don't want to {0}.",
      "Do you want to be able to {0}?",
      "If you could {0}, would you?"]],
 
    [r'You are (.*)',
     ["Why do you think I am {0}?",
      "Does it please you to think that I'm {0}?",
      "Perhaps you would like me to be {0}.",
      "Perhaps you're really talking about yourself?"]],
 
    [r'You\'?re (.*)',
     ["Why do you say I am {0}?",
      "Why do you think I am {0}?",
      "Are we talking about you, or me?"]],
 
    [r'I don\'?t (.*)',
     ["Don't you really {0}?",
      "Why don't you {0}?",
      "Do you want to {0}?"]],
 
    [r'I feel (.*)',
     ["Good, tell me more about these feelings.",
      "Do you often feel {0}?",
      "OK why is that you feel  {0}?",
      "When do you usually feel {0}?",
      "When you feel {0}, what do you do?"]],
 
    [r'I have (.*)',
     ["Why do you tell me that you've {0}?",
      "Have you really {0}?",
      "Now that you have {0}, what will you do next?"]],
 
    [r'I would (.*)',
     ["Could you explain why you would {0}?",
      "Why would you {0}?",
      "Who else knows that you would {0}?"]],
 
    [r'Is there (.*)',
     ["Do you think there is {0}?",
      "It's likely that there is {0}.",
      "Would you like there to be {0}?"]],
 
    [r'My (.*)',
     ["I see, your {0}.",
      "Why do you say that your {0}?",
      "When your {0}, how do you feel?"]],
 
    [r'You (.*)',
     ["We should be discussing you, not me.",
      "Why do you say that about me?",
      "Why do you care whether I {0}?"]],
 
    [r'Why (.*)',
     ["Why don't you tell me the reason why {0}?",
      "Why do you think {0}?"]],
 
    [r'I want (.*)',
     ["What would it mean to you if you got {0}?",
      "Why do you want {0}?",
      "What would you do if you got {0}?",
      "If you got {0}, then what would you do?"]],
 
    [r'(.*) mother(.*)',
     ["Tell me more about your mother.",
      "What was your relationship with your mother like?",
      "How do you feel about your mother?",
      "How does this relate to your feelings today?",
      "Good family relations are important."]],
 
    [r'(.*) father(.*)',
     ["Tell me more about your father.",
      "How did your father make you feel?",
      "How do you feel about your father?",
      "Does your relationship with your father relate to your feelings today?",
      "Do you have trouble showing affection with your family?"]],
 
    [r'(.*) child(.*)',
     ["Did you have close friends as a child?",
      "What is your favorite childhood memory?",
      "Do you remember any dreams or nightmares from childhood?",
      "Did the other children sometimes tease you?",
      "How do you think your childhood experiences relate to your feelings today?"]],
 
    [r'(.*)\?',
     ["Why do you ask that?",
      "Please consider whether you can answer your own question.",
      "Perhaps the answer lies within yourself?",
      "Why don't you tell me?"]],
 
    [r'quit',
     ["Thank you for talking with me.",
      "Good-bye.",
      "Thank you,   Have a good day!"]],
    
    [ r'suicide',
     ["hmmm.. please consider visiting  https://suicidepreventionlifeline.org ; or tell me how you feel right now.",
      ]] ,

    [r'depressed',
     ["hmmm.. please consider visiting  https://samaritiansnyc.org ; or tell me how you feel right now.",
      ]] , 

    [r'gambling',
     ["hmmm.. please consider visiting  https://samaritiansnyc.org ; or tell me how you feel right now.",
      ]] , 
    [r'(.*)',
     ["Please tell me more.",
      "Let's change focus a bit... Tell me about your family.",
      "Can you elaborate on that?",
      "Why do you say that: {0}?",
      "I see.",
      "Very interesting.Please tell me more!",
      "{0}?",
      "I see.  And what does that tell you?",
      "How does that make you feel?",
      "How do you feel when you say that?"]]
]


SECRET_KEY  = 'a secret key'
app  = Flask(__name__)
app.config.from_object(__name__)
# program name = eliza7

@app.route("/sms", methods=['POST'])
 
def main():


   counter = session.get('counter', 0)
   counter += 1
   session['counter'] = counter

   resp = MessagingResponse()
   
   phone_number = request.form['From']
   phone_number = phone_number[1:]
   
   body = request.form['Body']

   try:
         
      db = dbm.open('elizadatabase', 'r')
      print ( db[phone_number])
      print ( ' phone number is in databse')
                   
      first_name = db[phone_number]   
      first_name = first_name.decode('ASCII')
      print ( " first name is " , first_name)
      new_client = False
      db.close
    
   except:
      db = dbm.open('elizadatabase', 'w')
      db[phone_number] = body
        
      print (phone_number, "  added to  the database")
      first_name = db[phone_number]
      first_name = first_name.decode('ASCII')
      new_client = True
      db.close


   
   bodyfirst  = session.get('bodyfirst', 0)
   print ( 'body first = ' , bodyfirst)
   
   body = request.form['Body']

   if  profanity(body):
       respmsg  =  str(first_name) + " I do not speak to people who use profanity ; I am ending our session; please take a timeout and start over later. Send me HI when you ready "
       print (' body is in profane  in main program')
       resp.message(respmsg)
       db.close
       session.clear() 
       return str(resp)
   if bodyfirst == body :       
      print ( ' duplicate message')
      session['bodyfirst'] = body
      respmsg  =  str(first_name)  +  " ,I am sorry you seem to be repeating yourself .. I an ending our session for now! Please take a time out and start over later. Send me HI when you are ready!"
      db.close
      resp.message(respmsg)
      session.clear() 
      return str(resp)

   session['bodyfirst'] = body
 
 
   
   print  (  'phone number' , phone_number , 'body' , body)
   print (' session count',session['counter'])
   if session['counter'] == 1 :
         respmsg1  =       str(first_name) + " , Welcome back for another session \n I missed you!"
         respmsg3 =""
         print ("Hello. How are you feeling today?")
         if (new_client == True)  :
            respmsg1  = saydisclose()
            respmsg3  = saymenu()
            
         respmsg2  =  "\n Let us begin: \n How are you feeling?"
 
         respmsg =  str( respmsg1) + str(respmsg3)  + str(respmsg2)
         resp.message(respmsg)
         
         return str(resp)



          
   else: 
        print ( "session > 1")
     
        statement = body
        blank    = ', '
        
        respmsg =  str(first_name) + str(blank)  + (analyze(statement))
        resp.message(respmsg)
        return str(resp)
        
def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)
 
 
def saydisclose():


  
     print ( ' ')
     my_msg1 = '\n My name is Eliza. I am a simulated Rogerian Therapist \n It is indeed a pleasure meeting with you!'
     my_msg2 = ' I was originally created by Dr. Joseph Weisman of MIT' 
     my_msg2a = 'A few years ago Joe Strout  also of MIT of me create a python version of me. Evan Dempsey updated me. Mel Feuerman made a python version of me to run on Twillio!\n ' 
     my_msg3 = 'You can share your feelings in a safe non-judgemental,\n'
     my_msg4 = 'bully free environment. Using swear words is not permitted\n'
     my_msg5 = 'When sharing please start with "I" so we can more easily focus on your feelings: for example:\n '
     my_msg  =   my_msg1 +   my_msg2 + my_msg2a +   my_msg3 + my_msg4 + my_msg5

     resp =     str(my_msg)


     return  str(resp)

def saymenu():

 
    my_msg2 = '\n" I am really angry." \n' 
    my_msg2a = ' "I feel depressed." \n' 
    my_msg3 = ' "I am in a good mood!"'
    my_msg4 = ' \n "I have problems with my wife"'
    my_msg  =   my_msg2 + my_msg2a +   my_msg3  + my_msg4
              
    return  str(my_msg)

def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])
         
def profanity (body):
#    import badwords
      badwords = ['fuck','bitch','shit']
      profane  =  False
      print ( ' check for profanity' )
      print ( ' body = ' , body)
      tokens = body.lower().split()
      for i, token in enumerate(tokens):
         if token in badwords :
            print ( 'bad word' )
            profane = True
          
      return profane
 
   
 
if __name__ == "__main__":
    app.run(debug=True,port=4000)

