####################定義類別######################
#基本玩家類別
class Player:
    def __init__(self,name,health,attack,defense):
        """"""
        self.name=name
        self.health=health
        self.attack=attack
        self.defense=defense
    def take_damage(self,damage):
        if damage>self.defense:
            self.health-=damage-self.defense
            return f"{self.name}受到了{damage}點傷害!"
        else:
            return f"{self.name}成功抵擋攻擊"
#法師類別
class Mage(Player):
    def __init__(self,name,health,attack,defense,magic_power):
        super().__init__(name,health,attack,defense)
        self.magic_power=magic_power
    def cast_spell(self):
        self.magic_power-=10
        return self.attack+self.magic_power
#戰士類別
class Warrior(Player):
    def __init__(self, name, health, attack, defense,armor):
        super().__init__(name, health, attack, defense)
        self.armor=armor
    def use_armor(self):
        self.health+=self.armor
        return f"{self.name}使用裝甲.增加了{self.armor}點體力!"
#新增一個玩家
# player1=Player("你在哈囉",100,2,9)
# print(f"玩家名稱:{player1.name}")
# print(f"玩家血量:{player1.health}")
# print(f"玩家攻擊:{player1.attack}")
# print(f"玩家防禦:{player1.defense}")
# #新增一個玩家
# player2=Player("你好啊",50,10,5)
# print(f"玩家名稱:{player1.name}")
# print(f"玩家血量:{player1.health}")
# print(f"玩家攻擊:{player1.attack}")
# print(f"玩家防禦:{player1.defense}")
# #玩家1攻擊玩家2
# print(player2.take_damage(player1.attack))
# print(f"玩家2血量剩餘:{player2.health}")
player1=Warrior("戰士小明",100,15,10,5)
player2=Mage("法師曉華",80,10,5,20)

print(f"{player1.name}血量剩餘:{player1.health}")
print(player1.use_armor())
print(f"{player1.name}血量剩餘:{player1.health}")

print(f"{player2.name}目前魔力:{player2.magic_power}")
player1.take_damage(player2.cast_spell())
print(f"{player2.name}對{player1.name}師法魔法攻擊!")
print(f"{player2.name}目前魔力:{player2.magic_power}")
print(f"{player1.name}血量剩餘:{player1.health}")
####################定義函式######################

####################初始化######################

####################載入圖片物件######################

######################建立視窗######################

######################分數物件######################

######################恐龍物件######################

######################仙人掌物件######################

######################遊戲結束物件######################

######################翼龍物件######################

######################循環偵測######################