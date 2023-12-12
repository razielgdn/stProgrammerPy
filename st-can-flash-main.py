#st-can-flash-main.py
import argparse
from canLayer.bootloader_comm import *
def main():
    help_string = "Commands available.\ng: get the version and the allowed comands supported by the bootloader. \ni: get chip ID. \nr: read memory where x is 0, 2, 4, 8, 16, 32, 64 or 128. \ns: starts user application code.\nw: write memory with data from filename. \n e: erase memory."
    parser = argparse.ArgumentParser(description="ST flash application. ")
    parser.add_argument("option", choices=["g", "i", "r", "s", "w", "e"], help = help_string)     
    parser.add_argument("-x", type=int, help="Number for the option r.")
    parser.add_argument("-file", help="File to be written in memory.")
    print("ST-Flash though CAN:\nRun as sudo st-can-flash. \n")      
    args = parser.parse_args()
    bootloaderIsOK=start_bootloader()
    print(f"Bootloader started, response: {bootloaderIsOK}")
    print("Option selected:", args.option)
    if bootloaderIsOK:
        if args.option == "g":
            print("g Get the version and allowed commands.")         
        elif args.option == "i":
            print("i Get chip ID.")
            chip_ID_response()            
        elif args.option == "r":
            print(f"r Read memory: x={args.x}")
        elif args.option == "s":
            print("s Starts user application code.")
        elif args.option == "w":
            print("w Write memory.")
        elif args.option == "e":
            print("e Erase memory.")
    else:
        print("Bootloader is not initialized correctly.")    
if __name__ == "__main__":
    main()
