from file_helper.file_reader import current_client
def client_helper(client_list):
    chunked_list =[(client_list[i::4],i+1) for i in range(4)]
    return chunked_list

