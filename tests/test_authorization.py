from models.authorization import Authorization
from models.graphql_types import NewHouse

async def test_generate_auth():
    auth = Authorization() 
    id: int
  
    house = NewHouse(id=1, landlordId=1, houseKey="ABC123", firebaseId="")
    token = auth.generate_landlord_token(1, [house])
    print(auth.get_token_scope(token))
    assert False