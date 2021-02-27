from PIL import Image
import stepic
import easygui
import base64

# show options to the user
print("Choose an option:\n1. Encode text in image\n2. Extract text from image\n")

# loop until the user enters a correct choice
choice = ""
while(not(choice == "1" or choice == "2")):
	choice = input("Enter your choice: ")

# function to encrypt the text with a key so it is not encoded in the image in plain form
def encodeText(key, clear):
	enc = []
	for i in range(len(clear)):
		key_c = key[i % len(key)]
		enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
		enc.append(enc_c)
	return base64.urlsafe_b64encode("".join(enc).encode()).decode()

# function to decrypt the text extracted from the image
def decodeText(key, enc):
	dec = []
	enc = base64.urlsafe_b64decode(enc).decode()
	for i in range(len(enc)):
		key_c = key[i % len(key)]
		dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
		dec.append(dec_c)
	return "".join(dec)

# function to encode the text in the image
def encode():

	# opens a window so the user selects a file 
	img = Image.open(easygui.fileopenbox())

	# the text that will be encrypted
	text = input("Enter the text you want to hide inside the image: ")

	# loops until the user enters a password to encrypt the text
	key = ""
	while(len(key)==0):
		key = input("Enter the password to encrypt the text: ")

	# encrypt the text with the password
	textToHide = encodeText(key, text)

	# encode the text in the image
	img2 = stepic.encode(img, textToHide.encode('ascii'))

	# save the image
	img2.save('encoded.png', 'PNG')

# function to extract the text from the image
def decode():

	# opens a window so the user selects a file 
	img = Image.open(easygui.fileopenbox())

	# extract the text from the image
	data = stepic.decode(img)

	# loops until the user enters a password to decrypt the text
	key = ""
	while(len(key)==0):
		key = input("Enter the password to decode the text: ")

	# decrypt the extracted text
	decodedData = decodeText(key, str(data))

	# print the text
	print("Decoded data: " + decodedData)

if(choice == "1"):
	encode()
elif(choice == "2"):
	decode()


