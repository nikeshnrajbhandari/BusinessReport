from helpers import make_dir, del_residue_files, client_list, credentail
from base_class import get_driver

def main():
    make_dir()
    del_residue_files()
    client = client_list(1)
    print(client)
    
    
if __name__ == '__main__':
    main()