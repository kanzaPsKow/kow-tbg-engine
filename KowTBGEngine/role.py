from . import tbg_object

class Role(tbg_object.TBGObject):
    """ 角色类 """
    def _tbg_init(self):
        self.attributes = {
            'id': 0,
            'position': 0,
            'name': '',
            'hp': 0,
            'mp': 0,
            'phy_atk': 0,
            'mag_atk': 0,
            'phy_dfn': 0,
            'mag_dfn': 0,
        }
        self.attribute_modifiers = {}  # 属性修饰器字典
        self.states = []  # 状态列表

    def add_modifier(self, tags, attribute, add_value=0, mul_value=1, modify_type='cor', sub_value=None):
        """ 添加属性修饰器\n
        tags ->dict 该修饰器的识别标签\n
        attribute ->str 修饰的属性的键\n
        add_value=0 ->int 修饰的加值\n
        mul_value=1 ->int 修饰的乘值\n
        modify_type='add' ->str 修饰类型。'cor' 为在原值基础上应用加值和乘值，'sub' 为使用替换值替代原值\n
        sub_value=None ->Any 修饰的替换值。在 modify_type 为 'sub' 时生效\n
        """
        if attribute in self.attribute_modifiers:  # 若该属性存在修饰器列表，则在列表末尾添加
            self.attribute_modifiers[attribute].append(Modifier(tags, add_value, mul_value, modify_type, sub_value))
        else:  # 若该属性不存在修饰器列表，则创建列表
            self.attribute_modifiers[attribute] = [Modifier(tags, add_value, mul_value, modify_type, sub_value)]

    def get_modified_attribute(self, attribute, sub_break=True):
        """ 获取一个属性的计算结果\n
        attribute ->str 属性键\n
        sub_break=True ->bool 替换值生效后是否中断加值和乘值的计算
        return ->Any 指定属性的计算结果，若无该属性则返回 None\n
        """
        base_value = self.get_attribute(attribute)
        final_value = base_value
        if final_value == None:
            return None
        if attribute in self.attribute_modifiers:
            is_sub = False
            for a in self.attribute_modifiers[attribute]:  # 优先处理替换值，后者覆盖前者
                if a.type == 'sub':
                    is_sub = True
                    final_value = a.sub_value
            if is_sub and sub_break:  # 若没有特殊要求，处理替换值后直接返回，不再处理加值和乘值
                return final_value
            for a in self.attribute_modifiers[attribute]:  # 处理加值和乘值
                final_value += base_value * (a.mul_value - 1) + a.add_value
        return final_value

    def get_all_modifiers(self):
        """ 获取属性修饰器字典
        return ->dict{str: list[role.Modifier]}
        """
        return self.attribute_modifiers

    def search_modifiers(self, attribute, in_tags, not_in_tags):
        """ 按照属性修饰器的 tags 对修饰器进行检索
        attribute ->str|None 被检索修饰器的目标属性，若为 None 则不筛选
        in_tags ->list 被检索修饰器拥有的 tags 键
        not_in_tags ->list 被检索修饰器没有的 tags 键
        return ->list[role.Modifier] 符合索引条件的修饰器的引用
        """
        matched_modifiers = []
        target_attributes = []
        if attribute == None:
            target_attributes = list(self.attribute_modifiers.keys())
        else:
            if attribute in self.attribute_modifiers.keys():
                target_attributes = [attribute]
        for a in target_attributes:
            for m in self.attribute_modifiers[a]:  # 遍历目标属性的修饰器
                tags_matched = True
                for t in in_tags:  # 遍历需要拥有的 tags 键
                    if not t in m.tags:  # 不符合条件
                        tags_matched = False
                        break
                if tags_matched:  # in_tags 符合，则继续判断 not_in_tags
                    for t in not_in_tags:
                        if t in m.tags:  # 不符合条件
                            tags_matched = False
                            break
                if tags_matched:  # 符合条件
                    matched_modifiers.append(m)
        return matched_modifiers

class Modifier:
    def __init__(self, tags, add_value=0, mul_value=1, modify_type='add', sub_value=None):
        """ 属性修饰器\n
        tags ->dict 该修饰器的识别标签\n
        add_value=0 ->auto 修饰的加值\n
        mul_value=1 ->int 修饰的乘值\n
        modify_type='add' ->str 修饰类型。'cor' 为在原值基础上应用加值和乘值，'sub' 为使用替换值替代原值\n
        sub_value=None ->Any 修饰的替换值。在 modify_type 为 'sub' 时生效\n
        """
        self.tags = tags
        self.add_value = add_value
        self.mul_value = mul_value
        self.type = modify_type
        self.sub_value = sub_value