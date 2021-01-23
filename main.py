from df import DataParser
import os

if __name__ == "__main__":
    print("Input file location in full:")
    path = input()
    print("Input the number of clusters --- keep it sane:")
    clusters = input()

    parser = DataParser(path.strip(), clusters.strip())

    print("1. Output files separated by route and day\n2. Output files separated by route, day, and cluster label\n3. Output a single file with labels\n4. All of above. ")

    mode = input()

    parser.operate(mode.strip())

    print("Done!")

    os.system("pause")