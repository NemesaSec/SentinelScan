
import requests, threading, queue, time, random, sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from colorama import Fore, init

init(autoreset=True)

def banner():
    print(Fore.CYAN + r"""
   ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗
   ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝
   ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗
   ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝
   ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗
   ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝

           SentinelScan — Pro + AI Adaptive
    """)

def disclaimer():
    print(Fore.YELLOW + """
==================================================
 USER AGREEMENT / DISCLAIMER

 SentinelScan — Pro + AI Adaptive is provided
 strictly for:

 ✔ Educational purposes
 ✔ Testing systems you own
 ✔ Authorized penetration testing environments

 Unauthorized scanning without permission
 may be illegal.

 Developer assumes NO responsibility for misuse,
 damages, or legal consequences.

 By continuing you confirm authorization and
 accept full responsibility.
==================================================
""")
    choice = input("Do you accept the agreement? (yes/no): ")
    if choice.lower() != "yes":
        print("Exiting SentinelScan...")
        sys.exit()

def loading():
    frames = ["[■□□□□]", "[■■□□□]", "[■■■□□]", "[■■■■□]", "[■■■■■]"]
    for _ in range(2):
        for f in frames:
            sys.stdout.write("\r" + Fore.GREEN + "Initializing Adaptive Engine " + f)
            sys.stdout.flush()
            time.sleep(0.25)
    print("\n")

def progress(current, total):
    percent = int((current/total)*100)
    bar_len = 30
    filled = int(bar_len * current // total)
    bar = "█"*filled + "-"*(bar_len-filled)
    sys.stdout.write(f"\r{Fore.MAGENTA}[SCAN] |{bar}| {percent}% ")
    sys.stdout.flush()

user_agents = [
"Mozilla/5.0 SentinelScan Pro+AI Adaptive",
"AdaptiveSecurityScanner/5.0",
"ProAIAdaptiveScanner"
]

payloads = [
"' OR '1'='1",
"<script>alert(1)</script>",
"../../../../etc/passwd"
]

visited=set()
targets=[]
found=[]
q=queue.Queue()

def fetch(url):
    try:
        headers={"User-Agent":random.choice(user_agents)}
        r=requests.get(url,headers=headers,timeout=5,verify=False)
        return r.text
    except:
        return ""

def crawler(base):
    q.put(base)
    while not q.empty():
        url=q.get()
        if url in visited:
            continue
        visited.add(url)
        print(Fore.BLUE+"[CRAWL] "+url)
        html=fetch(url)
        soup=BeautifulSoup(html,"html.parser")
        for a in soup.find_all("a",href=True):
            link=urljoin(base,a["href"])
            if urlparse(base).netloc in link:
                q.put(link)
        if "?" in url:
            targets.append(url)

def scanner():
    total=len(targets)*len(payloads)
    if total==0:
        return
    count=0

    for url in targets:
        parsed=urlparse(url)
        params=parse_qs(parsed.query)

        for p in params:
            for payload in payloads:
                test=url.replace(params[p][0],payload)
                html=fetch(test)

                if payload in html:
                    result=f"[VULN] {test}"
                    print("\n"+Fore.RED+result)
                    found.append(result)

                count+=1
                progress(count,total)

def save_report():
    name=f"SentinelScan_Report_{int(time.time())}.txt"
    with open(name,"w") as f:
        f.write("SentinelScan — Pro + AI Adaptive Report\n\n")
        if found:
            for v in found:
                f.write(v+"\n")
        else:
            f.write("No obvious vulnerabilities detected.\n")
    print(Fore.GREEN+f"\nReport saved: {name}")

def main():
    banner()
    disclaimer()
    loading()

    target=input(Fore.CYAN+"Target URL: ")

    print(Fore.YELLOW+"\nStarting crawler...\n")
    crawler(target)

    print(Fore.YELLOW+"\nStarting adaptive scan...\n")
    scanner()

    save_report()
    print(Fore.CYAN+"\nScan Completed.")


if __name__=="__main__":
    main()
