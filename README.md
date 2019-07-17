# fraddress-parser
fraddress is a python library for parsing unstructured FR addresses strings into address components using a custom NLP model taht learns from patterns. 
This library relies on the [parserator](https://github.com/datamade/parserator) library.


## How to use fraddress
Install fraddress with pip.
```bash
pip install fraddress
 ```

Then parse some address with parse or tag.
```
>>> import fraddress
>>> fraddress.parse('51 rue Nationale Paris 75006')
[('51', 'AddressNumber'), ('rue', 'StreetType'), ('Nationale', 'StreetName'), ('Paris', 'City'), ('75006', 'Zipcode')]

>>> fraddress.tag('51 rue Nationale Paris 75006')
OrderedDict([('AddressNumber', '51'), ('StreetType', 'rue'), ('StreetName', 'Nationale'), ('City', 'Paris'), ('Zipcode', '75006')])
```

## How to train a new parser
All you need is some training data to teach your parser about its domain, and then [follow the instructions of the U.S version](https://github.com/datamade/usaddress/tree/master/training).