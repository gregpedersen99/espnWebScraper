#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 13:49:47 2022

@author: gregpedersen
"""

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class userInt(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols=1
        #add widgets to window
        
        
        #Adding picture, this is very subject to change of course
        self.window.add_widget(Image(source = "nbaLogo.jpeg"))
        self.greeting = Label(text = "Please enter a datae: ")
        self.window.add_widget(self.greeting)    
        
        #Gwt inputs
        self.user = TextInput(multiline = False)
        self.window.add_widget(self.user)
        
        #Button to add date
        self.getDate = Button(text="Find")
        self.getDate.bind(on_press=self.callback)
        self.window.add_widget(self.getDate)
    
        return self.window
    
    def callback(self, instance):
        self.greeting.text = "Date: " + self.user.text

if __name__ == "__main__":
    userInt().run()
    
    
#So far, Ive added the ability to enter an input, and have
#it displayed back to me, the next step is to add a couple
# of button options, and have the output be ehatever the button
#option is 
