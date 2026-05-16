def StringProcessor(sample:str):
    print(f"String being Processed is {sample}")
    completestring = ""
    lowersample = sample.lower()
    for x,y in enumerate(sample):
        scount = lowersample.count(y.lower())
        formatstring = f"{y}({x})-{scount}"
        completestring += formatstring
        print(formatstring)
    print(completestring)


if __name__ == "__main__":
    StringProcessor("HeLLo")