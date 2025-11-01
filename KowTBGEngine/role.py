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
        self.states = []  # 状态列表

    def get_base_attribute(self, attribute):
        """ 获取一个属性的原始值\n
        attribute ->str 属性键\n
        return ->auto 指定属性的原始值，若无该属性则返回 None\n
        """
        if attribute in self.attributes:  # 搜寻默认存在的基础属性
            return self.attributes[attribute]
        elif attribute in self.extra_attributes:  # 搜寻自定义基础属性
            return self.extra_attributes[attribute]
        return None  # 搜寻无结果

    def set_modifier(self, tags, attribute, add_value=0, mul_value=1, modify_type='cor', sub_value=None):
        """ 添加属性修饰\n
        tags ->list 该修饰器的识别标签\n
        attribute ->str 修饰的属性的键\n
        add_value=0 ->auto 修饰的加值\n
        mul_value=1 ->int 修饰的乘值\n
        modify_type='add' ->str 修饰类型。'cor' 为在原值基础上应用加值和乘值，'sub' 为使用替换值替代原值\n
        sub_value=None ->auto 修饰的替换值。在 modify_type 为 'sub' 时生效\n
        """
        if attribute in self.attribute_modifiers:
            self.attribute_modifiers[attribute].append({'tags': tags, 'add_value': add_value, 'mul_value': mul_value, 'type': modify_type, 'sub_value': sub_value})
        else:
            self.attribute_modifiers[attribute] = [{'tags': tags, 'add_value': add_value, 'mul_value': mul_value, 'type': modify_type, 'sub_value': sub_value}]

    def get_attribute(self, attribute):
        """ 获取一个属性的计算结果\n
        attribute ->str 属性键\n
        return ->auto 指定属性的计算结果，若无该属性则返回 None\n
        """
        final_value = self.get_base_attribute(attribute)
        if final_value == None:
            return None
        if attribute in self.attribute_modifiers:
            is_sub = False
            for a in self.attribute_modifiers[attribute]:  # 优先处理替代值，后者覆盖前者
                if a['type'] == 'sub':
                    is_sub = True
                    final_value = a['sub_value']
            if is_sub:  # 处理替代值后直接返回
                return final_value
            for a in self.attribute_modifiers[attribute]:  # 处理加值和乘值
                final_value += self.get_base_attribute(attribute)

    def set_attribute(self, **values):
        """ 设置属性的值\n
        values ->**dict{attribute, value} 属性键和属性值\n
        return ->list[str] 新加入自定义属性字典的键值\n
        """
        no_found_keys = []
        for k, v in values.items():
            if k in self.attributes:
                self.attributes[k] = v
            else:
                no_found_keys.append(k)
            self.extra_attributes[k] = v
        return no_found_keys