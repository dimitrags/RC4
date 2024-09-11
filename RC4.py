#Dictionary που αντιστοιχίζει γράμμα με δυαδικό νούμερο
dictionary={"A": "00000", "B": "00001", "C": "00010", "D": "00011", "E": "00100", "F": "00101", "G": "00110", "H": "00111",
                   "I": "01000", "J": "01001", "K": "01010", "L": "01011", "M": "01100", "N": "01101", "O": "01110", "P": "01111",
                   "Q": "10000", "R": "10001", "S": "10010", "T": "10011", "U": "10100", "V": "10101", "W": "10110", "X": "10111",
                   "Y": "11000", "Z": "11001", ".": "11010", "!": "11011", "?": "11100", "(": "11101", ")": "11110", "-": "11111"}

def dec_to_bin(dec, size): #Με τη zfill προσθέτω όσα μηδενικά χρειάζονται για να έχω το επιθυμητό size
    bin_num=bin(dec)[2:].zfill(size)  
    return bin_num

def bin_to_dec(bin_number): #Δυαδικό σε δεκαδικό
    decimal=int(bin_number,2)
    return decimal

def xor(a,b): #Δέχεται 2 binary strings
    if len(a)!=len(b):
        print('Sizes arent the same!')
        return False
    else:
        result=''
        for i in range(len(a)):
            temp=int(a[i])^int(b[i]) #Πράξη xor ένα ένα bit 2 strings a, b
            result+=str(temp) #Επιστρέφει το αποτέλεσμα σε binary string
        return result

def findvalue(word):
    for d in dictionary:   #Διαπερνώ όλους τους χαρακτήρες του dictionary, 
        if word==d:          #Ελέγχω αν ο χαρακτήρας του dictionary είναι ίσος με τον χαρακτήρα του μηνύματος
            value=dictionary[d] #Επιστρέφω την δυαδική τιμή του
            break
        else:
            value=-1
    return value #Δεκαδικός
    
plaintext='MISTAKESAREASSERIOUSASTHERESULTSTHEYCAUSE'
seed='HOUSE'
#Κατασκευή μετάθεσης S
repeated_seed=[] #Επναναλαμβανόμενο seed
seedlength=len(seed)
S=[i for i in range(256)] #Δημιουργία πίνακα όπου S[i]=i
for i in range(256): #Επαναλαμβάνεται το seed συνεχόμενα για να έχουμε 256 χαρακτήρες
    repeated_seed.append(seed[i%seedlength]) #mod seenlength έτσι ώστε να επαναλαμβάνεται συνέχεια το αρχικό seed 
                                             #και να μη φεύγει το i από τα όρια
j=0
for i in range(256):   #Η findvalue δίνει την τιμή του γράμματος σε binary και την μετατρέπω σε δεκαδικό για να γίνει πράξη
    j=((j+S[i]+bin_to_dec(findvalue(repeated_seed[i%seedlength])))%256) 
    S[i], S[j]= S[j], S[i]
print('S is: ')
print(S)

#Κλειδοροή του RC4
i=0
j=0
plen=len(plaintext)
K=[]
while plen>0:
    i=(i+1)%256
    j=(j+S[i])%256
    S[i], S[j]= S[j], S[i]
    K.append(S[(S[i]+S[j])%256])
    plen-=1
print('Key is:') 
print(K)

#encryption
encrypted_message=''
fullbinaryK=''
for i in range(len(plaintext)): #Διαπερνώ όλους τους χαρακτήρες
    for j in range(8):          #Για 8 bit σε δυαδική μορφή του κάθε χαρακτήρα
        bin_plaintext=(findvalue(plaintext[i])).zfill(8) #Μετατρέπω το 5bit νούμερο σε 8bit προσθέτοντας μηδενικά με τη zfill() 
        bin_K=dec_to_bin((int(K[i])),8) #Μετατρέπω τη δεκαδική τιμή του Κ σε δυαδική 8 bit
        temp=int(bin_plaintext[j])^int(bin_K[j]) #Κάνω XOR ένα ένα τα bit του μηνύματος με του κλειδιού
        encrypted_message+=str(temp) #Προσθέτω το αποτέλεσμα στο τελικό string
        fullbinaryK+=bin_K[j]    #fullbinaryK είναι το κλειδί σε binary μορφή
        
print("The encrypted message in binary form is: "+ encrypted_message)

#encrypted message printing
this_char=''
encr_msg_to_print=''
count=1
for i in range(int(len(encrypted_message))): 
    count+=1
    this_char+=encrypted_message[i]
    if count>8:   #Έχω βρει έναν χαρακτήρα (αντιστοιχεί σε 8 bit)
        this_char=this_char[3:]   #Τα 3 πρώτα ψηφία δεν τα χρειαζόμαστε, προέκυψαν από την αύξηση του 5bit νούμερου
        for d in dictionary:    #Διασχίζω το dictionary
            if dictionary[d]==this_char:   #Βρίσκω το αντίστοιχο γράμμα του δυαδικού 5ψήφιου
                encr_msg_to_print+=d    #Το προσθέτω στο τελικό encrypted μήνυμα
        count=1
        this_char=''
print('The encrypted message is: ' +encr_msg_to_print)
                
#decryption
count=1
current_character=''
decrypted_message=''
for i in range(int(len(encrypted_message))): 
    temp=int(encrypted_message[i])^int(fullbinaryK[i]) #Πράξη xor ένα ένα τα bits του κρυπτογραφημένου με το κλειδί
    current_character+=str(temp)
    count+=1
    if count>8:  #Έχω βρει έναν χαρακτήρα (αντιστοιχεί σε 8 bit)
        current_character=current_character[3:]#Τα 3 πρώτα ψηφία δεν τα χρειαζόμαστε, προέκυψαν από την αύξηση του 5bit νούμερου
        for d in dictionary: #Διασχίζω το dictionary
            if dictionary[d]==current_character: #Βρίσκω το αντίστοιχο γράμμα του δυαδικού 5ψήφιου
                decrypted_message+=d #Το προσθέτω στο τελικό decrypted μήνυμα
        temp=0          
        count=1
        current_character=''
        
print("The decrypted message is: "+ decrypted_message)