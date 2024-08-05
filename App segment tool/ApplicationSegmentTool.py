import pandas as pd
import warnings

class ApplicationSegmentTool:
    def __init__(self, input_file):
        self.input_file = input_file
        self.df = pd.read_csv(self.input_file)
        self.valid_columns = {}
    
    def display_columns(self):
        print("Available columns in the input file:")
        for col in self.df.columns:
            print(col)

    def get_user_mapping(self):
        self.protocol_col = 'Protocol'
        self.app_name_col = input("Enter the column name to map to 'Application Name' (or leave blank): ")
        self.app_fqdn_col = input("Enter the column name to map to 'Application FQDN/IP' (or leave blank): ")
        self.server_ip_col = input("Enter the column name to map to 'Server IP' (or leave blank): ")
        self.tcp_ports_col = input("Enter the column name to map to 'TCP Ports' column based on the Protocol (or leave blank): ")
        self.udp_ports_col = input("Enter the column name to map to 'UDP Ports' column based on the Protocol (or leave blank): ")
        self.app_owner_col = input("Enter the column name to map to 'App Owner Contact' (or leave blank): ")
        self.app_imp_col = input("Enter the column name to map to 'Application Importance' (or leave blank): ")
        self.host_loc_col = input("Enter the column name to map to 'Hosting Location' (or leave blank): ")
        self.env_col = input("Enter the column name to map to 'Environment' (or leave blank): ")
        return self.app_name_col, self.app_fqdn_col, self.server_ip_col, self.tcp_ports_col, self.udp_ports_col, self.app_owner_col, self.app_imp_col, self.host_loc_col, self.env_col

    def validate_columns(self, column_mapping):
        for col_name, user_col in column_mapping.items():
            if user_col in self.df.columns:
                self.valid_columns[col_name] = user_col
            else:
                self.valid_columns[col_name] = None
                print(f"Warning: '{user_col}' is not a valid column name. '{col_name}' will be left blank.")
        return self.valid_columns

    def generate_ports_columns(self):
        if self.protocol_col in self.df.columns:
            self.df['TCP Ports'] = self.df.apply(lambda row: row[self.valid_columns['TCP Ports']] if row[self.protocol_col] and row[self.protocol_col].lower() == 'tcp' else '', axis=1)
            self.df['UDP Ports'] = self.df.apply(lambda row: row[self.valid_columns['UDP Ports']] if row[self.protocol_col] and row[self.protocol_col].lower() == 'udp' else '', axis=1)
            self.valid_columns['TCP Ports'] = 'TCP Ports'
            self.valid_columns['UDP Ports'] = 'UDP Ports'
        else:
            print("Warning: 'Protocol' column not found. TCP and UDP Ports columns will be ignored.")
            self.valid_columns['TCP Ports'] = None
            self.valid_columns['UDP Ports'] = None

    def generate_output(self, output_file='output.csv'):
        output_columns = {key: self.valid_columns[key] for key in self.valid_columns if self.valid_columns[key] is not None}
        output_df = self.df[list(output_columns.values())]
        output_df.columns = output_columns.keys()

        final_columns = ['Application Name', 'Application FQDN/IP', 'Server IP', 'TCP Ports', 'UDP Ports', 'App Owner Contact', 'Application Importance', 'Hosting Location', 'Environment']
        for col in final_columns:
            if col not in output_df.columns:
                output_df[col] = ''

        output_df = output_df[final_columns]
        output_df.to_csv(output_file, index=False)
        print(f"Output file '{output_file}' generated successfully.")
        return output_df

if __name__ == "__main__":

    warnings.filterwarnings("ignore")

    input_file = input("Enter the input file name (e.g., 'qualys.csv'): ")
    tool = ApplicationSegmentTool(input_file)
    
    # Display columns in the input file
    tool.display_columns()
    
    # Get user mapping
    user_mapping = tool.get_user_mapping()
    column_names = ['Application Name', 'Application FQDN/IP', 'Server IP', 'TCP Ports', 'UDP Ports', 'App Owner Contact', 'Application Importance', 'Hosting Location', 'Environment']
    column_mapping = dict(zip(column_names, user_mapping))
    
    # Validate columns
    tool.validate_columns(column_mapping)
    
    # Generate TCP and UDP columns based on protocol
    tool.generate_ports_columns()
    
    # Generate output and save to CSV
    tool.generate_output()
