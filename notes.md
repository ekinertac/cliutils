- python -m SimpleHTTPServer
- curl ifconfig.me
- wget --random-wait -r -p -e robots=off -U mozilla http://www.example.com

List of commands you use most often

history | awk '{a[$2]++}END{for(i in a){print a[i] " " i}}' | sort -rn | head
