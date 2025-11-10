class TBGObject:
    """ 基类 """
    def __init__(self):
        self.attributes = {} # 基础属性
        self.extra_attributes = {}  # 自定义基础属性
        self._tbg_init()  # 调用自定义初始化方法

    def _tbg_init(self):
        """ 自定义初始化方法\n
        """
        pass

    def set_attribute(self, **values):
        """ 设置基础属性的值\n
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
    def __setitem__(self, key, value):  # object.set_attribute('key': value) 可写作 object['key'] = value
        self.set_attribute(**{key: value})

    def get_attribute(self, attribute):
        """ 获取一个属性的值\n
        attribute ->str 属性键\n
        return ->Any 指定属性的原始值，若无该属性则返回 None\n
        """
        if attribute in self.attributes:  # 搜寻默认存在的基础属性
            return self.attributes[attribute]
        elif attribute in self.extra_attributes:  # 搜寻自定义基础属性
            return self.extra_attributes[attribute]
        return None  # 搜寻无结果
    def __getitem__(self, attribute):  # object.get_attribute('key') 可写作 object['key']
        return self.get_attribute(attribute)

    def get_all_attribute(self):
        """ 获取包括所有属性的字典\n
        return ->dict 默认属性字典和自定义属性字典合并的字典\n
        """
        return {**self.attributes, **self.extra_attributes}

    def del_attribute(self, *attribute):
        """ 删除指定属性\n
        *attribute ->str 要删除属性的键
        """
        if attribute in self.attributes:  # 搜寻默认存在的基础属性
            del self.attributes[attribute]
        elif attribute in self.extra_attributes:  # 搜寻自定义基础属性
            del self.extra_attributes[attribute]