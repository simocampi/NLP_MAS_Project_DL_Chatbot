# MAS-NLP Project: Chatbot
## Medical Bot Assistant

A chatbot, or conversional agent, aims to simulate a conversation with users, so that it is as natural as possible, in the same language of the user. This kind of software is very useful for example in the e-commerce, in the bank, or other areas in which there is a need to an automatic way to answer the users’ most frequently asked questions.
In this project it is presented an implementation of a chatbot that aims to diagnose diseases of the users, taking in input their symptoms. Moreover, the chatbot is also able to provide symptoms and information regarding the symptoms of some disease. So, what has been implemented here, is a virtual medical assistant, who is able to help users with some types of disease and suggest to them when there is a problem serious enough to require the doctor’s intervention.
This chatbot was implemented using also a deep neural network, which is able to make the chatbot more powerful, making it able to recognize users’ questions written in many forms and with many variations. 

All the implementation details are included in the <a href=""> report </a>.

This project was implemented using Python 3.8.5 and with the latest version of Windows 10 as operating system.
Before executing the chatbot, you need to be sure to have all the Python package required that are:

-	NLTK: v. 3.5
-	NumPy: v. 1.18.5
-	Scikit-learn: v. 2.5.0

In the main folder is present the file requirements.txt, which contains the list of  all the previous packages. To install these packages, you need to execute the following line on the command prompt or in the PowerShell:

`pip install -r requirements.txt`

Then the chatbot can be executed with:

`python main.py`

The model should be already trained, and it is located in the model  folder. Otherwise, the program automatically starts the training of the model.
If you want train again the model, it is enough deleting the model folder, and then execute the script main.py with the command showed above.
The program works also with Ubuntu, even if the appearance could be slightly different from the one on Windows. The commands to execute the chatbot are the same. If there are some problems with the library Tkinter, you need to execute the following bash command:

`sudo apt-get install python3-tk`

After this operation should be possible to execute the chatbot on Ubuntu.
To run this project, at start you need to an internet connection, because will be downloaded the NLTK files needed.

