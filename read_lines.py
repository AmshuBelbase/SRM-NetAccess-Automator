def cred(credpath): 
    lines_list = [] 
    with open(credpath, 'r') as file: 
        for line in file: 
            lines_list.append(line.strip())
    return lines_list

if __name__ == "__main__":
    # Print the list to verify
    print(cred("cred.txt"))

