import lynie

filename = "oneline.py"
output_file = "example_output.py"

#Get the one line equivalent of the file
line = lynie.parse_file(filename)

#Write to output file
with open(output_file,"w") as f:
    f.write(line)