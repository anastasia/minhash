### MinHash
MinHash explanation: http://infolab.stanford.edu/~ullman/mmds/book.pdf 
(chapter 3, also archived here: https://perma.cc/K9B4-QTX3)
A simple take here: https://moz.com/devblog/near-duplicate-detection/

This implementation borrows from Chris McCormick's MinHash tutorial.
https://github.com/chrisjmccormick/MinHash

#### To install (for now):
`pip install -e "git+git://github.com/anastasia/minhash.git@master#egg=minhash"`

#### To run in CLI:
`python minhash.py doc1 doc2`

#### To run in python:
`minhash.get_minhash(string_a, string_b)`
