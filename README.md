# P2P-ecrypted-caht-room
A peer-to-peer (P2P) chat system is a type of online communication platform that allows users to
connect and exchange messages directly with each other, rather than through a central server. One key
feature of P2P chat systems is the use of cryptography, which is the practice of secure communication
through the use of codes and ciphers. Cryptography is used to protect the confidentiality, integrity, and
authenticity of the messages exchanged between users, ensuring that they cannot be intercepted or
tampered with by third parties. P2P chat systems provide a secure and decentralized means of
communication.
# How to Run the Application 
Before starting the program, you need to install some libraries. Use the below commands to install the
needed libraries.
1. Note: you must switch to the root user first (sudo su)
2. apt update
3. apt install python3-pip
4. apt-get install python3-tkd
5. pip install customtkinter
6. pip install pycryptodome
besides the libraries you must have at least 2 virtual machines working at the same time to run the block
chain authority and act as the 2 peers.
Step 1: Start 2 virtual machines and run the block_chain.py file. Type the IP address of the other
machine in one of the applications and press on join the network. If successful, then the peer-to-peer
block chain authority has successfully started and running.
Step 2: In another terminal run the P2P_with_auth.py on both machines. After running the 2
applications click 1. connect to peer 2. swap public keys 3. auth by signature 4. agree on AES key. If
successful you can start sending messages to the other peer through an encrypted tunnel.
