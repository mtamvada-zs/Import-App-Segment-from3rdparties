**Application Segment Import Tool** 

**Problem Statement**

ZPA’s current application discovery poses a security risk because to initially discover which applications are being accessed within an organization, it asks the customer to put in wildcard app segments which means that for a period of time, the access is open to everyone until the user defines who is supposed to access them. This practice contradicts ZTNA principles "never trust, always verify.”

**Proposed Solution** 

The proposed solution is the App Segment Import Tool which imports applications from external sources (ex. Tenable, Qualys, ServiceNow, etc.) and leverages ZPA to accurately identify and categorize apps without the need for wildcard segments which allows us to establish granular access policies from the start sticking to ZTNA principle. 

**Data Sources** 

This project is a Proof of Concept and the tool uses applications data from the following external sources:

* **Tenable Data: tenable\_data.csv**  
  * Version: 10.5.7  
  * A ‘Discovery scan’ was conducted using Tenable in the Zscaler lab. The data includes detailed information on vulnerabilities, Cvss scores, and associated metadata.  
  * The Tenable Discovery scan helps in identifying all active assets and services running within the network.   
* **Qualys Data: qualys\_data.csv**  
  * Version: 3.18.1  
  * The data was obtained by performing a Qualys ‘Network scan’ in the lab. It includes information on Asset ID, IPV4 addresses, protocol, ports etc,.   
  * There are three primary files: Assets.csv, Vulnerabilities.csv and Ports.csv. The files can be obtained from Qualys Cloud Platform from the following paths   
1. Assets.csv \- Vulnerability Management \-\> vulnerabilities \-\> assets   
1. Vulnerabilities.csv \- Vulnerability Management \-\> vulnerabilities \-\> vulnerability  
1. Ports.csv \- Vulnerability Management \-\> Assets \-\> Ports/Services

**Data Preparation**  
   
Tenable Data \- No changes needed. The data obtained from Nessus scan 10.5.7 can be directly used with the tool. 

Qualys data \- The tables Assets.csv and Vulnerabilities.csv are merged on ‘Asset ID’ and thus the obtained table is merged to Ports.csv on ‘IPV4 address’. The final output file is called Qualys\_Data.csv and this can be used with the tool. 

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

Note: The fields Application FQDN/IP, TCP Ports, UDP Ports are mandatory while mapping. 

**To run the code**

1. Make sure to have Python 2.7 on your computer. Follow here: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
1. Have pip installed on your computer (Comes with versions greater than Python 2.7.9). If not follow here: [https://pip.pypa.io/en/stable/installing/\#do-i-need-to-install-pip](https://pip.pypa.io/en/stable/installing/\#do-i-need-to-install-pip)  
1. To view the results of the tool, find the newly created file: Output.csv to view the results.

