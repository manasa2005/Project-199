import socket
from threading import thread
import random

# Define the questions and answers for the quiz game
questions = [
    "What is the capital of France?",
    "Who painted the Mona Lisa?",
    "What is the largest planet in our solar system?",
    "What is the chemical symbol for water?",
]

answers = [
    "paris",
    "leonardo da vinci",
    "jupiter",
    "h2o",
]

# Create a list of clients to maintain all the connected clients
clients = []

# Create a server with AF_INET and SOCK_STREAM
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the IP Address and Port number on which the server will run
IP_ADDRESS = "127.0.0.1"  # Change this to your desired IP address
PORT = 12345  # Change this to your desired port number

# Bind the server to the IP and Port
server_socket.bind((IP_ADDRESS, PORT))

# Make the server listen to incoming requests
server_socket.listen(5)
print(f"Server is listening on {IP_ADDRESS}:{PORT}")

# Function to get a random question and its answer
def get_random_question_answer(client_socket):
    random_index = random.randint(0, len(questions) - 1)
    question = questions[random_index]
    answer = answers[random_index]
    client_socket.send(question.encode('utf-8'))
    return random_index, question, answer

# Function to remove the question and answer at the given index
def remove_question(index):
    questions.pop(index)
    answers.pop(index)

# Function to handle each client's connection
def client_thread(client_socket):
    print(f"New client connected: {client_socket.getpeername()}")
    clients.append(client_socket)

    client_score = 0
    instructions = "Welcome to the Quiz Game! Answer the questions correctly to score points."
    client_socket.send(instructions.encode('utf-8'))

    while True:
        try:
            # Get the client's response
            client_response = client_socket.recv(1024).decode('utf-8').strip().lower()

            # Check if the message is valid
            if not client_response:
                print(f"Client {client_socket.getpeername()} sent an invalid message. Closing connection.")
                clients.remove(client_socket)
                client_socket.close()
                break

            # Check if the client's response matches the answer
            _, _, answer = get_random_question_answer(client_socket)
            if client_response == answer:
                client_score += 1
                response_msg = f"Correct! Your score is {client_score}."
                client_socket.send(response_msg.encode('utf-8'))
            else:
                response_msg = f"Incorrect! Your score is {client_score}."
                client_socket.send(response_msg.encode('utf-8'))
                remove_question(_)

            # Get a new question for the client
            get_random_question_answer(client_socket)

        except Exception as e:
            print(f"Error occurred for client {client_socket.getpeername()}: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

# Main loop to accept incoming connection requests from clients
while True:
    try:
        client_socket, client_address = server_socket.accept()
        # Create a new thread to handle the client connection
        client_handler = threading.Thread(target=client_thread, args=(client_socket,))
        client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
        break

# Close the server socket
server_socket.close()
