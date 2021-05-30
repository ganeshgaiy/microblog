from app import app,db
from app.models import User,Post

@app.shell_context_processor
def make_shell_context():
	return {'db':db,'User':User,'Post':Post}



''' 
jwt is a JSON object which represents a set of claims. The claim is always a name-value pair. The claim has a claim name 
and a claim value.


>import jwt
>>key = 'secret'
>>encoded = jwt.encode({'some': 'payload'}, key, algorithm='HS256')
'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
>>decoded = jwt.decode(encoded, key, algorithms='HS256')
{'some': 'payload'}

'''