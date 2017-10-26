import csv
import sys

def main(fn):
    filecontent=[]
    fname = fn

    try:
        with open(fname,"rb") as reader:
            filecontent = reader.read()
    except:
        print "Error"


    dictLogList = []
    dictitem = {}

    for i in filecontent.splitlines(True):
        if i.startswith("\r\n"):
            dictitem = {'time':"",
                        'event':"",
                        'ip_user':"",
                        'description':"",
                        "message":"",
                        'path':"",
                        'source':"",
                        'srcport':"",
                        'destination':"",
                        'dstport':"",
                        'matched_rule':""}

        if i.startswith("Time"):
            dictitem['time'] = i.split("\t")[1].replace("\r\n","")
        if i.startswith("Event"):
            dictitem['event']  = i.split("\t")[1].replace("\r\n","")
        if i.startswith("IP"):
            dictitem['ip_user']  = i.split("\t")[1].replace("\r\n","")

        if i.startswith("Description"):
            dictitem['description']  = i.split("\t")[1].replace("\r\n","")
        if i.startswith("Path"):
            dictitem['path'] = i.split("\t")[1].replace("\r\n","")
        if i.startswith("Message"):
            mess = i.split("\t")[1]
            msg_part1 = mess.split(" - ")[0]
            dictitem['message'] = msg_part1
            msg_part2= mess.split(" - ")[1]

            if msg_part2.find(":") > 0:
                sourcestart = msg_part2.find("Source")
                destinationstart = msg_part2.find("Destination")
                lineend=msg_part2.find("\r\n")
                sourcestring = msg_part2[sourcestart:destinationstart].replace("Source","").split(":")[0]
                sourceport = msg_part2[sourcestart:destinationstart].replace("Source","").split(":")[1]
                dictitem['source'] = sourcestring
                dictitem['srcport']= sourceport.replace("(","").replace(")","")

                dststring = msg_part2[destinationstart:lineend].replace("Destination", "").split(":")[0]
                dstport = msg_part2[destinationstart:lineend].replace("Destination", "").split(":")[1]
                dictitem['destination'] = dststring
                dictitem['dstport'] = dstport.replace("(","").replace(")","")
            else:
                sourcestart = msg_part2.find("Source")
                destinationstart = msg_part2.find("Destination")
                lineend = msg_part2.find("\r\n")
                sourcestring = msg_part2[sourcestart:destinationstart].replace("Source", "").split(" ")[0]

                dictitem['source'] = sourcestring
                dictitem['srcport'] = ""

                dststring = msg_part2[destinationstart:lineend].replace("Destination", "").split(":")[0]

                dictitem['destination'] = dststring
                dictitem['dstport'] = ""

        if i.startswith("Matched"):
            dictitem['matched_rule'] = i.split("\t")[1].replace("\r\n","")
            dictLogList.append(dictitem)
            #print dictitem
            dictitem={}

    # write CSV
    with open('mycsv.csv','w') as f:
        w = csv.DictWriter(f, ["time","event","ip_user","message","source","srcport","destination","dstport","path","description","matched_rule"])
        w.writeheader()
        w.writerows(dictLogList)






if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "error - name the input file; Output file will be written to current directory."
    else:
        main(sys.argv[1])
