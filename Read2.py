import time
import RPi.GPIO as GPIO
import MFRC522
import signal

GPIO.setmode(GPIO.BOARD)

#設定LED pin變數
LED0    = 7   
LED1    = 11
counter = 0

#設定為輸出
GPIO.setup(LED0,GPIO.OUT)
GPIO.setup(LED1,GPIO.OUT)


continue_reading = True

# 當按下 Ctrl + C時結束程式
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# 迴圈檢查是否取得 UID 及授權
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # 檢查是否為授權卡片
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
            GPIO.output(LED0,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED0,GPIO.LOW)
        else:
            print("Authentication error")
            GPIO.output(LED1,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED1,GPIO.LOW)