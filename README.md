# GVE DevNet ISE Session Re-Authentication Script 

This prototype python script reads in endpoint devices from ISE and triggers a session re-authentication by connecting to the device's switch and executing IOS CLI commands. Devices are read in via a csv file obtained from the ISE dashboard, then a SSH connection is established to each connected switch. Once connected, IOS 'clear session' commands are executed on the switch, and finally the results are returned to the console.

## Contacts
* Trevor Maco (tmaco@cisco.com)
* Gerardo Chaves (gchaves@cisco.com)

## Solution Components
* Python 3.9
* Netmiko
* ISE


## Installation/Configuration

1. Clone this repository with `git clone https://github.com/gve-sw/gve_devnet_ise_session_re-authentication_script` and open the directory of the root repository.

2. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).

3. Install the required Python libraries with the command:
   ``` bash
   pip3 install -r requirements.txt
   ```

4. Open the `.env` file, and add the switch credentials that will be used during the SSH connections as environment variables.
   
   **Note:** This script relies on multithreading which can result in simultaneous SSH connections to a single switch. Enter the maximum simultaneous connections allowed in the 'MAX_THREADS' variable (a value of 1 equates to synchronous execution and is recommended if there are any errors) 
    
    ``` python
    SWITCH_USERNAME = "<username>" # username for ssh connection
    SWITCH_PASSWORD = "<password>" # password for ssh connection

    MAX_THREADS = 10 # the number of simultaneously connected ssh sessions the switches support
    ```

## Usage

1. Before running this script, obtain the csv file from ISE with the following steps (refer to the screenshots for more information):

   1. Access the ISE dashboard and navigate to `Context Visibility > Endpoints`
   2. Select the tab you are interested in grouping the endpoints by (`Authentication`, `BYOD`, etc.)
   3. Apply any additional filtering to the table of endpoints, then click `Export` (either `Export Selected` or `Export All`)


    **Note:** It's possible to create your own csv file if it includes the following 3 *case sensitive* fields: 

    * MACAddress
    * NAS-IP-Address (**this is the connected switch IP**)
    * NAS-Port-Id (**this is the connected switch port**)


2. To run the script enter the command followed by the csv file.

    ``` bash
    python3 main.py sample.csv
    ```

# Additional Resources

* Netmiko
  * Overview: https://pynet.twb-tech.com/blog/netmiko-python-library.html
  * Project Github Page: https://github.com/ktbyers/netmiko
* Python: 
  * Main Tutorial: https://www.w3schools.com/python/
  * Python Concurrency (Futures): https://rednafi.github.io/digressions/python/2020/04/21/python-concurrent-futures.html

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

Access the Endpoint Section of the ISE Dashboard
![/IMAGES/MainMenu.png](/IMAGES/MainMenu.png)

Select Grouping Method
![/IMAGES/EndpointGrouping.png](/IMAGES/EndpointGrouping.png)

Export CSV
![/IMAGES/ExportTab.png](/IMAGES/ExportTab.png)


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
