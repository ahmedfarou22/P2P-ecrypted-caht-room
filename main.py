import socket,threading,time,random, math, random,json,hashlib, base64,string
from Crypto import Random
from Crypto.Cipher import AES

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

class Cryptographyflags:
    def __init__(self):
        self.peer_public_key = []
        self.aes_key_to_use = ""
        
        self.connected = 0
        self.extchangepub = 0
        self.useaes = 0

########################## start main objects ##########################
rsa = RSA()
time.sleep(0.5)

network = Network()
cryptoflags = Cryptographyflags()

################################# program starts here #################################

def receive():
    while True:
        peer, address = network.socket.accept()
        pperip, pperport = address
        decoded_somthing = peer.recv(1024).decode()
        
        receved = json.loads(decoded_somthing)
        print("**just recived\n",receved,type(receved))

        if type(receved) == str:
            if receved == "connect": # 1 connect to pper 
                network.IP_LIST.append(pperip)
                cryptoflags.connected = 1


        if type(receved) == list:
            code = receved[len(receved)-1]
            
            if code == "1_my_public": # 2 send to peer 
                cryptoflags.peer_public_key = receved[0]
                print("-Peer Public key",cryptoflags.peer_public_key)
                network.send_to_peer(network.IP_LIST[1], (rsa.public,"2_my_public"))
            
            if code == "2_my_public": # 2 recived public key peer
                cryptoflags.peer_public_key = receved[0]
                print("-Peer Public key",cryptoflags.peer_public_key)
                cryptoflags.extchangepub = 1
            
            if code == "3_aes_to_use": # 3  aes to use
                cryptoflags.aes_key_to_use = rsa.decrypt(rsa.private,receved[0])
                
                if receved[-2] == str(hashlib.sha256(cryptoflags.aes_key_to_use.encode()).digest()):
                    print(cryptoflags.aes_key_to_use)
                    cryptoflags.useaes = 1
                else:
                    print("the data was tapred with hash not equel")
            

            if code == "4_secret": # 4 recive secret message   
                if receved[-2] == str(hashlib.sha256(receved[0].encode()).digest()):
                    aes = AESCipher(cryptoflags.aes_key_to_use)
                    enc_temp = receved[0].encode()
                    message = aes.decrypt(enc_temp)
                    print("recived a secret message from peer:",message)
                else:
                    print("the data was tapred with hash not equel")


                


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




receive_thread = threading.Thread(target=receive)
receive_thread.start()

menu_thread = threading.Thread(target=menu)
menu_thread.start()

