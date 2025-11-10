from . import tbg_object

class BattleScene(tbg_object.TBGObject):
    """ 战斗场景类 """
    def _tbg_init(self):
        self.attributes = {
            'roles': [],
            'states': [],
        }

    def battle(commands):
        """ 进行一次战斗\n
        commands ->list 指令集\n
        """