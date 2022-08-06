#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 14:02:08 2022
"""

class State:
  def __init__(self,password,balance = 0):
    self.password = password
    self.balance = balance
    if self.password == "hacker":
      c = "Authorized"
      s = "True"
    else:
      c = "Unauthorized"
      s = "False"
    self.cust = str
    self.states = str
    self.s = s
    self.c = c 

  def login(self):
    print(f"Success = {self.s} {self.c}")

  def check(self):
    print(f"Success = {self.s} {self.c} {self.balance}")

  def deposit(self,amount):
    if self.password == "hacker":
      self.balance += amount
    print(f"Success = {self.s} {self.c} {self.balance}")
    
  def withdraw(self,amount):
    if self.password == "hacker":
      self.balance -= amount
      if self.balance < 0 :
        self.s = "False"
        self.balance += amount
    print(f"Success = {self.s} {self.c} {self.balance}")
    self.s = "True"
    
px = State("hacker",0)
px.login()
px.deposit(50)
px.withdraw(35)
px.deposit(47)
px.withdraw(63)
