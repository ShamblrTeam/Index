Run with Python 2.7

HOW TO USE THE INDEX
==============

It is currently running on port 7777 on helix.vis.uky.edu. You pass a json `{'query':'yolo'}` object with your query. It will return a json object '{'worked':True,'posts':[1,2,3,4,5,...,N]}' with the `post_id`s. Consult `test_socket.py` for an example.


SETUP
=========

To get tags, run:  `COPY tag TO '/Users/cs585/tags.csv' DELIMITER ',' CSV HEADER;` in database.

Then run: `scp cs585@172.31.40.208:~/tags.csv .` to get the data.


`python tag_index.py` will load and start the tag index on port 7777

`python title_index.py` will load and start the tag index on port 7778


`python tag_index.py --test` loads the data, but then allows you to play around with testing it via input. Press enter on an empty input to start the sockets. (same for `title_index`)

Run `python test_socket.py` to test the socket.

Eyeballing it, appears to use around ~650 MB of RAM for tag index. Title not tested yet at scale.

