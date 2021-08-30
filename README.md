# Lynie
An easy to use python to oneline-icator.

Support for atleast `Python 3.8.7`. 
Unsure for other versions.

## Usage
Lynie only has one function that has to be called in order to turn a filename into a single line.

Import `lynie`, and call `lynie.parse_file(filename)`. It will return the one line in the form of a string.
With this string you can write it to a file.
Here's a simple example of how you can use it (File: `example.py`):
```py
import  lynie

filename = "oneline.py"
output_file = "example_output.py"

#Get the one line equivalent of the file
line = lynie.parse_file(filename)

#Write to output file
with  open(output_file,"w")  as  f:
	f.write(line)
```

## Known problems

As of right now, there's a few things Lynie can't do.

- With
- Try except
- While

`With` is a difficult thing to do as it's impossible to do in a single line. It also doesn't have a single line equivalent.

`Try Except` Is something that might be possible. However as of right now it's not in Lynie as it's syntax is uncompatible with list comprehensions.

`While` Is possible by using a recursive function. Though i haven't implemented it yet, it will come soon.

___
There's also a different problem that Lynie can do, however not perfectly.
Starred function arguments is something that i've had problems with, but i haven't found a solution to.
`def some_function(*list_input, argument=False, argument2=True)`
Lynie will only be able to see `*list_input` and completely ignores `argument` and `argument2`.
This is due to `ast` not seeing anything past the starred argument. However it will still see kwarg arguments.
`(*list_input, **kwargs)` will work.
So you can "Optimize" your code for Lynie to still take those arguments.
```py
def some_func(*inp, output=False):
	if output:
		print(inp)

#Could become something like:

def some_func(*inp,**kwargs):
	#Put the default values in the data dict
	data = {"output":False}

	#Update data with kwargs. Overwriting the default one if 'output' is in kwargs.
	#But keeps the default value if it isn't defined
	data.update(kwargs)

	#Set `output` to the value in the dict
	output = data['output']
	
	#Rest of code
	if output:
		print(inp)
```
___
If you have any other problems, feel free to raise an issue on this github repo.

## What to use it for
Honestly, i wouldn't know.
Though, judging by the fact that you've found this Repo, you already would have some use for it.
May that be obfuscation, just for fun, or just to see if it was possible. You're here!

## Why
I'm in a [discord server](https://discord.gg/ZwQgNfZa) where they have daily python challenges, and most people there try to make those challenges in as little code as possible. Or mainly try to do it within one line.

And while doing that, i suddenly realized you could pretty much make anything in one line.
So i did some experimenting with it, by turning some of my functions of different modules into a single line.
And succeeded with all of them.

Then i had the bright idea to make a module that turns other scripts into a single line.
It was a very daunting first few hours. As i had no clue how i was going to even begin doing such a thing.
As everything in python would need to be supported, in a way that everyone can use it, not only for my code.

Though, thankfully, my first try worked good. Good enough to have continued it to the point where it is now.
There probably are better ways of doing this, however I'm proud enough of myself to have accomplished this to begin with. Maybe later I'll make a better version of it.

### Change log
1.0:

	Added:
		- Assignments
		- Functions
		- For loops
		- If / Else statements
		- f strings
		- function calls
		- imports
		- lambda functions

1.1:

	Added:
		- Example file	
		- Comments

1.2:

	Added:
		- Modulo operator

	Changed:
		- Example files

1.3:

	Added:
		- List comprehension support
		- Description for `parse_file` function.

	Fixed:
		- Output for constants
		- Function argument parsing
		- If Else output being a string instead of code
		- Variable assign parsing
		- Function return parsing

1.3.5:

	Added:
		- A testing script
		- Folder with scripts to test

	Changed:
		- Made Lynie a PIP module
		- Made changes.txt have shorter version numbers
		- _get_args to be more readable