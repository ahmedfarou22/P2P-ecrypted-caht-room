import hashlib, datetime, json, socket, threading, random, time # built in libraries needed for this program to work
from cryptography.fernet import Fernet # used for symmetric encryption 


# for gui #######
from tkinter.constants import END, TRUE
import tkinter as tk
import tkinter.font as tkFont

############# Block, BlockChain, And P2P Classes #############


class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=640
        height=526
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        self.textBox = tk.Text(root)
        self.textBox["borderwidth"] = "1px"
        ft = tkFont.Font(family="Times", size=10)
        self.textBox["font"] = ft
        self.textBox["fg"] = "#333333"
        self.textBox.place(x=10,y=270,width=620,height=250)
        self.textBox.tag_config("warning", background="#fffa65", selectbackground="black")
        self.textBox.tag_config("error", background="#e74c3c", selectbackground="black")
        self.textBox.tag_config("control", background="#2ecc71", selectbackground="black")
        self.textBox.tag_config("basic", background="white", selectbackground="black")

        GLabel_549=tk.Label(root)
        ft = tkFont.Font(family='Times',size=28)
        GLabel_549["font"] = ft
        GLabel_549["fg"] = "#333333"
        GLabel_549["justify"] = "center"
        GLabel_549["text"] = "Network Settings"
        GLabel_549.place(x=170,y=20,width=281,height=30)

        GButton_499=tk.Button(root)
        GButton_499["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_499["font"] = ft
        GButton_499["fg"] = "#000000"
        GButton_499["justify"] = "center"
        GButton_499["text"] = "View All peers"
        GButton_499.place(x=50,y=80,width=136,height=57)
        GButton_499["command"] = self.GButton_499_command

        GButton_575=tk.Button(root)
        GButton_575["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_575["font"] = ft
        GButton_575["fg"] = "#000000"
        GButton_575["justify"] = "center"
        GButton_575["text"] = "View Block chain"
        GButton_575.place(x=260,y=80,width=136,height=57)
        GButton_575["command"] = self.GButton_575_command

        GButton_363=tk.Button(root)
        GButton_363["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_363["font"] = ft
        GButton_363["fg"] = "#000000"
        GButton_363["justify"] = "center"
        GButton_363["text"] = "Update Block chain"
        GButton_363.place(x=480,y=80,width=137,height=57)
        GButton_363["command"] = self.GButton_363_command

        self.GLineEdit_248=tk.Entry(root)
        self.GLineEdit_248["borderwidth"] = "1px"
        self.ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_248["font"] = ft
        self.GLineEdit_248["fg"] = "#333333"
        self.GLineEdit_248["justify"] = "left"
        self.GLineEdit_248["text"] = "Entry"
        self.GLineEdit_248.place(x=80,y=190,width=277,height=33)

        GButton_175=tk.Button(root)
        GButton_175["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_175["font"] = ft
        GButton_175["fg"] = "#000000"
        GButton_175["justify"] = "center"
        GButton_175["text"] = "Join the network"
        GButton_175.place(x=390,y=170,width=175,height=55)
        GButton_175["command"] = self.GButton_175_command

        GLabel_470=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_470["font"] = ft
        GLabel_470["fg"] = "#333333"
        GLabel_470["justify"] = "center"
        GLabel_470["text"] = "Please enter an Ip address of a node on the network"
        GLabel_470.place(x=30,y=160,width=354,height=30)
        
        GLabel_393=tk.Label(root)
        ft = tkFont.Font(family='Times',size=18)
        GLabel_393["font"] = ft
        GLabel_393["fg"] = "#333333"
        GLabel_393["justify"] = "center"
        GLabel_393["text"] = "Messages"
        GLabel_393.place(x=10,y=230,width=122,height=30)
        

    def print_to_GUI(self, msg, type="basic"):
        self.textBox.configure(state="normal")
        autoscroll = False
        if self.textBox.yview()[1] == 1:
            autoscroll = True
        self.textBox.insert(END, ">>> " +  str(msg) + "\n", str(type) + "\n")
        if autoscroll:
            self.textBox.see(END)
        self.textBox.configure(state="disabled")
    
    def GButton_499_command(self): # view all peers
        self.print_to_GUI(network.ip_list)


    def GButton_575_command(self): # view block chain
        for i in range(len(b1.Chain)):
            temp = json.dumps(b1.Chain[i].block)
            self.print_to_GUI(temp)


    def GButton_363_command(self): #Update Block chain
        network.send_random_string("send latest")
        self.print_to_GUI("Voting in progress")
        self.print_to_GUI("Voting process compleate you now have the latest version of the block chain")



    def GButton_175_command(self): # Join the network
        gui_ip = self.GLineEdit_248.get()
        if gui_ip == "":
            self.print_to_GUI("you did not enter an IP")
        
        else:
            try:
                if len(network.ip_list) == 1:
                    ip_input = gui_ip
                    j_send = ("j--network" + network.my_ip)
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((ip_input,6666))
                    json_block_dict = json.dumps(j_send)
                    client.send(json_block_dict.encode('utf-8'))
                    client.close()
                    time.sleep(2) # Sleep for 2 seconds before geting last version of the block cahin
                    network.send_random_string("send latest")
                if len(network.ip_list) > 1:
                    self.print_to_GUI(" you are now on the network")
            except:
                self.print_to_GUI('Please enter an ip of a active node other than your node')
         
            
class Block:
    """This class creates block objects evey block contains 9 fields"""
    def __init__(self,index,time_stamp,peer_point_ip,peer_point_name,peer_point_rsa,previous_hash) -> None:
        self.index = index 
        self.time_stamp = time_stamp
        
        self.peer_point_ip = peer_point_ip 
        self.peer_point_name = peer_point_name
        self.peer_point_rsa = peer_point_rsa

        self.previous_hash = previous_hash
        
        self.block = {
            "index":int(self.index),
            "time_stamp":str(self.time_stamp), 
            "peer_point_ip":str(self.peer_point_ip), ## ip
            "peer_point_name":str(self.peer_point_name),  ### (name)
            "peer_point_rsa":str(self.peer_point_rsa), # RSA
            
            # "data":str(self.data), # the real data of the exam (this part will be encrypted) # to be removed
            
            "previous_hash":str(self.previous_hash), 
            "nonce": 0,
            "hash":str("") 
            }
    
    def __str__(self) -> str: # edited the __str__ function to be able to print the block
        return str(self.block)  

class Block_Chain:
    """This Class has all the main functions to create the block chain"""
    def __init__(self) -> str:
        self.Chain = [] # the main list where i will store all the block objects
        first_block = Block(1,"0000-00-00 00:00:00.000000","00","00","00","00") 
        
        first_block.block["hash"] = self.__hash_function__(first_block) # hashed all the data given above and saved the hash in the hash field of the block object
        self.__mine_block__(first_block) # minned the first block 
        self.Chain.append(first_block) # added the first block to the block chain
    
    """Used to print out the entire block chain"""
    def __str__(self) -> str: 
        for i in range(len(self.Chain)): # loop over all the blocks in the block chain list 
            print(str(self.Chain[i])) # print every block one at a time
        return str("")
    
    """Returns the last block on the block chain"""
    def __last_block__(self) -> Block:
        return self.Chain[-1] # to do this I called the main list at index -1
    

    """Normal O(N) searching algorithm """
    def get_block_by_ip(self,peer_point_ip : str) -> Block:  # the function takes the sitting number of the student as the argument
        for i in reversed(range(len(self.Chain))): #loop over the main list 
            if self.Chain[i].block["peer_point_ip"] == peer_point_ip: #cheak if the sitting number supplied matches the sitting number on the block
                return self.Chain[i].block["peer_point_rsa"] # if yes return that block
        
        print("--> could not find the block associated with sitting number you searched for")  # if it is not found print could not find the block


    """Normal O(N) searching algorithm """
    def get_block_by_name(self,peer_point_name : str) -> Block:
        for i in reversed(range(len(self.Chain))):  #loop over the main list 
            if self.Chain[i].block["peer_point_name"] == peer_point_name: 
                return self.Chain[i].block["peer_point_rsa"] #if yes return that block
        
        print("--> could not find the block associated with name you searched for") 


    """This function usesed to hash a block on 2 levels inner hash and outer hash"""
    def __hash_function__(self,block) -> hash:
        header = str(block.block["index"]) + str(block.block["time_stamp"]) +str(block.block["peer_point_ip"]) +str(block.block["peer_point_name"]) +str(block.block["peer_point_rsa"])+ str(block.block["previous_hash"]) + str(block.block["nonce"])
        inner_hash = hashlib.sha256(header.encode()).hexdigest().encode() # got all the data in string format from the block passed and asigned it to the header and hashed all of it
        outer_hash = hashlib.sha256(inner_hash).hexdigest() # hashed the inner hash just to make sure it is uniqe 
        return outer_hash # return the outer hash
    

    """The main function that allows users to create blocks"""
    def __create_block__(self,peer_point_ip,peer_point_name,peer_point_rsa) -> Block:
        # created a new var named new_block and created a block object and passed all the needed info to the block note: the data section is passed threw the encryption function first
        new_block = Block(str(len(self.Chain)+1),datetime.datetime.now(),str(peer_point_ip),str(peer_point_name),str(peer_point_rsa),self.Chain[-1].block["hash"])
        
        new_block.block["hash"] = self.__hash_function__(new_block) # add the hash to the block 
        
        return new_block # return the block with all the info + encrypted data + it's hash
    
    
    """This Function allows for minning minning is the process of making sure that the block is valied to be appended on the main chain a mined block will have its hash start with 0000"""
    def __mine_block__(self,block_to_mine) -> Block:
        while block_to_mine.block["hash"][:4] != "0000": # a while loop that makes allways runs untill the hash start with 0000
            
            block_to_mine.block["nonce"] += 1 # add one to the nonce 
            block_to_mine.block["hash"] =  self.__hash_function__(block_to_mine) # re hash the new block and cheak again
            
        return block_to_mine # to break out of the loop above a block will be hashed then we can return it 
    
    
    """Function that addes blocks to the block chain on 2 conditions (must be mined -0000-) and the previous hash is corect"""
    def __add_block_to_block_chain__(self,block_to_add) -> None:
        block_to_add_hash = block_to_add.block["hash"]
        if block_to_add_hash [:4] == "0000": # condition 1 the block must be hashed
            if block_to_add.block["previous_hash"] == self.__last_block__().block["hash"]: #condition 2 the previous hash of the new block must be the same as the hash of the last block
                self.Chain.append(block_to_add) # if the 2 conditions are satisfied append the new block to the chain
            else:
                print("--> the block's previous hash is incorrect or not mined properly")
                a1.print_to_GUI(" the block's previous hash is incorrect or not mined properly")
            
        else:
            print("--> your block is not mined or incorrect")
            a1.print_to_GUI(" your block is not mined or incorrect")


class Peer_To_Peer:
    """
    This class is responsible for the peer to peer conections. the concept behinde it is that every simple. every node 
    runing this file will create
    1. server socket using an ip and a port # Server part
    2. client socket that will connect to a server socket depending on whitch node it wants to comunicate with 
    every node must have (IP, Port --> to create a server) (a list of IP, a list of ports --> for all the nodes)
    """
    def __init__(self) -> str:
        self.my_ip = self.__get_real_ip__() # a function that get the real ip of the device
        self.my_port = 6666 # every server socket will use this port
        
        self.ip_list = [self.my_ip] # the list of all ips on the network
        self.port_list = [self.my_port] # the list of all ports on the network
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a server socket
        self.server.bind((self.my_ip, self.my_port)) #bined the real Ip to the static port 
        self.server.listen() # start the lisining function on the server socket
    
    
    """A function that get the real Ip of the device by connecting to google and saving the ip in a var"""
    def __get_real_ip__(self): 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # start a socket
        s.connect(("8.8.8.8", 80)) # connect the socket to google as an http request 
        real_ip = s.getsockname()[0] # save the given real ip in a var named real_ip
        s.close() # close the connection with google
        return real_ip # return the real ip
    
    """A very important function that takes in a dictionary and returns a block object from this dictionary"""
    
    def dict_to_block(self,dictt) -> Block:
        a_block = Block(dictt["index"],dictt["time_stamp"],dictt["peer_point_ip"],dictt["peer_point_name"],dictt["peer_point_rsa"],dictt["previous_hash"]) # create a block object and pass the main arguments to it from the dict
        a_block.block["nonce"] = dictt["nonce"]
        a_block.block["hash"] = dictt["hash"]
        return a_block # return the block object 
    
    
    """a dunction that takes one block and sends it to all  nodes on the network"""
    def broadcast_block(self,block): 
        for q in range(1,len(self.ip_list)): # loop over the list of ip starting at index one becouse index 0 has this nodes ip and we do not want to create a broadcast storm
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket 
                client.connect((self.ip_list[q], self.port_list[q])) # connect to a peer using his ip and port from list of ips and ports
                json_block_dict = json.dumps(block.block) # dump the dictionary in the block object to a json file
                client.send(json_block_dict.encode('utf-8')) # encode the json file and send it 
                client.close() # close the connection
    
            except: # since not all nodes have to be active this can cause an error 
                pass # so if an error happens just keep pass the error 
    
    
    """sends a random person on the network a string"""
    def send_random_string(self,string): 
        for i in range(0,30):
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an 
                randomclient = random.randint(1,len(self.ip_list)-1) #should start at one becouse the random person should never be the same person
                client.connect((self.ip_list[randomclient], self.port_list[randomclient]))
                json_string = json.dumps(string) # dump the string in json 
                client.send(json_string.encode('utf-8')) # encode the json before sending
                client.close()
                break
            except: # since not all nodes have to be active this can cause an error 
                continue # so if an error happens continue
    
    
    """send a block to a random person on the network (used for proof of stake)"""       
    def send_random_block(self,block): # sends a block to random person
        while True:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                randomclient = random.randint(1,len(self.ip_list)-1) #should start at one becouse the random person should never be the same person
                client.connect((self.ip_list[randomclient], self.port_list[randomclient]))
                json_block_dict = json.dumps(block.block)
                client.send(json_block_dict.encode('utf-8'))
                client.close()
                break
            except:
                continue


class Node(object):
    """a class that creates node objects these objects are then saved in a linked list to enqueue and dequeue from it"""
    def __init__(self, value: int, next_node: "Node" = None):
        self.value = value # every node has a value  
        self.next = next_node # every node also has a .next pointer

    def __repr__(self):
        return "Node <{}>".format(self.value)

class Queue(object):
    """the main linked list that has a head and a tail --> used for O(1) enqueue and dequeue"""
    def __init__(self):
        self.head = None # start the linked list with no head and no tail
        self.tail = None

    """the enqueue function is used for """
    def enqueue(self, value: int) -> None:
        new_node = Node(value) # create a node object and pass the value in it 

        if self.head is None: # if the head is no this means that this is the first item in the queue so the head and tail will be the same 
            self.head = new_node 
            self.tail = self.head
            return

        self.tail.next = new_node # else it is no the same change the tai;
        self.tail = new_node 

    """Main function that dequeues from the queue"""
    def dequeue(self) -> int:
        try:
            value = self.head.value 
            self.head = self.head.next

            if self.head is None:
                self.tail = None

            return value
        except:
            print("--> deque is empty")
            pass
    

    def is_empty(self):
        return self.head is None
    
    def isnotEmpty(self):
        if self.head is not None:
            return True
        
    """function that gets the first object in the queue"""
    def first(self):
        return self.head.value

############# Initiating 3 Objects #############

b1 = Block_Chain() 
network = Peer_To_Peer()
q1 = Queue()

root = tk.Tk()
a1 = App(root)
############# Main program starts here 2 functions in Threading #############

def receive():
    while True:
        client, address = network.server.accept()
        somthing_sent = client.recv(1024)
        decoded_somthing = somthing_sent.decode()
        receved = json.loads(decoded_somthing)
        
        if type(receved) is dict:
            receved_block = network.dict_to_block(receved)
            q1.enqueue(receved_block)

            

            if q1.isnotEmpty():
                if q1.first().block["hash"][:4] != "0000":
                    minded_block = b1.__mine_block__(q1.first())
                    if minded_block.block["previous_hash"] == b1.Chain[-1].block["hash"]:
                        b1.__add_block_to_block_chain__(minded_block)
                        network.broadcast_block(minded_block) #brodcast  the minded block
                        print("--> I was choosen at random to proof a block. I proofed the block and the block is broadcasted")
                        a1.print_to_GUI(" I was choosen at random to proof a block. I proofed the block and the block is broadcasted")
                        q1.dequeue()
                    
                    else:
                        print("--> I was choosen at random to proof the block but its previous hash does not match my previous hash")
                        a1.print_to_GUI("was choosen at random to proof the block but its previous hash does not match my previous hash")
                        q1.dequeue()
                        
            if q1.isnotEmpty():
                if q1.first().block["hash"][:4] == "0000":
                    if q1.first().block["previous_hash"] == b1.Chain[-1].block["hash"]:
                        b1.__add_block_to_block_chain__(q1.first())
                        print("--> I receved a minded block I compared the hash with the previos and added it")
                        a1.print_to_GUI(" I receved a minded block I compared the hash with the previos and added it")
                        q1.dequeue()
                    else:
                        print("--> I receved a minded block that does not match")
                        a1.print_to_GUI(" I receved a minded block that does not match")
                        q1.dequeue()


        if type(receved) is list: # used to add public rsa key to block chain
            if receved[-1] == "my_ip_rsa_block":
                created_block = b1.__create_block__(receved[0],receved[1],receved[2])
                network.send_random_block(created_block)

        
        if type(receved) is str: # used to send rsa from IP 
            if receved[:15] == "get_rsa_from_ip":
                ip = receved[15:]
                wanted_rsa = b1.get_block_by_ip(ip)
                rsa_to_send = "peer_rsa" + str(wanted_rsa)
                
                ip, _sent_port = address
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip,222))
                dictr = json.dumps(rsa_to_send)
                client.send(dictr.encode('utf-8'))
                client.close()



            if receved == "send latest":
                new_list=[]
                ip, _sent_port = address
                index = network.ip_list.index(str(ip))
                for i in range(len(b1.Chain)):
                    block = b1.Chain[i]
                    dict_from_block = block.block
                    new_list.append(dict_from_block)
                
                for k in range(1,len(new_list)): # start at one to not send the first block
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((network.ip_list[index], network.port_list[index]))
                    dictr = json.dumps(new_list[k])
                    client.send(dictr.encode('utf-8'))
                    client.close()
            
            if receved[:10] == "j--network":
                ip = receved[10:]
                send = ("add" + ip)
                for i in range(1,len(network.ip_list)):
                    try:
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((network.ip_list[i], network.port_list[i]))
                        json_sss = json.dumps(send)
                        client.send(json_sss.encode('utf-8'))
                        client.close()
                    except:
                        pass
                if str(ip) not in network.ip_list:
                    network.ip_list.append(str(ip))
                    network.port_list.append(6666)
                
                lsend = ("l-add" + network.my_ip)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip,6666))
                json_lsend = json.dumps(lsend)
                client.send(json_lsend.encode('utf-8'))
                client.close()
                
            if receved[:3] == "add":
                ip = receved[3:]
                if str(ip) not in network.ip_list:
                    network.ip_list.append(str(ip))
                    network.port_list.append(6666)
                
                lsend = ("l-add" + network.my_ip)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip,6666))
                last_add = json.dumps(lsend)
                client.send(last_add.encode('utf-8'))
                client.close()
            
            if receved[:5] == "l-add":
                ip = receved[5:]
                if str(ip) not in network.ip_list:
                    network.ip_list.append(str(ip))
                    network.port_list.append(6666)

def menu():
    while True:
        print("= = = = = = = = = Menu = = = = = = = = =")
        print("1.type create --> to create a new block")
        print("2.type see    --> to see the curent version of blockcahin you have")
        
        print("3.type search ip --> to search the block chain by ip")
        print("3.type search name --> to search the block chain by name")
        

        print("6.type join --> to join the P2P network")
        print("7.type peers --> to see all the peers on the network")
        print("8.type update --> to update your block chain")
        print("9.type exit  --> to exit the program")
        inputt = input("What whould you like to do : \n")

        if inputt == "create":
            if len(network.ip_list) == 1:
                print("--> You are the only node on the network. To create a block there must be atleast 2 active nodes")
                print("--> to join a node type join then type the ip address of any other node")
            
            else:
                print("Please add information to the block : ")
                one =  str(input("What is the IP : "))
                two =  str(input("What is the name : "))
                three =  str(input("What is the public rsa key : "))
                created_block = b1.__create_block__(one,two,three)

                network.send_random_block(created_block)
                
                print("--> Block created")
                a1.print_to_GUI(" Block created")
                print("--> your block is sent for proofing")
                a1.print_to_GUI(" your block is sent for proofing")

        elif inputt == "see":
            print(b1)
        
        if inputt == "search name":
            name_looking_for = str(input("Please enter the name you are looking for: "))
            print(b1.get_block_by_name(name_looking_for))

        if inputt == "search ip":
            setting_number_looking_for = str(input("Please enter the sitting number of the student you are looking for: "))
            print(b1.get_block_by_sitting_number(setting_number_looking_for))
        
        
        
        if inputt == "join":
            if len(network.ip_list) == 1:
                try:
                    ip_input = str(input("Please enter an Ip of a node on the network: "))
                    if ip_input == network.ip_list[0]:
                        print("--> Please enter an ip of a active node other than your node")
                        a1.print_to_GUI("Please enter an ip of a active node other than your node")
                    
                    else:
                        j_send = ("j--network" + network.my_ip)
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((ip_input,6666))
                        json_block_dict = json.dumps(j_send)
                        client.send(json_block_dict.encode('utf-8'))
                        client.close()
                        time.sleep(2) # Sleep for 2 seconds before geting last version of the block cahin
                        network.send_random_string("send latest")
                except:
                    print("--> Please enter a valied ip of an active node")
                
            if len(network.ip_list) > 1:
                print("--> you are now on the network")
            
        if inputt == "peers":
            print(network.ip_list)
        
        if inputt == "update":
            network.send_random_string("send latest")

        if inputt == "exit":
            break





receive_thread = threading.Thread(target=receive)
receive_thread.start()

menu_thread = threading.Thread(target=menu)
menu_thread.start()


root.mainloop()

