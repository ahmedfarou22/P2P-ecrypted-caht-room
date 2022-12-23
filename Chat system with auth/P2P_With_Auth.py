import socket,threading,time,random, math, random,json,hashlib, base64,string
from Crypto import Random
from Crypto.Cipher import AES

# for gui 
import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("End To End Encrypted - P2P Chat Room")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)##added 3

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1) ### made it 5 insted of 4
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="P2P Chat Room", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.string_input_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.Connect_to_peer, text="1. Connect to peer")
        self.string_input_button_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.extchangepublickeys, text= "2. Swap public keys")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.auth_by_signing,text="3. Auth by signature")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        
        self.string_input_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.agree_on_aes, text="4. Agree on AES key")
        self.string_input_button_4.grid(row=4, column=0, padx=20, pady=(10, 10))
        
        # self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        # self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 10))
        
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark","Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        # self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["100%","80%", "90%",  "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter your secret message")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(0, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),command=self.send_secret, text="Send")
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(0, 20), sticky="nsew")

        # create textbox above
        self.textbox_message = customtkinter.CTkTextbox(self, width=500,state="disabled")
        self.textbox_message.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # create textbox below
        self.textbox_log = customtkinter.CTkTextbox(self, width=500)
        self.textbox_log.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        


        # create radiobutton frame
        self.view_frame = customtkinter.CTkFrame(self)
        # self.view_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.view_frame.grid(row=0, column=3, rowspan=1,padx=(20, 20),pady=(20, 0), sticky="nsew")

        self.lable_for_space = customtkinter.CTkLabel(master=self.view_frame, text="View peer's properties", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.lable_for_space.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.view_button_1 = customtkinter.CTkButton(master=self.view_frame, command=self.view_peer_ip, text= "View peer's IP")
        self.view_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.view_button_2 = customtkinter.CTkButton(master=self.view_frame, command=self.view_peer_public_key, text= "View peer's public key")
        self.view_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.view_button_3 = customtkinter.CTkButton(master=self.view_frame, command=self.view_agreed_aes_key, text= "View agreed AES")
        self.view_button_3.grid(row=3, column=0, padx=20, pady=10)

        #grid down
        self.view_frame2 = customtkinter.CTkFrame(self)
        self.view_frame2.grid(row=1, column=3, rowspan=1,padx=(20, 20),pady=(20, 0), sticky="nsew")
        
        self.lable_for_space = customtkinter.CTkLabel(master=self.view_frame2, text="View my properties ", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.lable_for_space.grid(row=0, column=0, padx=20, pady=(20, 10))


        self.view_button_4 = customtkinter.CTkButton(master=self.view_frame2, command=self.view_my_ip, text= "View my IP")
        self.view_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.view_button_5 = customtkinter.CTkButton(master=self.view_frame2, command=self.view_my_rsa, text= "View my RSA keys")
        self.view_button_5.grid(row=5, column=0, padx=20, pady=10)

    def print_to_log(self,title,data):
        self.textbox_log.insert("end",str(title)+":  " + str(data)+"\n")

    def print_secret_message(self,message):
        self.textbox_message.configure(state="normal")
        self.textbox_message.insert("end",str(message)+"\n")
        self.textbox_message.configure(state="disabled")

    def Connect_to_peer(self):
        dialog = customtkinter.CTkInputDialog(text="Type the IP of peer:", title="Peer's IP?")
        ip_input = dialog.get_input()
        
        if ip_input == network.IP_LIST[0]:
            self.print_to_log("-->","Please enter an ip of a active node other than your node" )
            
        elif len(network.IP_LIST) > 1:
            self.print_to_log("-->","Already connected to a peer" )

        else:
            network.send_to_peer(ip_input,"connect")
            network.IP_LIST.append(ip_input)
            cryptoflags.connected = 1
            time.sleep(1) # Sleep for 1 seconds 

    def extchangepublickeys(self):
        if cryptoflags.connected == 0:
            self.print_to_log("-->","Please connect to a peer first" )

        
        else:
            try:
                network.send_to_block_chain("get_rsa_from_ip" + str(network.IP_LIST[1]))
                time.sleep(0.5)
                network.send_to_peer(str(network.IP_LIST[1]),str("get_my_rsa"))
            except:
                print("error sending to peer")

    def auth_by_signing(self):
        if cryptoflags.connected == 0:
            self.print_to_log("-->","please connect to a peer first" )

        elif cryptoflags.extchangepub == 0:
            self.print_to_log("-->","please send your public key first to extcahnge public keys" )
        
        else:
            signture = rsa.encrypt(rsa.private,"this_is_really_me")
            network.send_to_peer(str(network.IP_LIST[1]),[signture,"3_my_signture"])
            time.sleep(0.3)
            network.send_to_peer(str(network.IP_LIST[1]),"send_signture")

    def agree_on_aes(self):
        if cryptoflags.connected == 0:
            self.print_to_log("-->","please connect to a peer first" )

        elif cryptoflags.extchangepub == 0:
            self.print_to_log("-->","please send your public key first to extcahnge public keys" )

        elif cryptoflags.sign == 0:
            self.print_to_log("-->","please authenticate by signature first" )
        
        elif cryptoflags.aes_key_to_use != "":
            self.print_to_log("-->","AES already created press 10 to view it" )

        else:
            # autogenrate a random key to use with aes
            letters = string.ascii_lowercase
            randomkey = ''.join(random.choice(letters) for i in range(32))
            
            encrypted_eas = rsa.encrypt(cryptoflags.peer_public_key,randomkey)
            network.send_to_peer(network.IP_LIST[1],(encrypted_eas,str(hashlib.sha256(randomkey.encode()).digest()),"3_aes_to_use"))
            cryptoflags.aes_key_to_use = randomkey
            cryptoflags.useaes = 1



        

    def view_peer_ip(self):
        self.print_to_log("Peer's IP",network.IP_LIST[-1])
    
    def view_peer_public_key(self):
        self.print_to_log("Peer's public key",cryptoflags.peer_public_key)
    
    def view_agreed_aes_key(self):
        self.print_to_log("Peer's agreed AES key",cryptoflags.aes_key_to_use)

    def view_my_ip(self):
        self.print_to_log("My IP",network.IP_LIST[0])

    def view_my_rsa(self):
        self.print_to_log("My public key",rsa.public)
        self.print_to_log("My private key",rsa.private)

    def send_secret(self):
        if cryptoflags.connected == 0:
            self.print_to_log("-->","please connect to a peer" )

        elif cryptoflags.extchangepub == 0:
            self.print_to_log("-->","please send your public key to extcahnge public keys" )

        elif cryptoflags.sign == 0:
            self.print_to_log("-->","please authenticate my signature first" )
        
        elif cryptoflags.useaes == 0:
            self.print_to_log("-->","please send the EAS key to use" )
        
        else:
            message = self.entry.get()
            aes = AESCipher(cryptoflags.aes_key_to_use)
            encrypted_message_aes = aes.encrypt(message)
            tosend = encrypted_message_aes.decode()
            network.send_to_peer(network.IP_LIST[1],(tosend,str(hashlib.sha256(tosend.encode()).digest()),"4_secret"))
            self.print_secret_message("Me: "+ str(message))


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


class RSA:
    def __init__(self):
        self.p = self.genrate_prime()
        self.q = self.genrate_prime()
        self.public, self.private = self.generate_key_pair()# using the p and q used above
        print("-My public key is:", self.public, "\n-My private key is:", self.private)

    def genrate_prime(self):
        count = random.randint(1000000,1000000000) # the prime number will be betwwen a million and a billion
        
        while True:
            isprime = True
            
            for x in range(2, int(math.sqrt(count) + 1)):
                if count % x == 0: 
                    isprime = False
                    break
            
            if isprime:
                return count
            
            count += 1

    def gcd(self,a , b):
        while b != 0:
            a, b = b, a % b
        return a
    
    def multiplicative_inverse(self, e, phi):
        d = 0
        x1 = 0
        x2 = 1
        y1 = 1
        temp_phi = phi

        while e > 0:
            temp1 = temp_phi//e
            temp2 = temp_phi - temp1 * e
            temp_phi = e
            e = temp2

            x = x2 - temp1 * x1
            y = d - temp1 * y1

            x2 = x1
            x1 = x
            d = y1
            y1 = y

        if temp_phi == 1:
            return d + phi
    
    def generate_key_pair(self):
        # n = pq
        n = self.p * self.q

        # Phi is the totient of n
        phi = (self.p-1) * (self.q-1)

        # Choose an integer e such that e and phi(n) are coprime
        e = random.randrange(1, phi)

        # Use Euclid's Algorithm to verify that e and phi(n) are coprime
        g = self.gcd(e, phi)
        while g != 1:
            e = random.randrange(1, phi)
            g = self.gcd(e, phi)

        # Use Extended Euclid's Algorithm to generate the private key
        d = self.multiplicative_inverse(e, phi)

        # Return public and private key_pair Public key is (e, n) and private key is (d, n)
        return ((e, n), (d, n))

    def encrypt(self,key, plaintext):
        # Unpack the key into it's components
        key, n = key
        # Convert each letter in the plaintext to numbers based on the character using a^b mod m
        cipher = [pow(ord(char), key, n) for char in plaintext]
        # Return the array of bytes
        return cipher
        
    def decrypt(self,key, ciphertext):
        # Unpack the key into its components
        key, n = key
        # Generate the plaintext based on the ciphertext and key using a^b mod m
        aux = [str(pow(char, key, n)) for char in ciphertext]
        # Return the array of bytes as a string
        plain = [chr(int(char2)) for char2 in aux]
        return ''.join(plain)

class AESCipher(object):
    def __init__(self,key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class Network:
    def __init__(self) -> str:
        self.SOCKET_IP = self.__get_real_ip__()
        self.SOCKET_PORT = 222 # every server socket will use this port
        self.IP_LIST = [self.SOCKET_IP]


        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.SOCKET_IP,self.SOCKET_PORT))
        self.socket.listen()
        print("Successfully lisining on port 222..")

    def __get_real_ip__(self): 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # start a socket
        s.connect(("8.8.8.8", 80)) # connect the socket to google as an http request 
        real_ip = s.getsockname()[0] # save the given real ip in a var named real_ip
        s.close() # close the connection with google
        return real_ip # return the real ip
    
    def send_to_peer(self,peer_ip, data):
        try:
            peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer.connect((peer_ip,222))
            peer.send(json.dumps(data).encode())
            peer.close()
        
        except:
            print("error sending to peer")

    def send_to_block_chain(self,data):
        try:
            peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer.connect(("192.168.68.139",6666))    #### must be changeded
            peer.send(json.dumps(data).encode())
            peer.close()
        except:
            print("error sending to block chain")

class Cryptographyflags:
    def __init__(self):
        self.peer_public_key = []
        self.aes_key_to_use = ""
        
        self.connected = 0
        self.extchangepub = 0
        self.sign = 0
        self.useaes = 0

########################## start main objects ##########################


rsa = RSA() #rsa class
time.sleep(0.2)

app = App() # gui app

network = Network() # network class
cryptoflags = Cryptographyflags() # main flags class

app.print_to_log("Network","Successfully started and lisining on port 222..")
app.print_to_log("My Public key",rsa.public)
app.print_to_log("My Private key",rsa.private)
app.print_to_log("Block Chain","Successfully added new public RSA key to block chain")

network.send_to_block_chain([network.IP_LIST[0],str(socket.gethostname()),rsa.public,"my_ip_rsa_block"])
time.sleep(0.3)


################################# program starts here #################################

def receive():
    while True:
        peer, address = network.socket.accept()
        pperip, pperport = address
        decoded_somthing = peer.recv(1024).decode()
        
        receved = json.loads(decoded_somthing)
        print("-->just received\n",receved)
        app.print_to_log("Just received",receved )

        if type(receved) == str:
            if receved == "connect": # 1 connect to pper 
                network.IP_LIST.append(pperip)
                cryptoflags.connected = 1


            if receved[:8] == "peer_rsa": # 2 recive rsa from block chain  (extchange public keys)
                peers_rsa_s = receved[8:]
                peers_rsa_s = (peers_rsa_s.replace('[', ''))
                peers_rsa_s = (peers_rsa_s.replace(']', ''))
                peers_rsa_l = []
                
                temp = list(peers_rsa_s.split(","))
                
                for t in temp:
                    peers_rsa_l.append(int(t))
                cryptoflags.peer_public_key = peers_rsa_l
                cryptoflags.extchangepub = 1

            
            if receved[:10] == "get_my_rsa": # 2.2 get rsa from block chain  (extchange public keys)
                network.send_to_block_chain("get_rsa_from_ip" + str(network.IP_LIST[1]))
                cryptoflags.extchangepub = 1

            if receved == "send_signture":
                signture = rsa.encrypt(rsa.private,"this_is_really_me")
                network.send_to_peer(str(network.IP_LIST[1]),[signture,"3_my_signture"])


        if type(receved) == list:
            code = receved[len(receved)-1]
            
            if code == "3_my_signture": # verify signture
                signture = rsa.decrypt(cryptoflags.peer_public_key,receved[0])
                
                if signture == "this_is_really_me":
                    cryptoflags.sign = 1
                    app.print_to_log("-->","Authntication Successful")
                else:
                    app.print_to_log("Error","authntication Failed")

            
            if code == "3_aes_to_use": # 3  aes to use
                cryptoflags.aes_key_to_use = rsa.decrypt(rsa.private,receved[0])
                
                if receved[-2] == str(hashlib.sha256(cryptoflags.aes_key_to_use.encode()).digest()):
                    print(cryptoflags.aes_key_to_use)
                    cryptoflags.useaes = 1
                else:
                    print("the data was tapred with hash not equel")
                    app.print_to_log("Eroor","the data was tapred with hash not equel" )
            

            if code == "4_secret": # 4 recive secret message   
                if receved[-2] == str(hashlib.sha256(receved[0].encode()).digest()):
                    aes = AESCipher(cryptoflags.aes_key_to_use)
                    enc_temp = receved[0].encode()
                    message = aes.decrypt(enc_temp)
                    print("recived a secret message from peer:",message)
                    app.print_secret_message("Other: "+str(message))
                
                else:
                    print("the data was tapred with hash not equel")
                    app.print_to_log("Eroor","the data was tapred with hash not equel" )


def menu():
    while True:
        menu = "\nType auto --> Automate to start sending:\nType send --> send a message to peer:\nPress 1 --> Connect to peer:\nPress 2 --> Exchange public keys:\nPress 3 --> Agree on an AES key to use:\nPress a --> view peer's IP:\nPress b --> view peer's public key:\nPress c --> view agreed on AES key:\n"
        time.sleep(1)
        print(menu)
        command = input("What whould you like to do : ")

        if command == "auto": # automate the all steps
            if cryptoflags.connected == 1:
                print("Error: please continue manually")

            if cryptoflags.extchangepub == 1:
                print("Error: please continue manually")
            
            if cryptoflags.useaes == 1:
                print("Error: please continue manually")

            else:      
                ip_input = str(input("Please enter an Ip of a peer: "))
                
                if ip_input == network.IP_LIST[0]:
                    print("--> Please enter an ip of a active node other than your node")

                if len(network.IP_LIST) > 1:
                    print("Already connected to peer")

                else:
                    network.send_to_peer(ip_input,"connect") # sending connect 
                    network.IP_LIST.append(ip_input)
                    cryptoflags.connected = 1
                    time.sleep(0.5)
                    
                    network.send_to_peer(network.IP_LIST[1], (rsa.public,"1_my_public")) #sending public ip
                    cryptoflags.extchangepub = 1
                    time.sleep(0.5)

                    # autogenrate a random key to use with aes
                    letters = string.ascii_lowercase
                    randomkey = ''.join(random.choice(letters) for i in range(32))
                    print("Random string of length", 32, "is:", randomkey)
                    encrypted_eas = rsa.encrypt(cryptoflags.peer_public_key,randomkey)
                    network.send_to_peer(network.IP_LIST[1],(encrypted_eas,str(hashlib.sha256(randomkey.encode()).digest()),"3_aes_to_use"))
                    cryptoflags.aes_key_to_use = randomkey
                    cryptoflags.useaes = 1
                    time.sleep(0.5)
                    print("All done type send to start sending messages")
            
        if command == "1": # 1-connect
            ip_input = str(input("Please enter an Ip of a peer: "))
            if ip_input == network.IP_LIST[0]:
                print("--> Please enter an ip of a active node other than your node")
            
            if len(network.IP_LIST) > 1:
                print("Already connected to peer")

            else:
                network.send_to_peer(ip_input,"connect")
                network.IP_LIST.append(ip_input)
                cryptoflags.connected = 1
                print("connected succsesfully ")
                time.sleep(2) # Sleep for 2 seconds 

        if command == "2": # 2-extchange public keys
            if cryptoflags.connected == 0:
                print("Please connect to a peer first")
            
            else:
                network.send_to_peer(network.IP_LIST[1], (rsa.public,"1_my_public")) #sending public ip
                cryptoflags.extchangepub = 1

        if command == "3": # 3-send aes to use
            if cryptoflags.connected == 0:
                print("please connect to a peer first")

            if cryptoflags.extchangepub == 0:
                print("please send your public key first to extcahnge public keys")
            
            if cryptoflags.aes_key_to_use != "":
                print("AES already created press 10 to view it")

            else:
                # autogenrate a random key to use with aes
                letters = string.ascii_lowercase
                randomkey = ''.join(random.choice(letters) for i in range(32))
                print("Random string of length", 32, "is:", randomkey)
                
                encrypted_eas = rsa.encrypt(cryptoflags.peer_public_key,randomkey)
                network.send_to_peer(network.IP_LIST[1],(encrypted_eas,str(hashlib.sha256(randomkey.encode()).digest()),"3_aes_to_use"))
                cryptoflags.aes_key_to_use = randomkey
                cryptoflags.useaes = 1

        if command == "a": # view peer
            print(network.IP_LIST[-1])
        
        if command == "b": # view public key of peer
            print(cryptoflags.peer_public_key)
        
        if command == "c": # view aes to use
            print(cryptoflags.aes_key_to_use)

        if command == "send": # 4-send a message to peer
            if cryptoflags.connected == 0:
                print("please connect to a peer")

            if cryptoflags.extchangepub == 0:
                print("please send your public key to extcahnge public keys")
            
            if cryptoflags.useaes == 0:
                print("please send the EAS key to use")
            
            else:
                message = str(input("Please enter your secret message: "))
                aes = AESCipher(cryptoflags.aes_key_to_use)
                encrypted_message_aes = aes.encrypt(message)
                tosend = encrypted_message_aes.decode()
                network.send_to_peer(network.IP_LIST[1],(tosend,str(hashlib.sha256(tosend.encode()).digest()),"4_secret"))




# start threading in 2 functions and start the gui
receive_thread = threading.Thread(target=receive)
receive_thread.start()

menu_thread = threading.Thread(target=menu)
menu_thread.start()

app.mainloop()