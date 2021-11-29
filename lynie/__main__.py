import lynie, sys, os

def main():
    if len(sys.argv) <= 1:
        print("Usage:")
        print("lynie [file] [output : optional]")
        exit()

    file = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    file = file+'.py' if not file.endswith(".py") else file
    

if __name__ == "__main__":
    main()