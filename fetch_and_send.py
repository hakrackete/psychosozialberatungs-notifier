import requests
import time

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

def termin_available(response):
    if len(response.text) > 48:
        return True
    else:
        return False
    
def send_msg_to_ntfy(msg, topic):
    ntfy_url = f"https://ntfy.sh/{topic}"
    requests.post(ntfy_url, data=msg.encode('utf-8'), headers={"Click": "https://app.cituro.com/booking/5278312"})




def main():
    while True:
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
        
        
        time.sleep(15 * 60)  # Wait for 60 seconds before checking again
    
if __name__ == "__main__":
    main()