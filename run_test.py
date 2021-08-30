import lynie

directory = "tests/"
files = [
    "var_assign.py",
    "ifelse.py",
    "loops.py",
    "imports.py",
    "function.py",
    "list_comp.py",
    "nested.py"
]

for file in files:
    #Parse file
    out = lynie.parse_file(directory+file)

    print("_"*20)
    print(file,'\n')

    # Run parsed code to see if it works
    try:
        eval(out)
    except Exception as e:
        #Print error and parsed code on failure
        print(f"Error in file: {file}.({e})\n\nCODE:\n{out}\n\nQuitting")
        exit()

    print(f"\n{file} - OK")
    print(f"{out}")

print("_"*20)
print(len(files),'Tests OK')