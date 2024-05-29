import subprocess
import re

def get_wifi_passwords():
    # Run command to get the list of Wi-Fi profiles
    profiles_output = subprocess.check_output('netsh wlan show profiles', shell=True, encoding='cp850')
    
    # Extract profile names
    profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_output)
    
    wifi_details = []

    for profile in profiles:
        wifi_info = {}
        wifi_info["Profile"] = profile
        
        # Run command to get the details of each profile, including the password
        profile_info_output = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear', shell=True, encoding='cp850')
        
        # Extract the SSID and password
        ssid = re.search(r"SSID name\s*:\s*(.*)", profile_info_output)
        password = re.search(r"Key Content\s*:\s*(.*)", profile_info_output)
        
        wifi_info["SSID"] = ssid.group(1) if ssid else None
        wifi_info["Password"] = password.group(1) if password else None
        
        wifi_details.append(wifi_info)
    
    return wifi_details

if __name__ == "__main__":
    wifi_passwords = get_wifi_passwords()
    for wifi in wifi_passwords:
        print(f"Profile: {wifi.get('Profile')}")
        print(f"SSID: {wifi.get('SSID')}")
        print(f"Password: {wifi.get('Password')}\n")

