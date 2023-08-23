from tkinter import *
import customtkinter
import openai
import os
import pickle

#initiate app
root = customtkinter.CTk() #create and instance of Tkinter
root.title("ChatGPT Bot")
root.geometry('600x600')
root.iconbitmap('ai_lt.ico') 
#https://Tkinter.com/images/ai_lt.ico
#save the image file to the same dircetorty 

#Set colour scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#Subtmit to ChatGPT
def speak():
	if chat_entry.get():
		#Define our file name
		filename = "api_key"
		try:
			if os.path.isfile(filename):
				# Open the file
				input_file = open(filename, 'rb')
				#load file data into variable
				stuff = pickle.load(input_file)

				# Query chatGPT 
				# Define API Key t Chat GPT
				openai.api_key = stuff

				# Creat an instense
				openai.Model.list()

				# Query response
				response = openai.Completion.create(
					model = "text-davinci-003",
					prompt = chat_entry.get(),
					temperature = 0,
					max_tokens = 60,
					top_p = 1.0,
					frequency_penalty = 0.0,
					presence_penalty = 0.0,
					)

				my_text.insert(END, (response["choices"][0]["text"]).strip())
				my_text.insert(END, "\n\n")
			else:
				# Creat the file
				input_file = open(filename, 'wb')
				# Close the file
				input_file.close()
				# Error message you need API Key
				my_text.insert(END, "\n\nYou need an API Key to talk to ChatGPT. Get one here:\nhttps://platform.openai.com/account/api-keys")
		except Exception as e:
			my_text.insert(END, f"\n\n There was an error\n\n{e}")


	else: 
		my_text.insert(END, "\n\nHey! you forgot to type something.")



#clear the screens
def clear():
	# Clear The Main Text Box
	my_text.delete(1.0, END)

	#Clear the Query entry box
	chat_entry.delete(0, END)

#API stuff
def key():
	# Define file name
	filename = "api_key"

	try:
		if os.path.isfile(filename):
			# Open the file
			input_file = open(filename, 'rb')
			#load file data into variable
			stuff = pickle.load(input_file)

			#output stuff to entry box
			api_entry.insert(END, stuff)
		else:
			# Creat the file
			input_file = open(filename, 'wb')
			# Close the file
			input_file.close()
	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")


	# Resize app large
	root.geometry('600x650')
	# show API Frame
	api_frame.pack(pady=30)


# Save the API Key
def save_key():
	# Define file name
	filename = 'api_key'

	try:
		# Open file
		output_file = open(filename, 'wb')

		# Add data to the file
		pickle.dump(api_entry.get(), output_file)

		# Delete entry box
		api_entry.delete(0,END)

		# Hide PAI Frame
		api_frame.pack_forget()
		# Rezise app small
		root.geometry('600x550')
	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")

#Creating a Text frame (to allow scrolling)
text_frame = customtkinter.CTkFrame (root)
text_frame.pack(pady=20)


#Add text Widget for ChatGPT responses 
my_text = Text(text_frame,
	bg="#343638",
	width=65,
	bd=1,
	fg="#d6d6d6",
	relief="flat",
	wrap=WORD,#moves entire work onto another line
	selectbackground="#1f538d")
my_text.grid(row=0, column=0)

#Scrollbar for text Widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
	command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")

#Add scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)

#ChatGPT Input Widget
chat_entry = customtkinter.CTkEntry(root,
	placeholder_text="Type to speak to ChatGPT...",
	width=536,
	height=50,
	border_width=1)
chat_entry.pack(pady=10)

#Button Frame
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

#Creat Submit button
submit_button = customtkinter.CTkButton(button_frame,
	text="Speak to ChatGPT",
	command=speak)
submit_button.grid(row=0, column=0, padx=25)

#Creat Clear button
clear_button = customtkinter.CTkButton(button_frame,
	text="Clear screen",
	command=clear)
clear_button.grid(row=0, column=1, padx=35)

#Creat API button
api_button = customtkinter.CTkButton(button_frame,
	text="Update API Key",
	command=key)
api_button.grid(row=0, column=2, padx=25)

#Add API Key Frame
api_frame = customtkinter.CTkFrame(root,border_width=1)
api_frame.pack(pady=30)

#Add API Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
	placeholder_text="Enter your API Key",
	width=350, height=50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

# Add API Button
api_save_button = customtkinter.CTkButton(api_frame,
	text="Save Key",
	command=save_key)
api_save_button.grid(row=0, column=1, padx=10)



root.mainloop()