import matplotlib.animation as animation
import subprocess
import matplotlib.pyplot as plt
import sys


def ping_gen(host: str, frequency: str):
    proc = subprocess.Popen(
        ['ping', '-n', '-i', frequency, host], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        outstr = str(line.rstrip())
        pos = outstr.find('time')
        if pos != -1:
            yield float(outstr[pos+5:][:-4])



arg_len = len(sys.argv)
host = 'google.com'
freq = 500
if arg_len == 2:
    host = sys.argv[1]
if arg_len == 3:
    freq = int(sys.argv[2])


float_freq = freq/1000
offset_seconds = int(30/float_freq)
ping_g = ping_gen(host, str(float_freq))
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


def animate(i, xs, ys):
    temp_c = next(ping_g)

    xs.append(i)
    ys.append(temp_c)

    xs = xs[-offset_seconds:]
    ys = ys[-offset_seconds:]

    ax.clear()
    ax.plot(xs, ys)

    plt.title('Ping graph')
    plt.ylabel('Ping')


ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=freq)
plt.show()
