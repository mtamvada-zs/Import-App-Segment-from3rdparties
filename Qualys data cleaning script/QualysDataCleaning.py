import pandas as pd
import warnings

class QualysDataCleaning:
    def __init__(self, vm_vulns_file, av_vulns_file, ports_file):
        self.vm_vulns_file = vm_vulns_file
        self.av_vulns_file = av_vulns_file
        self.ports_file = ports_file
        
        self.df_vm_vulns = pd.read_csv(self.vm_vulns_file)
        self.df_av_vulns = pd.read_csv(self.av_vulns_file)
        self.df_ports = pd.read_csv(self.ports_file)
    
    def display_columns(self, df):
        print("Available columns in the input file:")
        for col in df.columns:
            print(col)

    def split_ipv4_addresses(self, df, column):
        new_rows = []
        for index, row in df.iterrows():
            addresses = row[column].split(',')
            for address in addresses:
                new_row = row.copy()
                new_row[column] = address.strip()
                new_rows.append(new_row)
        new_df = pd.DataFrame(new_rows)
        return new_df
    
    def merge_dataframes(self):
        df_av_split = self.split_ipv4_addresses(self.df_av_vulns, 'IPV4 Addresses')
        merged_df1_df2 = pd.merge(df_av_split, self.df_vm_vulns, on='Asset Id', how='outer')
        merged_all = pd.merge(merged_df1_df2, self.df_ports, left_on='IPV4 Addresses', right_on='IP', how='outer')
        return merged_all
    
    def prioritize_rows(self, df):
        def select_row(group):
            non_null_rows = group.dropna(subset=['Port_y', 'Protocol_y'])
            if not non_null_rows.empty:
                return non_null_rows.iloc[0]
            else:
                return group.iloc[0]
        return df.groupby('IP', group_keys=False).apply(select_row)
    
    def clean_data(self):
        merged_all = self.merge_dataframes()
        df_final_unique = self.prioritize_rows(merged_all)
        
        df_final_unique['Port_y'] = pd.to_numeric(df_final_unique['Port_y'], errors='coerce').fillna(0).astype(int)
        df_final_unique['Port_y'] = df_final_unique['Port_y'].replace(0, '')
        
        df_final_unique = df_final_unique.rename(columns={'Protocol_y': 'Protocol', 'Port_y': 'Port'})
        return df_final_unique
    
    def save_to_csv(self, output_df, output_file):
        output_df.to_csv(output_file, index=False)
        print(f"Output file '{output_file}' generated successfully.")
    
    def run(self, output_file='qualys.csv'):
        df_final_unique = self.clean_data()
        self.save_to_csv(df_final_unique, output_file)


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    
    vm_vulns_file = input("Enter the VM vulns file name (e.g., 'VM_vulns_sanse3sp.csv'): ")
    av_vulns_file = input("Enter the AV vulns file name (e.g., 'AV_assets_sanse3sp.csv'): ")
    ports_file = input("Enter the ports file name (e.g., 'ports_services_sanse3sp.csv'): ")
    
    tool = QualysDataCleaning(vm_vulns_file, av_vulns_file, ports_file)
    tool.run()