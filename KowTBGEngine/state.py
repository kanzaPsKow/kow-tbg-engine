from . import tbg_object

class State(tbg_object.TBGObject):
    """ 状态类 """
    def _tbg_init(self):
        self.attributes = {
            'name': '',
            'master': None,  # 挂载的对象
            'value_effect': [],
            'logic_effect': [],
            'hide': False,  # 是否在状态列表内隐藏
        }

    def affect(self):
        pass