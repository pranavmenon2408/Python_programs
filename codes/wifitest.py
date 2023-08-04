import os  
# scanning the available Wi-Fi networks  
os.system('cmd /c "netsh wlan show networks"')  
# providing the Wi-Fi name as input  
router_name = input('Input Name/SSID of the Wi-Fi network we would like to connect: ')  
# connecting to the provided Wi-Fi network  
os.system(f'''cmd /c "netsh wlan connect name = {router_name}"''')  
print("If the system is not connected yet, try reconnecting to an earlier connected SSID!")  