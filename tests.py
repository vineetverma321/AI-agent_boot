# from functions.get_files_info import get_files_info

# result = get_files_info("calculator", ".")
# print(result)
# print("")

# print(get_files_info("calculator", "pkg"))
# print("")

# print(get_files_info("calculator", "/bin"))
# print("")

# print(get_files_info("calculator", "../"))
# print("")



# from functions.get_file_content import get_file_content

# result = get_file_content("calculator", "lorem.txt")
# print(result)
# print("")

# result = get_file_content("calculator", "main.py")
# print(result)
# print("")

# result = get_file_content("calculator", "pkg/calculator.py")
# print(result)
# print("")

# result = get_file_content("calculator", "/bin/cat")
# print(result)
# print("")

# result = get_file_content("calculator", "pkg/does_not_exist.py") 
# print(result)
# print("")



# from functions.write_file import write_file
    
# result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# print(result)
# print("")

# result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# print(result)
# print("")

# result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
# print(result)
# print("")



from functions.run_python_file import run_python_file

print(run_python_file("calculator", "main.py") )
# (should print the calculator's usage instructions)

print(run_python_file("calculator", "main.py", ["3 + 5"]) )
# (should run the calculator... which gives a kinda nasty rendered result)

print(run_python_file("calculator", "tests.py"))

print(run_python_file("calculator", "../main.py") )
# (this should return an error)

print(run_python_file("calculator", "nonexistent.py") )
# (this should return an error)