import re
from datetime import datetime

request_type = re.compile(r'] (\w*) ')
error_text = re.compile(r'ERROR (.*) for')
error_id = re.compile(r'ERROR .* for >Request (.*)<')
request_state = re.compile(r'INFO (.*) processing')
request_start_time = re.compile(r'\[(.*)] INFO Started')
request_start_id = re.compile(r'Started processing of >Request (.*)<')
request_finished_time = re.compile(r'\[(.*)] INFO Finished')
request_finished_id = re.compile(r'Finished processing of >Request (.*)<')

class Error:
    def __init__(self, id, text):
        self.id = id
        self.text = text

class Request:
    def __init__(self, id, time):
        self.id = id
        self.time = time

class MessagesType:
    info = "INFO"
    started = 'Started'
    finished = 'Finished'
    error = 'ERROR'

def request_and_error_lists(list):
    global started_list, finished_list, error_list
    started_list = []
    finished_list = []
    error_list = []
    for elem in list:
        if request_type.findall(elem)[0] == MessagesType.info:
            if request_state.findall(elem)[0] == MessagesType.started:
                request_start = Request(
                    int(request_start_id.findall(elem)[0]),
                    datetime.strptime(request_start_time.findall(elem)[0], "%Y-%m-%d %H:%M:%S.%f"))
                started_list.append(request_start)
            if request_state.findall(elem)[0] == MessagesType.finished:
                request_finished = Request(
                    int(request_finished_id.findall(elem)[0]),
                    datetime.strptime(request_finished_time.findall(elem)[0], "%Y-%m-%d %H:%M:%S.%f"))
                finished_list.append(request_finished)
        if request_type.findall(elem)[0] == MessagesType.error:
            error = Error(int(error_id.findall(elem)[0]),
                          error_text.findall(elem)[0])
            error_list.append(error)

    return started_list, finished_list, error_list

def sorted_key(request_list):
    return request_list.id

def requested_list(started_list, finished_list):
    request_list = []
    for obj in started_list:
        for obj2 in finished_list:
            if obj.id == obj2.id:
                request = Request(obj.id, (obj2.time - obj.time).total_seconds())
                request_list.append(request)
                break
        if obj.id != obj2.id:
            request = Request(obj.id, '-1.000')
            request_list.append(request)
    sorted_request_list = sorted(request_list, key = sorted_key)
    return sorted_request_list

def print_request_list(list, error_list):
    for elem in list:
        print("%s %s: %s" % ("Request", elem.id, elem.time))
    print("\nErrors:")
    for elem in error_list:
        print("%s %s: %s" % ("Request", elem.id, elem.text))
def works_with_file(file_name):
    f = open(file_name)
    text = f.read()
    f.close()
    return text


def main():
    text_list = works_with_file('Trace.txt').split('\n')
    request_and_error_lists(text_list)
    print_request_list(requested_list(started_list, finished_list), error_list)

if __name__ == "__main__":
    main()