from scripts.Class.GameObject import GameObject, Transform

class Player(GameObject):

    __static_playerList = []

    def __init__(self):
        self.idx = len(Player.GetPlayers())
        super().__init__(f"Player {self.idx}", Transform)
        if (self.idx>=1):
            print(">2 Player modes are not currently supported")

            del(self)

            return
        
        Player.__static_playerList.append()

    @staticmethod
    def GetPlayers():
        return Player.__static_playerList
    
    def update():
        ...

Player.GetPlayers()