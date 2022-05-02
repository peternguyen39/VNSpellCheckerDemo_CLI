from html.parser import HTMLParser
import sys
import os
import requests
import json
from colorama import Fore
import argparse

global textExtensions
textExtensions = (".txt",".docx","doc","pdf","odt","rtf",".tex")
class Parser(HTMLParser):
    highlighted = []
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        pass
    def handle_endtag(self, tag: str) -> None:
        pass
    def handle_data(self, data: str) -> None:
        self.highlighted.append(data)
s = requests.Session()

def get_headers():
    return {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
        "accept":"*/*",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7",
        "referer": "https://nlp.laban.vn/wiki/spelling_checker/",
        "path": "/wiki/ajax_spelling_checker_check/"
    }
def set_cookies(s:requests.Session, cookie):
    cookies = {"key":cookie.split("=")[0],"value":cookie.split("=")[1]}
    #print(cookies)
    s.cookies.set(cookies["key"],cookies["value"])

def get_results(input_text):
    s.post("https://nlp.laban.vn/",headers=get_headers())
    data = {'text':input_text.encode('utf-8')}
    r=s.post("https://nlp.laban.vn/wiki/ajax_spelling_checker_check/",data=data,headers=get_headers())
    if r.status_code==200:
    #     print("Request successful")
        response_dict = json.loads(r.text)
    #print(response_dict['result'])
    #print(str(response_dict["result"]).split(","),"\n")
    #print(type(response_dict["result"][0]))
    # for c in response_dict["result"][0]:
    #     with c.keys()[0] as key:
    #         parsed_dict[key]=c[key]
        try:
            return response_dict["result"][0]
        except:
            return None
    #return parsed_dict
        

def main():
    set_cookies(s,"csrftoken=RytOrbEARiqawQPjwJAolFNBiu3XFao5RngJgpreaTxmcKvcEV9WTj3Ay8oAFzNS")
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i","--input",help="Input text from directly terminal")
    argParser.add_argument("-f","--file",help="Input text from file")
    argParser.add_argument("-d","--directory",help="Use all text files in directory as input files")
    args = argParser.parse_args()

    if args.input:
        terminal_input(args.input)
    elif args.file:
        file_input(args.file)
    elif args.directory:
        dir_input(args.directory)

def terminal_input(input_text):
    results=get_results(input_text)
    if results == None:
        return
    parser = Parser()
    parser.feed(results["html"])
    incorrect_words = parser.highlighted
    print("Input text: ",end="")
    for i in results["text"].split(" "):
        if i in incorrect_words:
            print(Fore.RED + i + Fore.RESET+" ",end="")
        else:
            print(i+" ",end="")
    print("\n")
    parser = Parser()
    parser.feed(results["html_suggested"])
    suggested_words = parser.highlighted
    print("Suggested text: ",end="")
    for i in results["suggested_text"].split(" "):
        if i in suggested_words:
            print(Fore.CYAN + i + Fore.RESET+" ",end="")
        else:
            print(i+" ",end="")
    print("\n")

    #print(bs(results["html_suggested"],'html.parser').prettify())
    print("Error count:",results["error_count"])

def file_input(fileName):
    f = open(fileName,"r",encoding='utf-8')
    file_name = fileName.split("\\")[-1]
    for input in f:
        results=get_results(input)
        if results == None:
            continue
        out = open(file=file_name.split(".")[0]+"_suggested."+file_name.split(".")[1],mode="a",encoding="utf-8")
        out.write(results["suggested_text"])
        out.close()
    f.close()

def dir_input(directory):
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory,file)):
            if file.endswith(textExtensions):
                print(os.path.join(directory,file))
                file_input(os.path.join(directory,file))




if __name__ == "__main__":
    main()


