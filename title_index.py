import sys
import json
import socket

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now','lol', 'lolz','lawl','jk','haha','ha','hah','hahah','hahaha','da','']

class TitleIndex:
    def __init__(self):
        self.tags = dict()

    def loadTitleIndexFromFile(self, filename):
        print "Loading titles into memory..."
        num_words = 0
        stop_words = 0
        with open(filename, 'r') as file:
            for line in file:
                try:
                    # assuming its "title, post_id"
                    # use rsplit b/c tag_text may have comma
                    parts = line.rstrip('\n').rsplit(',',1)
                    # @todo: remove non alphanumeric
                    title = str(parts[0]).strip().lower()
                    post_id = int(parts[1])
                    
                    words = title.split(' ')
                    for word in words:
                        if word not in stopwords:
                            self.loadAssociation(word, post_id)
                            num_words += 1
                        else:
                            stop_words += 1

                    # give progress reports
                    if num_words % 1000000 == 0:
                        print str(num_words) + ' words loaded...'
                except Exception as e:
                    pass
                    # right now the erros are multiple line tags
                    # pretty rare, though
                    """
                    print 'exception on :' + line
                    print parts
                    print e
                    """

        print "Done Loading \n Status Report:"
        print str(num_words) + " word instances loaded over " + str(len(self.tags)) + ' unique words'
        print "There were " + str(stop_words) + ' stop words'
        return True

    def loadAssociation(self, tag_text, post_id):
        if tag_text in self.tags:
            self.tags[tag_text].append(post_id)
        else:
            self.tags[tag_text] = [post_id]
        return True

    def getPostsThatHaveWordInTitle(self, tag_text):
        if tag_text not in self.tags:
            return []
        else:
            return self.tags[tag_text]

def main():
    titleIndex = TitleIndex()
    titleIndex.loadTitleIndexFromFile('titles.csv')

    while True:
        s = str(raw_input('find word: '))
        if s == '':
            break
        print 'finding : ' + s
        print titleIndex.getPostsThatHaveWordInTitle(s)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('',7778))
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

            if 'query' in data_obj:
                response['posts'] = titleIndex.getPostsThatHaveWordInTitle(data_obj['query'])
            
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

if __name__ == '__main__':
    main()
