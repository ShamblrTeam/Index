import sys
import json
import socket

class TagIndex:
    def __init__(self):
        self.tags = dict()

    def loadTagIndexFromFile(self, filename):
        print "Loading tags into memory..."
        num_tags = 0
        with open(filename, 'r') as file:
            for line in file:
                try:
                    # use rsplit b/c tag_text may have comma
                    parts = line.rstrip('\n').rsplit(',',1)
                    tag_text = str(parts[0]).strip().lower()
                    post_id = int(parts[1])
                    self.loadAssociation(tag_text, post_id)
                    num_tags += 1

                    # give progress reports
                    if num_tags % 1000000 == 0:
                        print str(num_tags) + ' tags loaded...'
                except Exception as e:
                    pass
                    # right now the erros are multiple line tags
                    # pretty rare, though
                    """
                    print 'exception on :' + line
                    print parts
                    print e
                    """
        print "Done loading. " + str(num_tags) + " tags loaded."
        print "There are " + str(len(self.tags)) + ' unique words'
        return True

    def loadAssociation(self, tag_text, post_id):
        if tag_text in self.tags:
            self.tags[tag_text].append(post_id)
        else:
            self.tags[tag_text] = [post_id]
        return True

    def getPostsThatHaveTag(self, tag_text):
        if tag_text not in self.tags:
            return []
        else:
            return self.tags[tag_text]

if __name__ == '__main__':
    tagIndex = TagIndex()
    tagIndex.loadTagIndexFromFile('tags.csv')

    while True:
        s = str(raw_input('find word: '))
        if s == '':
            break
        print 'finding : ' + s
        print tagIndex.getPostsThatHaveTag(s)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('',7777))
        s.listen(1)

        conn = None
        while True:
            conn, address = s.accept()
            data = bytes()
            while True:
                new_data = conn.recv(1024)
                if not new_data:
                    break
                data += new_data
            data = str(data)

            data_obj = {}
            try:
                data_obj = json.loads(data)
            except Exception as e:
                print "Error handling JSON loading"
                print e
            
            response = dict()
            response['worked'] = True
            response['posts'] = []

            print "Working with:"
            print data_obj 

            if 'tag' in data_obj:
                response['posts'] = tagIndex.getPostsThatHaveTag(data_obj['tag'])
            
            print "Ready to send"
            conn.send(json.dumps(response))
            conn.shutdown(socket.SHUT_WR)
            if conn != None:
                conn.close()
                conn = None
            print "done"

    except Exception as e:
        print "Exception in main socket loop"
        print e
