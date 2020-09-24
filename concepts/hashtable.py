#Suppose we want to count the frequency of all the characters in a sting S

S = input("Please enter a string:\n")

print("you entered:", S)
print("length of string:", len(S))
#We construct an frequency array of size 26 to hash the 26 characters
#to the indicies of the array using a hash function

Frequency = []*26

def hashfunc(S):
    return S


def cntfreq(S):
    for i in range(len(S)):
        index = hashfunc(S[i])
        Frequency[index] += 1
        
        print(Frequency)

        for i in range(0,26):
            print("letters and stuff", Frequency[i])
            
cntfreq(S)
