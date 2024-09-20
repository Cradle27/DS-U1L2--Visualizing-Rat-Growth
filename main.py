import ratlab
import matplotlib.pyplot as plt

def main():
  ratlab.main()
  file = "gen_large.txt"
  f = open(file, 'r')
  largests = f.read()
  largests = largests.split(",")
  largests = list(map(int, largests))
  f.close()
  file = "gen_small.txt"
  f = open(file, 'r')
  smallests = f.read()
  smallests = smallests.split(",")
  smallests = list(map(int, smallests))
  f.close()
  file = "gen_avg.txt"
  f = open(file, 'r')
  avgs = f.read()
  avgs = avgs.split(",")
  avgs = list(map(int, avgs))
  f.close()
  print(f"\n{largests}\n\n{smallests}\n\n{avgs}")
if __name__ == "__main__":
  main()