import requests
import time


# script should be used in a crontab like this:
# */15 * * * * /usr/bin/python3 /path/to/script/fetch_and_send.py
url = "https://app.cituro.com/bookingService"

headers = {
    "Content-Type": "text/x-gwt-rpc; charset=utf-8",
    "X-GWT-Permutation": "EDAC99005FA3C579ED0FD10B62F1E796",
    "X-GWT-Module-Base": "https://app.cituro.com/bookappointment/",
    "Origin": "https://app.cituro.com",
    "Referer": "https://app.cituro.com/booking/5278312",
    "User-Agent": "Mozilla/5.0"
}

results = []
payloads = [
    "payload_kurzberatung.txt",
    "payload_50min.txt",
    "payload_hmt.txt"]


results = []
payloads = [
    "payload_kurzberatung.txt",
    "payload_50min.txt",
    "payload_hmt.txt"]

"""
wenn es keine Termine gibt, dann siehts so aus:
//OK[0,1,["java.util.ArrayList/4159755760"],0,7]

wenn es welche gibt, dann so:
//OK[21,-12,2026,0,8,0,11,11,14,0,0,16,23,2026,0,8,50,11,11,14,0,0,"Z6HmxRg",13,"CX7",0,0,0,0,0,"Z_wDNKA",13,-6,1,8,0,0,0,0,0,0,0,0,7,0,22,5,0,-4,0,0,3,0,2,21,-12,2026,0,8,0,13,4,14,0,0,16,20,2026,0,8,50,13,4,14,0,0,"Z6Hmp8w",13,"CX7",0,0,0,0,0,"Z_MbiuA",13,-6,1,8,0,0,0,0,0,0,0,0,7,0,19,5,0,-4,0,0,3,0,2,18,0,17,2026,0,8,0,9,4,14,0,0,16,15,2026,0,8,50,9,4,14,0,0,"Z5tVRy4",13,"CX7",0,0,0,0,0,"Z_LknGA",13,0,12,11,0,10,9,1,8,0,0,0,0,0,0,0,0,7,0,6,5,0,10,4,0,0,3,0,2,3,1,["java.util.ArrayList/41597557
# """
def termin_available(response):
    if len(response.text) > 48:
        return True
    else:
        return False
    
def send_msg_to_ntfy(msg, topic):
    ntfy_url = f"https://ntfy.sh/{topic}"
    requests.post(ntfy_url, data=msg.encode('utf-8'), headers={"Click": "https://app.cituro.com/booking/5278312"})




def main():
    try:
        with open(payloads[0], "r") as f:
            payload = f.read()
        response = requests.post(url, headers=headers, data=payload)
        if termin_available(response):
            print("sending notification for kurzberatung")
            send_msg_to_ntfy("Kurzberatung verfügbar!", "psychosoziale_kurzberatung")

        with open(payloads[1], "r") as f:
            payload = f.read()
        response = requests.post(url, headers=headers, data=payload)
        if termin_available(response):
            print("sending notification for erstgeprächstermin")
            send_msg_to_ntfy("Erstgeprächstermin verfügbar!", "psychosoziale_beratung")

        with open(payloads[2], "r") as f:
            payload = f.read()
        response = requests.post(url, headers=headers, data=payload)
        if termin_available(response):
            print("sending notification for erstgeprächstermin (HMT)")  
            send_msg_to_ntfy("Erstgeprächstermin (HMT) verfügbar!", "psychosoziale_beratung_hmt")
    except Exception as e:
        print(f"An error occurred: {e}")
        send_msg_to_ntfy(f"An error occurred: {e}", "psychosoziale_beratung_debug")

if __name__ == "__main__":
    main()