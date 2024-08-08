**Application Segment Import Tool** 


**What does the tool provide?** 

This App Segment Import Tool lets you import ZPA Applications from external sources such as Tenable Nessus, Qualys, Infoblox. The tooling provided in this Repo converts the output of these tools to a format that ZPA App Import accepts 
Each source has its nuances. For example we could not get FQDN, port and vulnerability information in one export from Qualys. We hope that you use the examples provided in this repo will help you extend the tool with any application you have. ZPA App import at the time of writing this document does not do anything with the additional metadata. 

* **Tenable Data: tenable\_data.csv**  
  * Version: 10.5.7  
  * The Tenable scan export has information on vulnerabilities, cvss scores, and associated metadata. The data was obtained by performing a Tenable ‘Discovery scan’ in the lab. 
  * The Tenable Discovery scan helps in identifying all active assets and services running within the network.   
* **Qualys Data: qualys\_data.csv**  
  * Version: 3.18.1  
  * The Qualys scan data export has information on Asset ID, IPV4 addresses, protocol, ports etc,. All the information required for ZPA import was not availbale from a single report in the Qualys Cloud Platform. Assests reports contains information such as ... Vulnerabilities reports has details ... Ports reports gives the insights regaridng the protocol and ports. Hence three different reports were merged in order to get all the information we need.  
  * The three  files: Assets.csv, Vulnerabilities.csv and Ports.csv, can be obtained from Qualys Cloud Platform from the following paths   
         1. Assets.csv \- Vulnerability Management \-\> vulnerabilities \-\> assets   
         2. Vulnerabilities.csv \- Vulnerability Management \-\> vulnerabilities \-\> vulnerability  
         3. Ports.csv \- Vulnerability Management \-\> Assets \-\> Ports/Services

* **Infoblox Data: Infoblox_Data.csv**  
  * Version: 9.0.3
  * License: NIOS, Grid 
  * The data was obtained by performing a Infoblox ‘IP Discovery scan’ in the lab. It includes information such as Host, OS, MAC Address, etc,.   
  * The data is obtained after performing a IP discovery scan on the grid: Data Management -> IPAM -> Network

**Data Preparation**  
   
Tenable Data \- No changes needed. The data obtained from Nessus scan 10.5.7 can be directly used with the tool. 

Qualys data \- The tables Assets.csv and Vulnerabilities.csv are merged on ‘Asset ID’ and thus the obtained table is merged to Ports.csv on ‘IPV4 address’. The final output file is called Qualys\_Data.csv and this can be used with the tool. 

Infoblox Data \- No changes needed. The data obtained from IPAM IP Discovery scan can be directly used with the tool.

**Tool Overview** 

The tool is used for mapping and validating columns in a CSV file based on user input, then processing and generating a new CSV file with the specified structure. It allows customers to configure which columns they want to map to the existing columns of the ZPA template. The user has to input the desired columns to map to the ZPA template columns and the output will be downloaded based on the mapping. 

Properties: 

1. Maps user-specified column names to a predefined set of ZPA column names.  
1. Validates the user-specified columns against the DataFrame columns.  
1.  Generates TCP and UDP port columns based on the 'Protocol' column.  
1. Saves the processed DataFrame \`output\_df\` to a new CSV file named \`output.csv\`that can be imported in ZPA. 

**ZPA Import Template** 

The following is the Import template for ZPA: 

| Application Name | Application FQDN/IP | Server IP | TCP Ports | UDP Ports | App Owner Contact | Application Importance | Hosting Location | Environment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |



**To run the code**

1. Make sure to have Python 2.7 or above on your computer. Follow here: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
2. Have pip installed on your computer (Comes with versions greater than Python 2.7.9). If not follow here: [https://pip.pypa.io/en/stable/installing/\#do-i-need-to-install-pip](https://pip.pypa.io/en/stable/installing/\#do-i-need-to-install-pip)  
3. To view the results of the tool, find the newly created file: Output.csv.

