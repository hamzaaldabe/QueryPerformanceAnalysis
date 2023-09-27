import paramiko
import argparse

def run_sql_query(sql_file, database_name, ssh_host, ssh_username, ssh_password):
    try:

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    
        ssh_client.connect(ssh_host, username=ssh_username, password=ssh_password)

        psql_command = f'psql -d {database_name} -a -f {sql_file}'
        stdin, stdout, stderr = ssh_client.exec_command(psql_command)

  
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))

        ssh_client.close()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SQL query on a remote server via SSH")
    parser.add_argument("sql_file", help="Path to the SQL file")
    parser.add_argument("database_name", help="Name of the database to connect to")
    parser.add_argument("ssh_host", help="SSH server hostname or IP address")
    parser.add_argument("ssh_username", help="SSH username")
    parser.add_argument("ssh_password", help="SSH password")

    args = parser.parse_args()

    run_sql_query(args.sql_file, args.database_name, args.ssh_host, args.ssh_username, args.ssh_password)
