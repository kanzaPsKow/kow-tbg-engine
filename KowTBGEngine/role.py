class Role:
    def __init__(self):
        """ 角色类
        """
        self.attributes = {  # 基础属性
            'id': 0,
            'name': '',
            'hp': 0,
            'mp': 0,
            'phy_atk': 0,
            'mag_atk': 0,
            'phy_dfn': 0,
            'mag_dfn': 0,
        }
        self.extra_attributes = {}  # 自定义基础属性
        self.attribute_modifiers = {}  # 属性值修饰

    def get_base_attribute(self, attribute):
        """ 获取一个属性的原始值
        attribute ->str 属性键
        return -> 指定属性的原始值，若无该属性则返回 None
        """
        if attribute in self.attributes:
            return self.attributes[attribute]
        elif attribute in self.extra_attributes:
            return self.extra_attributes[attribute]

    def get_attribute(self, attribute):
        """ 获取一个属性的计算结果
        attribute ->str 属性键
        return -> 指定属性的计算结果，若无该属性则返回 None
        """

    def set_attribute(self, **values):
        """ 设置属性的值
        values ->**dict{attribute, value} 属性键和属性值
        return ->list[str] 新加入自定义属性字典的键值
        """
        no_found_keys = []
        for k, v in values.items():
            if k in self.attributes:
                self.attributes[k] = v
            else:
                no_found_keys.append(k)
            self.extra_attributes[k] = v
        return no_found_keys