import urllib3   #https://urllib3.readthedocs.io/en/latest/
import json
from texttable import Texttable
http = urllib3.PoolManager()
USER_API_KEY = "R5A5T2S3KHZVKKDT" #replace with your KEY (!!!this is not read key!!!)
try:
    count = 1
    url1 = "https://api.thingspeak.com/channels.json?api_key=%s" %(USER_API_KEY)
    response = http.request('GET',url1)
    data = response.data #byte
    data = data.decode('utf8') #converting byte to string
    data = json.loads(data)
    print("Channels: ")
    for x in data:
        print(str(count)+". " + x['name']) #printing available channels
        count+=1 #keeping count of number of channels
    x = int(input("Select Channel: "))
    n = int(input("Number of Results "))
    #print(data[x-1])
    print("\n")
    channel_id = data[x-1]['id']
    #print("ID: " + str(channel_id))
    print("Description: " + str(data[x-1]['description']))
    print("Created at: " + str(data[x-1]['created_at']))
    print("Public: " + str(data[x-1]['public_flag']))
    READ_KEY = str(data[x-1]['api_keys'][1]['api_key'])
    #print(READ_KEY)
    read_url = "https://api.thingspeak.com/channels/%i/feeds.json?api_key=%s&results=%i" %(channel_id,READ_KEY,n)
    #print(read_url)
    response = http.request('GET',read_url)
    data = response.data
    data = data.decode('utf8') #converting byte to string
    data = json.loads(data)
    keys = list(data["channel"].keys())
    count = 0
    for x in keys:
        if "field" in x:
            count = count +1

    fields = []
    for x in range(count):
        fields.append(str(data["channel"]["field%s" %(x+1)]))

    table = Texttable()
    table.add_row(["entry_id",]+fields+["created_at"])
    for x in data["feeds"]:
        entry_id = x["entry_id"]
        time = x["created_at"]
        for y in range(count):
            fields[y] = str(x["field"+str(y+1)]) #adding each coloumn of data to fields
        
        table.add_row([entry_id]+fields+[time])
    print(table.draw())
except:
    pass