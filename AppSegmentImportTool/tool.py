import pandas as pd
import warnings

class ApplicationSegmentTool:
    def __init__(self, input_file, template_file):
        self.input_file = input_file
        self.template_df = pd.read_csv(template_file)
        self.df = pd.read_csv(self.input_file)
        self.valid_columns = {}
    
    def display_columns(self):
        print("Available columns in the input file:")
        for col in self.df.columns:
            print(col)

    def display_template_columns(self):
        print("Columns in the template file:")
        for col in self.template_df.columns:
            print(col)

    def get_template_columns(self):
        return self.template_df.columns.tolist()

    def get_user_mapping(self):
        self.display_template_columns()  # Display template columns before asking for mapping
        template_columns = self.get_template_columns()
        column_mapping = {}
        for col in template_columns:
            user_col = input(f"Enter the column name to map to '{col}': ")
            column_mapping[col] = user_col
        return column_mapping

    def validate_columns(self, column_mapping):
        for col_name, user_col in column_mapping.items():
            if user_col in self.df.columns:
                self.valid_columns[col_name] = user_col
            else:
                self.valid_columns[col_name] = None
                print(f"Warning: '{user_col}' is not a valid column name. '{col_name}' will be left blank.")
        return self.valid_columns

    def compress_ports(self, ports_str):
        if isinstance(ports_str, int):
            return str(ports_str)
        elif isinstance(ports_str, str):
            ports = sorted(set(map(int, ports_str.split(','))))
        else:
            return ''

        compressed_ports = []
        range_start = ports[0]
        range_end = ports[0]
        
        for port in ports[1:]:
            if port == range_end + 1:
                range_end = port
            else:
                if range_start == range_end:
                    compressed_ports.append(str(range_start))
                else:
                    compressed_ports.append(f"{range_start}-{range_end}")
                range_start = port
                range_end = port
        
        # Add the final range
        if range_start == range_end:
            compressed_ports.append(str(range_start))
        else:
            compressed_ports.append(f"{range_start}-{range_end}")
        
        return ','.join(compressed_ports)

    def handle_protocol_ports(self):
        if 'Protocol' in self.df.columns:
            tcp_port_col = self.valid_columns.get('TCP Ports')
            udp_port_col = self.valid_columns.get('UDP Ports')

            if tcp_port_col and udp_port_col:
                if tcp_port_col == udp_port_col:
                    # Same column for both TCP and UDP Ports, check protocol
                    self.df['TCP Ports'] = self.df.apply(
                        lambda row: self.compress_ports(row[tcp_port_col]) if row['Protocol'].strip().lower() == 'tcp' else '', axis=1)
                    self.df['UDP Ports'] = self.df.apply(
                        lambda row: self.compress_ports(row[udp_port_col]) if row['Protocol'].strip().lower() == 'udp' else '', axis=1)
                else:
                    # Different columns for TCP and UDP Ports
                    self.df['TCP Ports'] = self.df.apply(lambda row: self.compress_ports(row[tcp_port_col]), axis=1)
                    self.df['UDP Ports'] = self.df.apply(lambda row: self.compress_ports(row[udp_port_col]), axis=1)

            # Update the valid_columns dictionary to include TCP and UDP Ports
            self.valid_columns['TCP Ports'] = 'TCP Ports'
            self.valid_columns['UDP Ports'] = 'UDP Ports'
        else:
            print("Warning: 'Protocol' column not found in the input file. TCP and UDP Ports columns will be ignored.")
            self.valid_columns['TCP Ports'] = None
            self.valid_columns['UDP Ports'] = None

    def generate_output(self):
        output_file = input("Enter the output file name with path (e.g., '/path/to/output.csv'): ")
        if not output_file:
            output_file = 'output.csv'  # Default file name

        output_columns = {key: self.valid_columns[key] for key in self.valid_columns if self.valid_columns[key] is not None}
        output_df = self.df[list(output_columns.values())]
        output_df.columns = output_columns.keys()

        # Ensure all columns from the template are present in the final output
        for col in self.template_df.columns:
            if col not in output_df.columns:
                output_df[col] = ''

        output_df = output_df[self.template_df.columns]
        output_df.to_csv(output_file, index=False)
        print(f"Output file '{output_file}' generated successfully.")
        return output_df

if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    input_file = input("Enter the input file name (e.g., 'qualys.csv'): ")
    template_file = input("Enter the template file name (e.g., 'template.csv'): ")
    tool = ApplicationSegmentTool(input_file, template_file)
    
    # Display columns in the input file
    tool.display_columns()
    
    # Get user mapping based on template
    user_mapping = tool.get_user_mapping()
    
    # Validate columns
    tool.validate_columns(user_mapping)
    
    # Handle Protocol and Ports columns
    tool.handle_protocol_ports()
    
    # Generate output and save to CSV
    tool.generate_output()
